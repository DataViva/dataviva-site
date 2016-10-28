# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request, send_file
from dataviva.apps.general.views import get_locale
from flask.ext.login import login_required
from sqlalchemy import desc
from models import Publication, PublicationSubject
from dataviva import db
from forms import RegistrationForm
from datetime import datetime
from random import randrange
from dataviva.apps.admin.views import required_roles
from dataviva import app
from dataviva.utils.upload_helper import log_operation, save_b64_image, delete_s3_folder, upload_images_to_s3, save_file_temp, clean_s3_folder, get_logs, zip_logs
from flask_paginate import Pagination
from config import ITEMS_PER_PAGE, BOOTSTRAP_VERSION
import os

mod = Blueprint('news', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/news')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def active_publications_subjects(language):
    subjects_query = PublicationSubject.query.filter_by(
        language=language).order_by(PublicationSubject.name).all()
    subjects = []
    for subject_query in subjects_query:
        for row in subject_query.publications:
            if row.active is True:
                subjects.append(subject_query)
                break
    return subjects


@mod.route('/', methods=['GET'])
@mod.route('/<int:page>', methods=['GET'])
def index(page=1):
    publications_query = Publication.query.filter_by(active=True, language=g.locale)
    publications = []

    subject = request.args.get('subject')
    if subject:
        publications = publications_query.filter(Publication.subjects.any(PublicationSubject.id == subject)).order_by(
            desc(Publication.publish_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_publications = publications_query.filter(
            Publication.subjects.any(PublicationSubject.id == subject)).count()
    else:
        publications = publications_query.order_by(
            desc(Publication.publish_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_publications = publications_query.count()

    pagination = Pagination(page=page,
                            total=num_publications,
                            per_page=ITEMS_PER_PAGE,
                            bs_version=BOOTSTRAP_VERSION)

    return render_template('news/index.html',
                           publications=publications,
                           subjects=active_publications_subjects(g.locale),
                           pagination=pagination)


@mod.route('/publication/<id>', methods=['GET'])
def show(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    publications = Publication.query.filter(
        Publication.id != id, Publication.active).all()
    if len(publications) > 3:
        read_more = [
            publications.pop(randrange(len(publications))) for _ in range(3)]
    else:
        read_more = publications
    return render_template('news/show.html',
                           publication=publication,
                           subjects=active_publications_subjects(g.locale),
                           id=id,
                           read_more=read_more)


@mod.route('/publication/all', methods=['GET'])
def all():
    result = Publication.query.all()
    publications = []
    for row in result:
        publications += [(row.id, row.title, row.language.upper(), row.author,
            row.publish_date.strftime('%d/%m/%Y'), row.show_home, row.active)]
    return jsonify(publications=publications)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    publications = Publication.query.all()
    return render_template('news/admin.html', publications=publications)


@mod.route('/admin/logs/get', methods=['GET'])
@login_required
@required_roles(1)
def admin_get_logs():
    return jsonify(logs=get_logs(mod.name))


@mod.route('/admin/logs/zip', methods=['GET'])
@login_required
@required_roles(1)
def admin_zip_logs():
    zipfile = zip_logs(mod.name)
    if zipfile:
        response = send_file(zipfile['location'], attachment_filename=zipfile['name'], as_attachment=True)
        if os.path.isfile(zipfile['location']):
            os.remove(zipfile['location'])
        return response
    flash('Não foi possível baixar o arquivo.', 'danger')
    return redirect(url_for('news.admin'))

@mod.route('/admin/publication/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        publication = Publication.query.filter_by(id=id).first_or_404()
        setattr(publication, status, status_value == u'true')
        db.session.commit()

    message = u"Notícia(s) alterada(s) com sucesso!"
    return message, 200


@mod.route('/admin/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    subjects = PublicationSubject.query.all()
    deleted_publications = []

    if ids:
        publications = Publication.query.filter(Publication.id.in_(ids)).all()
        for publication in publications:
            try:
                delete_s3_folder(os.path.join(mod.name, str(publication.id)))
            except Exception:
                pass
            db.session.delete(publication)
            db.session.flush()
            deleted_publications.append((publication.id, publication.title))

            for subject in subjects:
                if subject.publications.count() == 0:
                    db.session.delete(subject)

        db.session.commit()
        log_operation(module=mod.name, operation='delete', user=(g.user.id, g.user.email), objs=deleted_publications)
        return u"Notícia(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma notícia para excluí-la.', 205


@mod.route('/admin/publication/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    form.set_choices()
    return render_template('news/new.html', form=form, action=url_for('news.create'))


@mod.route('/admin/publication/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    if form.validate() is False:
        form.set_choices()
        return render_template('news/new.html', form=form)
    else:
        publication = Publication()
        publication.title = form.title.data
        publication.text_call = form.text_call.data
        publication.last_modification = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.active = 0
        publication.author = form.author.data
        publication.language = form.language.data
        publication.add_subjects(form.subject.data, form.language.data)

        db.session.add(publication)
        db.session.flush()

        text_content = upload_images_to_s3(
            form.text_content.data, mod.name, publication.id)
        Publication.query.get(publication.id).text_content = text_content
        clean_s3_folder(text_content, mod.name, publication.id)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], mod.name, str(publication.id), 'images')
            publication.thumb = save_b64_image(
                form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()
        log_operation(module=mod.name, operation='create', user=(g.user.id, g.user.email), objs=[(publication.id, publication.title)])
        message = u'Muito obrigado! Sua notícia foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.admin'))


@mod.route('/admin/upload', methods=['POST'])
@login_required
@required_roles(1)
def upload_image():
    file = request.files['image']
    csrf_token = request.form['csrf_token'].replace('#', '')
    image_url = save_file_temp(file, mod.name, csrf_token)
    return jsonify(image={'url': image_url})


@mod.route('/admin/publication/new/upload', methods=['POST'])
@login_required
@required_roles(1)
def upload_images():
    images = {key: value for key,
              value in request.form.items() if key != 'csrf_token'}
    path_hash = request.form['csrf_token'].replace('#', '')
    upload_folder = os.path.join(
        app.config['UPLOAD_FOLDER'], mod.name, path_hash, 'images')
    return jsonify(file_paths=save_images_temporarily(upload_folder, images))


@mod.route('/admin/publication/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    form = RegistrationForm()
    form.subject.choices = ([(subject.name, subject.name) for subject in publication.subjects])
    form.subject.choices.remove((publication.main_subject, publication.main_subject))
    form.subject.choices.insert(0, (publication.main_subject, publication.main_subject))
    form.set_choices()
    form.title.data = publication.title
    form.author.data = publication.author
    form.text_content.data = publication.text_content
    form.publish_date.data = publication.publish_date
    form.text_call.data = publication.text_call
    form.show_home.data = publication.show_home
    form.thumb.data = publication.thumb
    form.subject.data = [subject.name for subject in publication.subjects]
    form.language.data = publication.language

    return render_template('news/edit.html', form=form, action=url_for('news.update', id=id))


@mod.route('/admin/publication/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        form.set_choices()
        return render_template('news/edit.html', form=form)
    else:
        publication = Publication.query.filter_by(id=id).first_or_404()
        old_title = publication.title
        publication.title = form.title.data
        publication.text_call = form.text_call.data
        publication.last_modification = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.author = form.author.data
        publication.language = form.language.data

        num_subjects = len(publication.subjects)
        for i in range(0, num_subjects):
            publication.subjects.remove(publication.subjects[0])

        publication.add_subjects(form.subject.data, form.language.data)

        publication.text_content = upload_images_to_s3(
            form.text_content.data, mod.name, publication.id)
        clean_s3_folder(publication.text_content, mod.name, publication.id)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], mod.name, str(publication.id), 'images')
            publication.thumb = save_b64_image(
                form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()
        log_operation(module=mod.name, operation='edit', user=(g.user.id, g.user.email), objs=[(publication.id, old_title)])

        message = u'Notícia editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.admin'))
