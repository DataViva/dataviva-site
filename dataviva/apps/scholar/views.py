# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, redirect, url_for, flash
from dataviva.apps.general.views import get_locale

from models import Article, Author, KeyWord
from dataviva import db
from forms import RegistrationForm
from datetime import datetime


mod = Blueprint('scholar', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/scholar')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    articles = Article.query.all()
    return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    article = Article.query.filter_by(id=id).first()
    return render_template('scholar/show.html', article=article)


@mod.route('/article/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('scholar/new.html', form=form, action=url_for('scholar.create'))


@mod.route('/article/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    article = Article.query.filter_by(id=id).first()
    form.title.data = article.title
    form.theme.data = article.theme
    form.authors.data = article.authors
    form.keywords.data = article.keywords
    form.abstract.data = article.abstract
    return render_template('scholar/edit.html', form=form, action=url_for('scholar.update', id=id))


@mod.route('/article/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('scholar/new.html', form=form)
    else:
        article = Article()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        article.file_path = 'test'
        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            article.authors.append(Author(author_input))

        keyword_input_list = form.keywords.data.split(',')
        for keyword_input in keyword_input_list:
            keyword = KeyWord.query.filter_by(name=keyword_input).first()

            if not keyword:
                article.keywords.append(KeyWord(keyword_input))
            else:
                article.keywords.append(keyword)

        db.session.add(article)
        db.session.commit()

        message = u'Muito obrigado! Seu estudo foi submetido com sucesso e será analisado pela equipe do DataViva. \
                  Em até 15 dias você receberá um retorno sobre sua publicação no site!'
        flash(message, 'success')
        return redirect(url_for('scholar.index'))


@mod.route('/article/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('scholar/edit.html', form=form)
    else:
        article = Article.query.filter_by(id=id).first()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        article.file_path = 'test'
        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            article.authors.append(Author(author_input))

        keyword_input_list = form.keywords.data.split(',')
        for keyword_input in keyword_input_list:
            keyword = KeyWord.query.filter_by(name=keyword_input).first()

            if not keyword:
                article.keywords.append(KeyWord(keyword_input))
            else:
                article.keywords.append(keyword)

        db.session.commit()

        message = u'Estudo editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('scholar.index'))


@mod.route('/article/<id>/delete', methods=['GET'])
def delete(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
        message = u"Estudo excluído com sucesso!"
        flash(message, 'success')
        return redirect(url_for('scholar.index'))
    else:
        return make_response(render_template('not_found.html'), 404)
