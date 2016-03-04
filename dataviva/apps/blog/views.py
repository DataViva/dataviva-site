# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from mock import posts

import random

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
    while len(read_more_posts) < 3:
        post_id = random.choice(posts.keys())
        if read_more_posts.has_key(post_id) is False and post_id != id:
            read_more_posts.update({post_id: posts[post_id]})

    return render_template('blog/show.html', post=post, id=id, read_more_posts=read_more_posts)


@mod.route('/post/new', methods=['GET'])
def new():
    return render_template('blog/new.html')


@mod.route('/post/<id>/edit', methods=['GET'])
def edit():
    return render_template('blog/edit.html')


@mod.route('/post', methods=['POST'])
def create():
    pass


@mod.route('/post/<id>', methods=['POST'])
def update():
    pass


@mod.route('/post/<id>', methods=['GET'])
def destroy():
    pass
