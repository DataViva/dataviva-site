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
import shutil
from upload_file import UploadFile
from werkzeug import secure_filename
from dataviva import app
from dataviva.utils import upload_helper


ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'png', 'jpeg'])
IGNORED_FILES = set(['.gitignore'])


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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@mod.route('/', methods=['GET'])
def index():
    articles = Article.query.filter_by(approval_status=True).order_by(desc(Article.postage_date)).all()
    return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    article = Article.query.filter_by(id=id).first_or_404()
    return render_template('scholar/show.html', article=article)


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


@mod.route('/admin/article/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('scholar/new.html', form=form, action=url_for('scholar.create'))


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
        db.session.flush()

        csrf_token = request.form.get('csrf_token')

        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')

        file_name = [file for file in os.listdir(upload_folder)][0]

        upload_helper.upload_s3_file(
            os.path.join(upload_folder, file_name),
            os.path.join('scholar/', str(article.id), 'files/', 'article'),
            {
                'ContentType': "application/pdf",
                'ContentDisposition': 'attachment; filename=dataviva-article-' + str(article.id) + '.pdf'
            }
        )

        shutil.rmtree(upload_folder)

        db.session.commit()

        message = u'Muito obrigado! Seu estudo foi submetido com sucesso e será analisado pela equipe do DataViva. \
                  Em até 15 dias você receberá um retorno sobre sua publicação no site!'
        flash(message, 'success')
        return redirect(url_for('scholar.index'))


@mod.route('/admin/article/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    article = Article.query.filter_by(id=id).first_or_404()
    form.title.data = article.title
    form.theme.data = article.theme
    form.authors.data = article.authors_str()
    form.keywords.data = article.keywords_str()
    form.abstract.data = article.abstract

    return render_template('scholar/edit.html', form=form, action=url_for('scholar.update', id=id))


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


@mod.route('/articles/all', methods=['GET'])
def all():
    result = Article.query.all()
    articles = []
    for row in result:
        articles += [(row.id, row.title, row.authors_str(),
                      row.postage_date.strftime('%d/%m/%Y'), row.approval_status)]
    return jsonify(articles=articles)


@mod.route('/admin/article/upload', methods=['POST'])
def upload():

    csrf_token = request.values['csrf_token']

    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if request.files:
        file_name = request.files.keys()[0]
        file = request.files[file_name]
        file.save(os.path.join(upload_folder, file_name))
        return 'File Saved!'
    else:
        return 'Upload Error!', 400

    #TODO - Check file size and extension

@mod.route('/admin/article/udsapload', methods=['GET', 'POST'])
@mod.route('/admin/article/<id>/upload', methods=['GET', 'POST'])
def uploada(id=None):
    file_path = app.config['UPLOAD_FOLDER'] + request.form.get('csrf_token')

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    if request.method == 'POST':
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = UploadFile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(file_path, filename)
                file.save(uploaded_file_path)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = UploadFile(name=filename, type=mimetype, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [f for f in os.listdir(file_path) if os.path.isfile(
            os.path.join(file_path, f)) and f not in IGNORED_FILES]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(file_path, f))
            file_saved = UploadFile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('scholar.index'))


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
