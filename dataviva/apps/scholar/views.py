# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request, send_from_directory
from dataviva.apps.general.views import get_locale

from sqlalchemy import desc
from models import Article, AuthorScholar, KeyWord
from dataviva import db
from forms import RegistrationForm
from datetime import datetime

import os
import simplejson
import upload_file as uploadfile
from werkzeug import secure_filename
from dataviva import app

app.config['UPLOAD_FOLDER'] = os.getcwd()+'/dataviva/static/data/scholar/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


mod = Blueprint('scholar', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/scholar')


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
    articles = Article.query.filter_by(approval_status=True).order_by(desc(Article.postage_date)).all()
    return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    article = Article.query.filter_by(id=id).first_or_404()
    return render_template('scholar/show.html', article=article)


@mod.route('/admin/article/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('scholar/new.html', form=form, action=url_for('scholar.create'))


@mod.route('/admin/article/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    article = Article.query.filter_by(id=id).first_or_404()
    form.title.data = article.title
    form.theme.data = article.theme
    form.authors.data = article.authors_str()
    form.keywords.data = article.keywords_str()
    form.abstract.data = article.abstract

    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(
        os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]

    file_display = []

    for f in files:
        size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
        file_saved = uploadfile(name=f, size=size)
        file_display.append(file_saved.get_file())

    #return simplejson.dumps({"files": file_display})

    return render_template('scholar/edit.html', form=form, action=url_for('scholar.update', id=id))


@mod.route('/admin/article/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('scholar/new.html', form=form)
    else:
        article = Article()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        form.article.data

        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)

            #return simplejson.dumps({"files": [result.get_file()]})

        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article.approval_status = 0

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            article.authors.append(AuthorScholar(author_input))

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


@mod.route('/admin/article/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('scholar/edit.html', form=form)
    else:
        article = Article.query.filter_by(id=id).first_or_404()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data

        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)

            #return simplejson.dumps({"files": [result.get_file()]})

        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article.authors = []
        article.keywords = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            article.authors.append(AuthorScholar(author_input))

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


@mod.route('/admin/article/delete', methods=['POST'])
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        articles = Article.query.filter(Article.id.in_(ids)).all()
        for article in articles:
            db.session.delete(article)

        db.session.commit()
        return u"Artigo(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum artigo para excluí-lo.', 205


@mod.route('/admin', methods=['GET'])
def admin():
    articles = Article.query.all()
    return render_template('scholar/admin.html', articles=articles)


@mod.route('/admin', methods=['POST'])
def admin_update():
    for id, approval_status in request.form.iteritems():
        article = Article.query.filter_by(id=id).first_or_404()
        article.approval_status = approval_status == u'true'
        db.session.commit()
    message = u"Estudo(s) atualizados com sucesso!"
    return message


@mod.route('/admin/article/<status>/<status_value>', methods=['POST'])
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        article = Article.query.filter_by(id=id).first_or_404()
        setattr(article, status, status_value == u'true')
        db.session.commit()

    message = u"Artigo(s) alterada(s) com sucesso!"
    return message, 200


@mod.route('/articles/all', methods=['GET'])
def all():
    result = Article.query.all()
    articles = []
    for row in result:
        articles += [(row.id, row.title, row.authors_str(),
                      row.postage_date.strftime('%d/%m/%Y'), row.approval_status)]
    return jsonify(articles=articles)


@mod.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@mod.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)
