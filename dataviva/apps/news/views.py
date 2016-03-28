# -*- coding: utf-8 -*-
import os
from flask import Blueprint, render_template, g, make_response, redirect, url_for, flash
from dataviva.apps.general.views import get_locale

from models import Publication, AuthorNews
from dataviva import db, app
from forms import RegistrationForm
from datetime import datetime
from random import randrange

mod = Blueprint('news', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/news')

UPLOAD_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], mod.name)
STATIC_UPLOAD_FOLDER = '/static/uploads/' + mod.name


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
    publications = Publication.query.all()
    return render_template('news/index.html', publications=publications)


@mod.route('/publication/<id>', methods=['GET'])
def show(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    publications = Publication.query.filter(Publication.id != id).all()
    if len(publications) > 3:
        read_more = [
            publications.pop(randrange(len(publications))) for _ in range(3)]
    else:
        read_more = publications
    return render_template('news/show.html', publication=publication, id=id, read_more=read_more)


@mod.route('/publication/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('news/new.html', form=form, action=url_for('news.create'))


@mod.route('/publication/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    publication = Publication.query.filter_by(id=id).first_or_404()
    form.title.data = publication.title
    form.authors.data = publication.authors_str()
    form.subject.data = publication.subject
    form.text_content.data = publication.text_content

    form.image.data = publication.image_path
    form.thumb.data = publication.thumb_path

    return render_template('news/edit.html', form=form, action=url_for('news.update', id=id))


@mod.route('/publication/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('news/new.html', form=form)
    else:
        publication = Publication()
        publication.title = form.title.data
        publication.subject = form.subject.data
        publication.text_content = form.text_content.data
        publication.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            publication.authors.append(AuthorNews(author_input))

        db.session.add(publication)
        db.session.flush()

        if form.image.data.filename:
            import pdb; pdb.set_trace()
            publication.image_path = save_file(
                form.image.data, 'image' + str(publication.id))

        if form.thumb.data.filename:
            publication.thumb_path = save_file(
                form.thumb.data, 'thumb' + str(publication.id))

        db.session.commit()

        message = u'Muito obrigado! Seu publication foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.index'))


def save_file(file, name):
    file_ext = os.path.splitext(file.filename)[-1]
    file_name = name + file_ext
    file.save(UPLOAD_FOLDER + '/' + file_name)
    return STATIC_UPLOAD_FOLDER + '/' + file_name


@mod.route('/publication/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if not form.validate_on_submit():
        return render_template('news/edit.html', form=form)
    else:
        publication = Publication.query.filter_by(id=id).first_or_404()
        publication.title = form.title.data
        publication.subject = form.subject.data
        publication.text_content = form.text_content.data
        publication.image_path = 'http://agenciatarrafa.com.br/2015/wp-content/uploads/2015/09/google-ads-1000x300.jpg'
        publication.thumb_path = 'http://1un1ba2fg8v82k48vu4by3q7.wpengine.netdna-cdn.com/wp-content/uploads/2014/05/Mobile-Analytics-Picture-e1399568637490-350x227.jpg'
        publication.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        publication.authors = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            publication.authors.append(AuthorNews(author_input))

        db.session.commit()

        message = u'Publicação editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.index'))


@mod.route('/publication/<id>/delete', methods=['GET'])
def delete(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    if publication:
        db.session.delete(publication)
        db.session.commit()
        message = u"Publicação excluída com sucesso!"
        flash(message, 'success')
        return redirect(url_for('news.index'))
    else:
        return make_response(render_template('not_found.html'), 404)
