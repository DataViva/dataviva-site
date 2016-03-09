# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, url_for, flash
from dataviva.apps.general.views import get_locale

from forms import RegistrationForm
from mock import Article, articles, ids
import time
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
    from models import Article
    articles = Article.query.all()
    return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    id = int(id.encode())
    article = articles[id]
    return render_template('scholar/show.html', article=article, id=id)


@mod.route('/article/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('scholar/new.html', form=form, action=url_for('scholar.create'))


@mod.route('/article/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    id = int(id.encode())
    article = articles[id]
    form.title.data = article.title
    form.theme.data = article.theme
    form.author.data = article.author
    form.key_words.data = article.key_words
    form.abstract.data = article.abstract
    return render_template('scholar/edit.html', form=form, action=url_for('scholar.update', id=id))


@mod.route('/article/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('scholar/new.html', form=form)
    else:
        from models import Article, Author, KeyWord
        from dataviva import db

        article = Article()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        article.file_path = 'test'
        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        author = form.author.data
        author = [Author(author)]

        key_word_input_list = form.key_words.data
        for key_word_input in key_word_input_list:
            key_word = KeyWord.query.filter_by(key_word=key_word_input).first()

            if not key_word:
                article.key_words.append(KeyWord(key_word_input))
            else:
                article.key_words.append(key_word)

        db.session.add(article)
        db.session.commit()

        message = u'Muito obrigado! Seu estudo foi submetido com sucesso e será analisado pela equipe do DataViva. \
                  Em até 15 dias você receberá um retorno sobre sua publicação no site!'
        flash(message, 'success')
        return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('scholar/edit.html', form=form)
    else:
        title = form.title.data
        theme = form.theme.data
        author = form.author.data
        key_words = form.key_words.data
        abstract = form.abstract.data
        postage_date = time.strftime("%d/%m/%Y")

        articles[id] = Article(title, theme, author, key_words, abstract, postage_date)
        message = u'Estudo editado com sucesso!'
        flash(message, 'success')
        return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>/delete', methods=['GET'])
def delete(id):
    if articles.pop(int(id.encode())):
        message = u"Estudo excluído com sucesso!"
        flash(message, 'success')
        return render_template('scholar/index.html', articles=articles)
    else:
        return make_response(render_template('not_found.html'), 404)
