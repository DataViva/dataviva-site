# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

from sqlalchemy import desc
from models import Post, AuthorBlog
from dataviva import db
from forms import RegistrationForm
from datetime import datetime
from random import randrange

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


@mod.route('/', methods=['GET'])
def index():
    posts = Post.query.filter_by(active=True).order_by(desc(Post.postage_date)).all()
    return render_template('blog/index.html', posts=posts)


@mod.route('/post/<id>', methods=['GET'])
def show(id):
    post = Post.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter(Post.id != id, Post.active).all()
    if len(posts) > 3:
        read_more = [posts.pop(randrange(len(posts))) for _ in range(3)]
    else:
        read_more = posts
    return render_template('blog/show.html', post=post, id=id, read_more=read_more)


@mod.route('/post/all', methods=['GET'])
def all_posts():
    result = Post.query.all()
    posts = []
    for row in result:
        posts += [(row.id, row.title, row.authors_str(),
                   row.postage_date.strftime('%d/%m/%Y'), row.active)]
    return jsonify(posts=posts)


@mod.route('/admin', methods=['GET'])
def admin():
    posts = Post.query.all()
    return render_template('blog/admin.html', posts=posts)


@mod.route('/admin/post/<status>/<status_value>', methods=['POST'])
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        post = Post.query.filter_by(id=id).first_or_404()
        setattr(post, status, status_value == u'true')
        db.session.commit()

    message = u"Post(s) alterado(s) com sucesso!"
    return message, 200


@mod.route('/admin/delete', methods=['POST'])
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        posts = Post.query.filter(Post.id.in_(ids)).all()
        for post in posts:
            db.session.delete(post)

        db.session.commit()
        return u"Post(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum post para excluí-lo.', 205


@mod.route('/admin/post/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('blog/new.html', form=form, action=url_for('blog.create'))


@mod.route('/admin/post/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('blog/new.html', form=form)
    else:
        post = Post()
        post.title = form.title.data
        post.subject = form.subject.data
        post.text_content = form.text_content.data
        post.text_call = form.text_call.data
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.thumb = form.thumb.data
        post.active = 0

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorBlog(author_input))

        db.session.add(post)
        db.session.commit()

        message = u'Muito obrigado! Seu post foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))


@mod.route('/admin/post/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    post = Post.query.filter_by(id=id).first_or_404()
    form.title.data = post.title
    form.authors.data = post.authors_str()
    form.subject.data = post.subject
    form.text_content.data = post.text_content
    form.text_call.data = post.text_call
    form.thumb.data = post.thumb
    return render_template('blog/edit.html', form=form, action=url_for('blog.update', id=id))


@mod.route('/admin/post/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('blog/edit.html', form=form)
    else:
        post = Post.query.filter_by(id=id).first_or_404()
        post.title = form.title.data
        post.subject = form.subject.data
        post.text_content = form.text_content.data
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.thumb = form.thumb.data
        post.authors = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorBlog(author_input))

        db.session.commit()

        message = u'Post editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))
