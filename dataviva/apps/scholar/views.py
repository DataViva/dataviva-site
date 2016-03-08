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
    if not form.validate():
        return render_template('scholar/new.html', form=form)
    else:
        title = form.title.data
        theme = form.theme.data
        author = form.author.data
        key_words = form.key_words.data
        abstract = form.abstract.data
        postage_date = time.strftime("%d/%m/%Y")
        id = ids[-1] + 1

        ids.append(id)
        articles.update({id: Article(title, theme, author, key_words, abstract, postage_date)})

        #####

        from models import Article as ArticleModel
        from models import Theme as ThemeModel
        from models import Author as AuthorModel
        from models import KeyWord as KeyWordModel
        from dataviva import db

        title = form.title.data
        theme = form.theme.data
        author = form.author.data
        first_name = 'A'
        last_name = 'B'
        key_word = form.key_words.data
        abstract = form.abstract.data
        file_path = 'test'
        postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        article = ArticleModel(title, abstract, file_path, postage_date)
        article_theme = ThemeModel(theme, id)
        article_author = AuthorModel(first_name, last_name)
        article_key_word = KeyWordModel(key_word)

        db.session.add(article)
        db.session.add(article_theme)
        db.session.add(article_author)
        db.session.add(article_key_word)
        db.session.commit()

        #####

        message = u'Muito obrigado! Seu estudo foi submetido com sucesso e será analisado pela equipe do DataViva. \
                  Em até 15 dias você receberá um retorno sobre sua publicação no site!'
        flash(message, 'success')
        return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if not form.validate():
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
