# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

from models import Publication, AuthorNews
from dataviva import db
from forms import RegistrationForm
from datetime import datetime
from random import randrange

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
    publications = Publication.query.filter_by(active=True).all()
    return render_template('news/index.html', publications=publications)


@mod.route('/publication/<id>', methods=['GET'])
def show(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    publications = Publication.query.filter(Publication.id != id, Publication.active).all()
    if len(publications) > 3:
        read_more = [publications.pop(randrange(len(publications))) for _ in range(3)]
    else:
        read_more = publications
    return render_template('news/show.html', publication=publication, id=id, read_more=read_more)


@mod.route('/publication/all', methods=['GET'])
def all():
    result = Publication.query.all()
    publications = []
    for row in result:
        publications += [(row.id, row.title, row.authors_str(),
                          row.last_modification.strftime('%d/%m/%Y'), row.show_home, row.active)]
    return jsonify(publications=publications)


@mod.route('/admin', methods=['GET'])
def admin():
    publications = Publication.query.all()
    return render_template('news/admin.html', publications=publications)


@mod.route('/admin/publication/<status>/<status_value>', methods=['POST'])
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        publication = Publication.query.filter_by(id=id).first_or_404()
        setattr(publication, status, status_value == u'true')
        db.session.commit()

    message = u"Notícia(s) alterada(s) com sucesso!"
    return message, 200


@mod.route('/admin/delete', methods=['POST'])
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        publications = Publication.query.filter(Publication.id.in_(ids)).all()
        for publication in publications:
            db.session.delete(publication)

        db.session.commit()
        return u"Notícia(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma notícia para excluí-la.', 205


@mod.route('/admin/publication/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('news/new.html', form=form, action=url_for('news.create'))


@mod.route('/admin/publication/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('news/new.html', form=form)
    else:
        publication = Publication()
        publication.title = form.title.data
        publication.subject = form.subject.data
        publication.text_content = form.text_content.data
        publication.text_call = form.text_call.data
        publication.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.thumb = form.thumb.data
        publication.active = 0

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            publication.authors.append(AuthorNews(author_input))

        db.session.add(publication)
        db.session.commit()

        message = u'Muito obrigado! Sua notícia foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.admin'))


@mod.route('/admin/publication/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    publication = Publication.query.filter_by(id=id).first_or_404()
    form.title.data = publication.title
    form.authors.data = publication.authors_str()
    form.subject.data = publication.subject
    form.text_content.data = publication.text_content
    form.publish_date.data = publication.publish_date
    form.text_call.data = publication.text_call
    form.show_home.data = publication.show_home
    form.thumb.data = publication.thumb
    return render_template('news/edit.html', form=form, action=url_for('news.update', id=id))


@mod.route('/publication/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('news/edit.html', form=form)
    else:
        publication = Publication.query.filter_by(id=id).first_or_404()
        publication.title = form.title.data
        publication.subject = form.subject.data
        publication.text_content = form.text_content.data
        publication.thumb = form.thumb.data
        publication.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        publication.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        publication.show_home = form.show_home.data
        publication.authors = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            publication.authors.append(AuthorNews(author_input))

        db.session.commit()

        message = u'Notícia editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.admin'))
