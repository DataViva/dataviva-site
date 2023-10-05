# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request, send_from_directory, send_file
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva import app, db, admin_email
from dataviva.utils import upload_helper
from models import Article, AuthorScholar, KeyWord
from forms import RegistrationForm
from sqlalchemy import desc, or_, and_
from datetime import datetime
from flask.ext.login import login_required
from dataviva.apps.admin.views import required_roles
from dataviva.utils.send_mail import send_mail
from dataviva.utils.upload_helper import save_b64_image
from flask_paginate import Pagination
from config import ITEMS_PER_PAGE, BOOTSTRAP_VERSION
import os
import shutil
import fnmatch


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
@mod.route('/<int:page>', methods=['GET'])
def index(page=1):
    articles_query = Article.query.filter_by(approval_status=True)
    lang = get_locale()
    articles = []
    idList = []
    search = request.args.get('search').replace('+', ' ') if request.args.get('search') else ''
    keyword = request.args.get('keyword')
    
    if search:
        if keyword:
            idList = [int(id) for id in keyword.split(',')]
            filter_items = [KeyWord.id == id_ for id_ in idList]
            filter_condition = or_(*filter_items)

            string = "%" + search + "%"
            string_condition = or_(Article.title.ilike(string), Article.abstract.ilike(string))

            combined_condition = and_(filter_condition, string_condition)

            articles = articles_query.filter(combined_condition).order_by(
                desc(Article.postage_date)).paginate(page, ITEMS_PER_PAGE, True).items

            num_articles = len(articles)
        else:
            string = "%" + search + "%" 
            string_condition = or_(Article.title.ilike(string), Article.abstract.ilike(string))
            articles = articles_query.filter(string_condition).order_by(desc(Article.postage_date)).paginate(
                page, ITEMS_PER_PAGE, True).items
            num_articles = len(articles)
    elif keyword:
        idList = [int(id) for id in keyword.split(',')]
        filter_itens = [KeyWord.id == id for id in idList]
        filter_condition = or_(*filter_itens)
        articles = articles_query.filter(Article.keywords.any(filter_condition)).order_by(desc(Article.postage_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_articles = articles_query.filter(Article.keywords.any(filter_condition)).count()
    else:
        articles = articles_query.order_by(desc(Article.postage_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_articles = articles_query.count()
        
    pagination = Pagination(page=page,
                            total=num_articles,
                            per_page=ITEMS_PER_PAGE,
                            bs_version=BOOTSTRAP_VERSION)
    
    return render_template('scholar/index.html',
                            idList = idList,
                            articles=articles,
                            language=lang,
                            keywords=approved_articles_keywords(),
                            pagination=pagination)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    if (g.user.is_authenticated and g.user.is_admin()):
        article = Article.query.filter_by(id=id).first_or_404()
    else:
        article = Article.query.filter_by(approval_status=True, id=id).first_or_404()

    return render_template('scholar/show.html', article=article, language=get_locale())


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    articles = Article.query.all()
    return render_template('scholar/admin.html', articles=articles)

@mod.route('/admin/logs/get', methods=['GET'])
@login_required
@required_roles(1)
def admin_get_logs():
    logs = upload_helper.get_logs(mod.name)
    return jsonify(logs=logs)


@mod.route('/admin/logs/zip/<date>', methods=['GET'])
@login_required
@required_roles(1)
def admin_zip_logs(date):
    zipfile = upload_helper.zip_logs(mod.name)
    if zipfile:
        response = send_file(zipfile['location'], attachment_filename=zipfile['name'], as_attachment=True)
        if os.path.isfile(zipfile['location']):
            os.remove(zipfile['location'])
        return response
    flash('Não foi possível baixar o arquivo.', 'danger')
    return redirect(url_for('scholar.admin'))


@mod.route('/admin', methods=['POST'])
@login_required
@required_roles(1)
def admin_update():
    for id, approval_status in request.form.iteritems():
        article = Article.query.filter_by(id=id).first_or_404()
        article.approval_status = approval_status == u'true'
        db.session.commit()
    message = u"Estudo(s) atualizados com sucesso!"
    return message


@mod.route('/admin/article/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        article = Article.query.filter_by(id=id).first_or_404()
        setattr(article, status, status_value == u'true')
        db.session.commit()

    message = u"Artigo(s) alterada(s) com sucesso!"
    return message, 200


def new_article_advise(article, server_domain):
    article_url = server_domain + g.locale + '/' + mod.name + '/article/' + str(article.id)
    advise_message = render_template('scholar/mail/new_article_advise.html', article=article, article_url=article_url, language=(get_locale()))
    send_mail("Novo Estudo", [admin_email], advise_message)


def approved_articles_keywords():
    keywords_query = KeyWord.query.order_by(KeyWord.name).all()
    keywords = []

    for keyword_query in keywords_query:
        for row in keyword_query.articles:
            if row.approval_status is True:
                keywords.append(keyword_query)
                break

    return keywords


@mod.route('/admin/article/new', methods=['GET'])
@login_required
def new():
    form = RegistrationForm()
    form.set_choices(approved_articles_keywords())
    return render_template('scholar/new.html', form=form, action=url_for('scholar.create'))


@mod.route('/admin/article/new', methods=['POST'])
@login_required
def create():
    csrf_token = request.form.get('csrf_token')
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')

    form = RegistrationForm()

    if not os.path.exists(upload_folder):
        flash(u'Selecione o arquivo do artigo para enviá-lo.', 'danger')
        return render_template('scholar/new.html', form=form)

    if form.validate() is False:
        form.set_choices(approved_articles_keywords())
        return render_template('scholar/new.html', form=form)
    else:
        article = Article()
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article.approval_status = 0
        author_input_list = form.authors.data.replace(', ', ',').split(',')
        article.postage_img = form.thumb.data
        for author_input in author_input_list:
            article.authors.append(AuthorScholar(author_input))

        for keyword_input in form.keywords.data:
            keyword = KeyWord.query.filter_by(name=keyword_input).first()
            if not keyword:
                article.keywords.append(KeyWord(keyword_input))
            else:
                article.keywords.append(keyword)

        db.session.add(article)
        db.session.flush()

        if os.path.exists(upload_folder):

            file_name = [file for file in os.listdir(upload_folder)][0]

            article.file_url = upload_helper.upload_s3_file(
                os.path.join(upload_folder, file_name),
                os.path.join('scholar/', str(article.id), 'files/', 'article'),
                {
                    'ContentType': "application/pdf",
                    'ContentDisposition': 'attachment; filename=dataviva-article-' + str(article.id) + '.pdf'
                }
            )

            shutil.rmtree(os.path.split(upload_folder)[0])

        db.session.commit()
        upload_helper.log_operation(module=mod.name, operation='create', user=(g.user.id, g.user.email), objs=[(article.id, article.title)])
        new_article_advise(article, request.url_root)
        message = dictionary()["article_submission"]
        flash(message, 'success')
        return redirect(url_for('scholar.index'))


@mod.route('/admin/article/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    article = Article.query.filter_by(id=id).first_or_404()
    form = RegistrationForm()
    form.keywords.choices = ([(keyword.name, keyword.name) for keyword in article.keywords])
    form.set_choices(approved_articles_keywords())
    form.title.data = article.title
    form.theme.data = article.theme
    form.authors.data = article.authors_str()
    form.keywords.data = [keyword.name for keyword in article.keywords]
    form.abstract.data = article.abstract
    article_url = article.file_url

    return render_template('scholar/edit.html', form=form, action=url_for('scholar.update', id=id), article_url=article_url)


@mod.route('/admin/article/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    csrf_token = request.form.get('csrf_token')
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')
    article = Article.query.filter_by(id=id).first_or_404()
    form = RegistrationForm()

    if form.validate() is False:
        form.set_choices(approved_articles_keywords())
        return render_template('scholar/edit.html', form=form)
    else:
        old_title = article.title
        article.title = form.title.data
        article.theme = form.theme.data
        article.abstract = form.abstract.data
        article.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article.authors = []
        article.keywords = []

        author_input_list = form.authors.data.replace(', ', ',').split(',')
        for author_input in author_input_list:
            article.authors.append(AuthorScholar(author_input))

        for keyword_input in form.keywords.data:
            keyword = KeyWord.query.filter_by(name=keyword_input).first()
            if not keyword:
                article.keywords.append(KeyWord(keyword_input))
            else:
                article.keywords.append(keyword)

        if os.path.exists(upload_folder):

            file_name = [file for file in os.listdir(upload_folder)][0]

            article.file_url = upload_helper.upload_s3_file(
                os.path.join(upload_folder, file_name),
                os.path.join('scholar/', str(article.id), 'files/', 'article'),
                {
                    'ContentType': "application/pdf",
                    'ContentDisposition': 'attachment; filename=dataviva-article-' + str(article.id) + '.pdf'
                }
            )

            shutil.rmtree(os.path.split(upload_folder)[0])

        db.session.commit()
        upload_helper.log_operation(module=mod.name, operation='edit', user=(g.user.id, g.user.email), objs=[(article.id, old_title)])
        message = u'Estudo editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('scholar.admin'))


@mod.route('/admin/article/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    keywords = KeyWord.query.all()
    deleted_articles = []

    if ids:
        articles = Article.query.filter(Article.id.in_(ids)).all()
        for article in articles:
            upload_helper.delete_s3_folder(os.path.join(mod.name, str(article.id)))
            db.session.delete(article)
            db.session.flush()
            deleted_articles.append((article.id, article.title))

            for keyword in keywords:
                if keyword.articles.count() == 0:
                    db.session.delete(keyword)

        db.session.commit()
        upload_helper.log_operation(module=mod.name, operation='delete', user=(g.user.id, g.user.email), objs=deleted_articles)
        return u"Artigo(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum artigo para excluí-lo.', 205


@mod.route('/admin/articles/all', methods=['GET'])
@login_required
@required_roles(1)
def all():
    result = Article.query.all()
    articles = []
    for row in result:
        articles += [(row.id, row.title, row.authors_str(),
                      row.postage_date.strftime('%d/%m/%Y'), row.approval_status)]
    return jsonify(articles=articles)


@mod.route('/admin/article/upload', methods=['POST'])
@login_required
def upload():

    csrf_token = request.values['csrf_token']

    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')

    if os.path.exists(upload_folder):
        if [file for file in os.listdir(upload_folder)][0]:
            file_name = [file for file in os.listdir(upload_folder)][0]
            os.remove(os.path.join(upload_folder, file_name))
    else:
        os.makedirs(upload_folder)

    if request.files:
        file_name = request.files.keys()[0]
        file = request.files[file_name]
        file.save(os.path.join(upload_folder, file_name))
        return 'Arquivo salvo com sucesso!', 200
    else:
        return 'Não foi possível salvar o arquivo devido a um erro no servidor.', 400


@mod.route('/admin/article/delete', methods=['DELETE'])
@login_required
def delete():
    csrf_token = request.data
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')
    
    if os.path.exists(upload_folder):
        try:
            shutil.rmtree(os.path.split(upload_folder)[0])
            return 'Arquivo removido com sucesso!', 200
        except:
            return 'Não foi possível remover o arquivo devido a um erro no servidor.', 400


# serve static files on server
@mod.route('/admin/file/<string:csrf_token1>/<string:csrf_token2>', methods=['GET'])
@login_required
def get_file(csrf_token1, csrf_token2):
    csrf_token = csrf_token1 + '##' + csrf_token2
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, csrf_token, 'files')
    file_name = [file for file in os.listdir(upload_folder)][0]
    return send_from_directory(upload_folder, file_name)


# show static files on server before send to s3
@mod.route('/admin/data', methods=['GET'])
@login_required
@required_roles(1)
def data():
    matches = []
    for root, dirnames, filenames in os.walk(os.path.join(app.config['UPLOAD_FOLDER'], mod.name)):
        for filename in fnmatch.filter(filenames, '*.pdf'):
            matches.append(filename)
    return jsonify(file_names=matches)
