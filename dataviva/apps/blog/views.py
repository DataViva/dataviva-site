# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale
from flask.ext.login import login_required
from sqlalchemy import desc
from models import Post, Subject
from dataviva import db
from forms import RegistrationForm
from datetime import datetime
from random import randrange
from dataviva.apps.admin.views import required_roles
from dataviva import app
from dataviva.utils.upload_helper import save_b64_image, delete_s3_folder, upload_images_to_s3, save_file_temp, clean_s3_folder
from flask_paginate import Pagination
from config import ITEMS_PER_PAGE, BOOTSTRAP_VERSION
import os

mod = Blueprint('blog', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/blog')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def active_posts_subjects(language):
    subjects_query = Subject.query.filter_by(
        language=language).order_by(Subject.name).all()
    subjects = []
    for subject_query in subjects_query:
        for row in subject_query.posts:
            if row.active is True:
                subjects.append(subject_query)
                break
    return subjects


def add_subjects(post, subjects_input, language):
    for subject_input in subjects_input:
        subject = Subject.query.filter_by(
            name=subject_input).first()
        if not subject:
            post.subjects.append(Subject(subject_input, language))
        else:
            post.subjects.append(subject)


@mod.route('/', methods=['GET'])
@mod.route('/<int:page>', methods=['GET'])
def index(page=1):
    posts_query = Post.query.filter_by(active=True)
    posts = []

    subject = request.args.get('subject')
    if subject:
        posts = posts_query.filter(Post.subjects.any(Subject.id == subject)).order_by(desc(Post.publish_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_posts = posts_query.filter(Post.subjects.any(Subject.id == subject)).count()
    else:
        posts = posts_query.order_by(desc(Post.publish_date)).paginate(page, ITEMS_PER_PAGE, True).items
        num_posts = posts_query.count()


    pagination = Pagination(page=page,
                            total=num_posts,
                            per_page=ITEMS_PER_PAGE,
                            bs_version=BOOTSTRAP_VERSION)

    return render_template('blog/index.html',
                            posts=posts,
                            subjects=active_posts_subjects(g.locale),
                            pagination=pagination)


@mod.route('/post/<id>', methods=['GET'])
def show(id):
    post = Post.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter(Post.id != id, Post.active).all()

    if len(posts) > 3:
        read_more = [posts.pop(randrange(len(posts))) for _ in range(3)]
    else:
        read_more = posts
    return render_template('blog/show.html',
                           post=post,
                           subjects=active_posts_subjects(g.locale),
                           id=id,
                           read_more=read_more)


@mod.route('/post/all', methods=['GET'])
def all_posts():
    result = Post.query.all()
    posts = []
    for row in result:
        posts += [(row.id, row.title_pt, row.author,
                   row.publish_date.strftime('%d/%m/%Y'),
                   row.show_home, row.active)]
    return jsonify(posts=posts)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    posts = Post.query.all()
    return render_template('blog/admin.html', posts=posts)


@mod.route('/admin/post/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        post = Post.query.filter_by(id=id).first_or_404()
        setattr(post, status, status_value == u'true')
        db.session.commit()

    message = u"Post(s) alterado(s) com sucesso!"
    return message, 200


@mod.route('/admin/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    subjects = Subject.query.all()

    if ids:
        posts = Post.query.filter(Post.id.in_(ids)).all()
        for post in posts:
            try:
                delete_s3_folder(os.path.join(mod.name, str(post.id)))
            except Exception:
                pass
            db.session.delete(post)
            db.session.flush()

            for subject in subjects:
                if subject.posts.count() == 0:
                    db.session.delete(subject)

        db.session.commit()
        return u"Post(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum post para excluí-lo.', 205


@mod.route('/admin/post/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    form.subject_pt.choices = [(subject.name, subject.name)
                               for subject in active_posts_subjects('pt')]
    form.subject_en.choices = [(subject.name, subject.name)
                               for subject in active_posts_subjects('en')]

    return render_template('blog/new.html',
                           form=form, action=url_for('blog.create'))


@mod.route('/admin/post/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('blog/new.html', form=form)
    else:
        post = Post()
        post.title_pt = form.title_pt.data
        post.title_en = form.title_en.data
        post.author = form.author.data
        post.text_call_pt = form.text_call_pt.data
        post.text_call_en = form.text_call_en.data
        post.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        post.show_home = form.show_home.data
        post.dual_language = form.dual_language.data
        post.active = 0

        add_subjects(post, form.subject_pt.data, 'pt')
        if form.dual_language.data:
            add_subjects(post, form.subject_en.data, 'en')

        db.session.add(post)
        db.session.flush()

        text_content_pt = upload_images_to_s3(
            form.text_content_pt.data, mod.name, post.id)
        text_content_en = upload_images_to_s3(
            form.text_content_en.data, mod.name, post.id)
        Post.query.get(post.id).text_content_pt = text_content_pt
        Post.query.get(post.id).text_content_en = text_content_en
        clean_s3_folder(text_content_en, text_content_pt, mod.name, post.id)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], mod.name, str(post.id), 'images')
            post.thumb = save_b64_image(
                form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()

        message = u'Muito obrigado! Seu post foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))


@mod.route('/admin/upload', methods=['POST'])
@login_required
@required_roles(1)
def upload_image():
    file = request.files['image']
    csrf_token = request.form['csrf_token'].replace('#', '')
    image_url = save_file_temp(file, mod.name, csrf_token)
    return jsonify(image={'url': image_url})


@mod.route('/admin/post/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    form = RegistrationForm()
    form.subject_pt.choices = [(subject.name, subject.name)
                               for subject in active_posts_subjects('pt')]
    form.subject_en.choices = [(subject.name, subject.name)
                               for subject in active_posts_subjects('en')]

    post = Post.query.filter_by(id=id).first_or_404()
    form.title_pt.data = post.title_pt
    form.title_en.data = post.title_en
    form.author.data = post.author
    form.text_content_pt.data = post.text_content_pt
    form.text_content_en.data = post.text_content_en
    form.text_call_pt.data = post.text_call_pt
    form.text_call_en.data = post.text_call_en
    form.show_home.data = post.show_home
    form.dual_language.data = post.dual_language
    form.thumb.data = post.thumb
    form.publish_date.data = post.publish_date
    form.subject_pt.data = [subject.name for subject in post.subjects]
    form.subject_en.data = [subject.name for subject in post.subjects]

    return render_template('blog/edit.html',
                           form=form,
                           action=url_for('blog.update', id=id))


@mod.route('/admin/post/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('blog/edit.html', form=form)
    else:
        post = Post.query.filter_by(id=id).first_or_404()
        post.title_pt = form.title_pt.data
        post.title_en = form.title_en.data
        post.author = form.author.data
        post.text_call_pt = form.text_call_pt.data
        post.text_call_en = form.text_call_en.data
        post.last_modification = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        post.show_home = form.show_home.data
        post.dual_language = form.dual_language.data

        num_subjects = len(post.subjects)
        for i in range(0, num_subjects):
            post.subjects.remove(post.subjects[0])

        add_subjects(post, form.subject_pt.data, 'pt')
        if form.dual_language.data:
            add_subjects(post, form.subject_en.data, 'en')

        post.text_content_pt = upload_images_to_s3(
            form.text_content_pt.data, mod.name, post.id)
        post.text_content_en = upload_images_to_s3(
            form.text_content_en.data, mod.name, post.id)
        clean_s3_folder(post.text_content_pt, post.text_content_en, mod.name, post.id)

        db.session.flush()
        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(
                app.config['UPLOAD_FOLDER'], mod.name, str(post.id), 'images')
            post.thumb = save_b64_image(
                form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()

        message = u'Post editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))
