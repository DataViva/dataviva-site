# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
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
from dataviva.utils.upload_helper import save_b64_image, delete_s3_folder, upload_images_to_s3, save_file_temp, clean_s3_folder
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


@mod.route('/', methods=['GET'])
def index():
    publications = Publication.query.filter_by(active=True).order_by(
        desc(Publication.publish_date)).all()
    subjects_query = PublicationSubject.query.order_by(desc(PublicationSubject.name_pt)).all()
    subjects = []

    for subject_query in subjects_query:
        for row in subject_query.publications:
            if row.active is True:
                subjects.append(subject_query)
                break

    return render_template('news/index.html', publications=publications, subjects=subjects)


@mod.route('/<subject>', methods=['GET'])
def index_subject(subject):
    publications_query = Publication.query.filter_by(
        active=True).order_by(desc(Publication.publish_date)).all()
    subjects_query = subjects_query = PublicationSubject.query.order_by(
        desc(PublicationSubject.name_pt)).all()
    publications = []
    subjects = []

    for subject_query in subjects_query:
        for row in subject_query.publications:
            if row.active is True:
                subjects.append(subject_query)
                break

    for publication in publications_query:
        if float(subject) in [x.id for x in publication.subjects]:
            publications.append(publication)

    return render_template(
        'news/index.html', publications=publications, subjects=subjects, active_subject=long(subject))


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
    return render_template('news/show.html', publication=publication, id=id, read_more=read_more)


@mod.route('/publication/all', methods=['GET'])
def all():
    result = Publication.query.all()
    publications = []
    for row in result:
        publications += [(row.id, row.title_pt, row.author,
                          row.publish_date.strftime('%d/%m/%Y'), row.show_home, row.active)]
    return jsonify(publications=publications)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    publications = Publication.query.all()
    return render_template('news/admin.html', publications=publications)


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
    if ids:
        publications = Publication.query.filter(Publication.id.in_(ids)).all()
        for publication in publications:
            delete_s3_folder(os.path.join(mod.name, str(publication.id)))
            db.session.delete(publication)

        db.session.commit()
        return u"Notícia(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma notícia para excluí-la.', 205


@mod.route('/admin/publication/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    return render_template('news/new.html', form=form, action=url_for('news.create'))


@mod.route('/admin/publication/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('news/new.html', form=form)
    else:
        publication = Publication()
        publication.title_pt = form.title_pt.data
        publication.title_en = form.title_en.data
        publication.text_call_pt = form.text_call_pt.data
        publication.text_call_en = form.text_call_en.data
        publication.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.dual_language = form.dual_language.data
        publication.active = 0
        publication.author = form.author.data

        subjects_pt = form.subject_pt.data.replace(', ', ',').split(',')

        if form.dual_language.data:
            subjects_en = form.subject_en.data.replace(', ', ',').split(',')
            for name_pt, name_en in zip(subjects_pt, subjects_en):
                subject = PublicationSubject.query.filter_by(name_pt=name_pt, name_en=name_en).first()
                if not subject:
                    subject = PublicationSubject()
                    subject.name_pt = name_pt
                    subject.name_en = name_en
                publication.subjects.append(subject)
        else:
            for name_pt in subjects_pt:
                subject = PublicationSubject.query.filter_by(name_pt=name_pt, name_en='').first()
                if not subject:
                    subject = PublicationSubject()
                    subject.name_pt = name_pt
                    subject.name_en = ''
                    publication.subjects.append(subject)

        db.session.add(publication)
        db.session.flush()

        text_content_pt = upload_images_to_s3(
            form.text_content_pt.data, mod.name, publication.id)
        text_content_en = upload_images_to_s3(
            form.text_content_en.data, mod.name, publication.id)
        Publication.query.get(publication.id).text_content_pt = text_content_pt
        Publication.query.get(publication.id).text_content_en = text_content_en
        clean_s3_folder(text_content_en, text_content_pt, mod.name, publication.id)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, str(publication.id), 'images')
            publication.thumb = save_b64_image(form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()
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
    images = { key: value for key, value in request.form.items() if key != 'csrf_token' }
    path_hash = request.form['csrf_token'].replace('#', '')
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, path_hash, 'images')
    return jsonify(file_paths=save_images_temporarily(upload_folder, images))


@mod.route('/admin/publication/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    form = RegistrationForm()
    publication = Publication.query.filter_by(id=id).first_or_404()
    form.title_pt.data = publication.title_pt
    form.title_en.data = publication.title_en
    form.author.data = publication.author
    form.text_content_pt.data = publication.text_content_pt
    form.text_content_en.data = publication.text_content_en
    form.publish_date.data = publication.publish_date
    form.text_call_pt.data = publication.text_call_pt
    form.text_call_en.data = publication.text_call_en
    form.show_home.data = publication.show_home
    form.dual_language.data = publication.dual_language
    form.thumb.data = publication.thumb
    form.subject_pt.data = ', '.join([sub.name_pt for sub in publication.subjects])
    if publication.dual_language:
        form.subject_en.data = ', '.join([sub.name_en for sub in publication.subjects])

    return render_template('news/edit.html', form=form, action=url_for('news.update', id=id))


@mod.route('/admin/publication/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('news/edit.html', form=form)
    else:
        publication = Publication.query.filter_by(id=id).first_or_404()
        publication.title_pt = form.title_pt.data
        publication.title_en = form.title_en.data
        publication.text_call_pt = form.text_call_pt.data
        publication.text_call_en = form.text_call_en.data
        publication.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.dual_language = form.dual_language.data
        publication.author = form.author.data

        subjects_pt = form.subject_pt.data.replace(', ', ',').split(',')
        num_subjects = len(publication.subjects)

        for i in range(0, num_subjects):
            publication.subjects.remove(publication.subjects[0])

        if form.dual_language.data:
            subjects_en = form.subject_en.data.replace(', ', ',').split(',')
            for name_pt, name_en in zip(subjects_pt, subjects_en):
                subject = PublicationSubject.query.filter_by(name_pt=name_pt, name_en=name_en).first()
                if not subject:
                    subject = PublicationSubject()
                    subject.name_pt = name_pt
                    subject.name_en = name_en
                publication.subjects.append(subject)
        else:
            for name_pt in subjects_pt:
                subject = PublicationSubject.query.filter_by(name_pt=name_pt, name_en='').first()
                if not subject:
                    subject = PublicationSubject()
                    subject.name_pt = name_pt
                    subject.name_en = ''
                    publication.subjects.append(subject)

        publication.text_content_pt = upload_images_to_s3(
            form.text_content_pt.data, mod.name, publication.id)
        publication.text_content_en = upload_images_to_s3(
            form.text_content_en.data, mod.name, publication.id)
        clean_s3_folder(publication.text_content_pt, publication.text_content_en, mod.name, publication.id)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, str(publication.id), 'images')
            publication.thumb = save_b64_image(form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()
        message = u'Notícia editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.admin'))
