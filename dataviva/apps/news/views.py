# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, redirect, url_for, flash
from dataviva.apps.general.views import get_locale

from models import Post, AuthorNews
from dataviva import db
from forms import RegistrationForm
from datetime import datetime
from random import randrange

mod = Blueprint('news', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/news')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('news/index.html', posts=posts)


@mod.route('/post/<id>', methods=['GET'])
def show(id):
    post = Post.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter(Post.id != id).all()
    if len(posts) > 3:
        read_more_posts = [posts.pop(randrange(len(posts))) for _ in range(3)]
    else:
        read_more_posts = posts
    return render_template('news/show.html', post=post, id=id, read_more_posts=read_more_posts)


@mod.route('/post/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('news/new.html', form=form, action=url_for('news.create'))


@mod.route('/post/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    post = Post.query.filter_by(id=id).first_or_404()
    form.title.data = post.title
    form.authors.data = post.authors_str()
    form.subject.data = post.subject
    form.text_content.data = post.text_content
    form.image_path.data = post.image_path
    form.thumb_path.data = post.thumb_path
    return render_template('news/edit.html', form=form, action=url_for('news.update', id=id))


@mod.route('/post/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('news/new.html', form=form)
    else:
        post = Post()
        post.title = form.title.data
        post.subject = form.subject.data
        post.text_content = form.text_content.data
        post.image_path = 'http://agenciatarrafa.com.br/2015/wp-content/uploads/2015/09/google-ads-1000x300.jpg'
        post.thumb_path = 'http://1un1ba2fg8v82k48vu4by3q7.wpengine.netdna-cdn.com/wp-content/uploads/2014/05/Mobile-Analytics-Picture-e1399568637490-350x227.jpg'
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorNews(author_input))

        db.session.add(post)
        db.session.commit()

        message = u'Muito obrigado! Seu post foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.index'))


@mod.route('/post/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('news/edit.html', form=form)
    else:
        post = Post.query.filter_by(id=id).first_or_404()
        post.title = form.title.data
        post.subject = form.subject.data
        post.text_content = form.text_content.data
        post.image_path = 'http://agenciatarrafa.com.br/2015/wp-content/uploads/2015/09/google-ads-1000x300.jpg'
        post.thumb_path = 'http://1un1ba2fg8v82k48vu4by3q7.wpengine.netdna-cdn.com/wp-content/uploads/2014/05/Mobile-Analytics-Picture-e1399568637490-350x227.jpg'
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.authors = []

        author_input_list = form.authors.data.split(',')
        for author_input in author_input_list:
            post.authors.append(AuthorNews(author_input))

        db.session.commit()

        message = u'Post editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('news.index'))


@mod.route('/post/<id>/delete', methods=['GET'])
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    if post:
        db.session.delete(post)
        db.session.commit()
        message = u"Post excluído com sucesso!"
        flash(message, 'success')
        return redirect(url_for('news.index'))
    else:
        return make_response(render_template('not_found.html'), 404)
