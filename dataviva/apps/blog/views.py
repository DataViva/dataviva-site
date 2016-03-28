# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

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
    posts = Post.query.filter_by(active=True).all()
    return render_template('blog/index.html', posts=posts)


@mod.route('/post/<id>', methods=['GET'])
def show(id):
    post = Post.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter(Post.id != id).all()
    if len(posts) > 3:
        read_more_posts = [posts.pop(randrange(len(posts))) for _ in range(3)]
    else:
        read_more_posts = posts
    return render_template('blog/show.html', post=post, id=id, read_more_posts=read_more_posts)


@mod.route('/post/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('blog/new.html', form=form, action=url_for('blog.create'))


@mod.route('/post/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    post = Post.query.filter_by(id=id).first_or_404()
    form.title.data = post.title
    form.authors.data = post.authors_str()
    form.subject.data = post.subject
    form.text_content.data = post.text_content
    form.text_call.data = post.text_call
    form.image.data = post.image
    form.thumb.data = post.thumb
    return render_template('blog/edit.html', form=form, action=url_for('blog.update', id=id))


@mod.route('/post/new', methods=['POST'])
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
        post.image = form.image.data
        post.thumb = form.thumb.data
        post.active = 0

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorBlog(author_input))

        db.session.add(post)
        db.session.commit()

        message = u'Muito obrigado! Seu post foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.index'))


@mod.route('/post/<id>/edit', methods=['POST'])
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
        post.image = form.image.data
        post.thumb = form.thumb.data
        post.authors = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorBlog(author_input))

        db.session.commit()

        message = u'Post editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.index'))


@mod.route('/post/<id>/delete', methods=['GET'])
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post:
        db.session.delete(post)
        db.session.commit()
        message = u"Post excluído com sucesso!"
        flash(message, 'success')
        return redirect(url_for('blog.index'))
    else:
        return make_response(render_template('not_found.html'), 404)


@mod.route('/approval', methods=['GET'])
def approval():
    posts = Post.query.all()
    return render_template('blog/approval.html', posts=posts)


@mod.route('/approval', methods=['POST'])
def approval_update():
    for id, active in request.form.iteritems():
        post = Post.query.filter_by(id=id).first_or_404()
        post.active = active == u'true'
        db.session.commit()
    message = u"Post(s) atualizados com sucesso!"
    return message


@mod.route('/all', methods=['GET'])
def all():
    result = Post.query.all()
    posts = []
    for row in result:
        posts += [(row.id, row.title, row.authors_str(), row.postage_date.strftime('%d/%m/%Y'), row.active)]
    return jsonify(posts=posts)
