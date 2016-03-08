# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, url_for, flash
from dataviva.apps.general.views import get_locale
from forms import RegistrationForm
from mock import Post, posts, ids
import random, time

mod = Blueprint('blog', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/blog')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    return render_template('blog/index.html', posts=posts)


@mod.route('/post/<id>', methods=['GET'])
def show(id):
    id = int(id.encode())
    post = posts[id]

    read_more_posts = {}
    #loop if has less then 3 articles
    while len(read_more_posts) < 3:
        post_id = random.choice(posts.keys())
        if read_more_posts.has_key(post_id) is False and post_id != id:
            read_more_posts.update({post_id: posts[post_id]})

    return render_template('blog/show.html', post=post, id=id, read_more_posts=read_more_posts)


@mod.route('/post/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('blog/new.html', form=form, action=url_for('blog.create'))


@mod.route('/post/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    id = int(id.encode())
    post = posts[id]
    form.title.data = post.title
    form.author.data = post.author
    form.category.data = post.category
    form.text.data = post.text
    form.image.data = post.image
    form.thumb.data = post.thumb
    return render_template('blog/edit.html', form=form, action=url_for('blog.update', id=id))


@mod.route('/post/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('blog/new.html', form=form)
    else:
        title = form.title.data
        author = form.author.data
        category = form.category.data
        text = form.text.data
        image = 'image'
        thumb = 'thumb'
        postage_date = time.strftime("%d/%m/%Y")
        id = ids[-1] + 1

        ids.append(id)
        posts.update({id: Post(title, author, image, thumb, category, text, postage_date)})

        message = u'Muito obrigado! Seu artigo foi submetido com sucesso!'
        flash(message, 'success')
        return render_template('blog/index.html', posts=posts)


@mod.route('/post/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('blog/edit.html', form=form)
    else:
        title = form.title.data
        author = form.author.data
        category = form.category.data
        text = form.text.data
        image = 'image'
        thumb = 'thumb'
        postage_date = time.strftime("%d/%m/%Y")

        posts[id] = Post(title, author, category, text, image, thumb, postage_date)
        message = u'Artigo editado com sucesso!'
        flash(message, 'success')
        return render_template('blog/index.html', posts=posts)


@mod.route('/post/<id>/delete', methods=['GET'])
def delete(id):
    if posts.pop(int(id.encode())):
        message = u"Artigo excluído com sucesso!"
        flash(message, 'success')
        return render_template('blog/index.html', posts=posts)
    else:
        return make_response(render_template('not_found.html'), 404)
