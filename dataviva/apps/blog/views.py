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
from dataviva.utils.upload_helper import save_b64_image, delete_s3_folder
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


@mod.route('/', methods=['GET'])
def index():
    posts_query = db.session.query(Post).filter(Post.active==True).order_by(desc(Post.postage_date))
    subjects_query = db.session.query(Subject).order_by(desc(Subject.name))
    posts = []
    subjects = []

    for subject_query in subjects_query:
        if len(subject_query.posts)  > 0:
            subjects.append(subject_query)

    for post_query in posts_query:
        post = {}
        post['id'] = post_query.id
        post['title'] = post_query.title 
        post['author'] = post_query.author 
        post['text_call'] = post_query.text_call 
        post['text_content'] = post_query.text_content 
        post['thumb'] = post_query.thumb 
        post['postage_date'] = post_query.postage_date 
        post['active'] = post_query.active
        post['date_str'] = post_query.date_str()
        post['subjects'] = str(post_query.subjects[0].name)
        for index in range( 1, len(post_query.subjects)):
            post['subjects'] += '-' + str(post_query.subjects[index].name)
        posts.append(post)

    return render_template('blog/index.html', posts=posts, subjects=subjects)



@mod.route('/<subject>', methods=['GET'])
def index_subject(subject):
    posts_query = db.session.query(Post).filter(Post.active==True).order_by(desc(Post.postage_date))
    subjects_query = db.session.query(Subject).order_by(desc(Subject.name))
    posts = []
    subjects = []

    for subject_query in subjects_query:
        if len(subject_query.posts)  > 0:
            subjects.append(subject_query)

    for post in posts_query:
        if float(subject) in [x.id for x in post.subjects]:
            posts.append(post)
    
    return render_template('blog/index.html', posts=posts, subjects=subjects, active_subject=long(subject))


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
    result = db.session.query(Post)
    posts = []
    for row in result:
        posts += [(row.id, row.title, row.author,
                   row.postage_date.strftime('%d/%m/%Y'), row.active)]

    return jsonify(posts=posts)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    posts = db.session.query(Post)
    return render_template('blog/admin.html', posts=posts)


@mod.route('/admin/post/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        post = db.session.query(Post).filter(Post.id==id)
        setattr(post, status, status_value == u'true')
        db.session.commit()

    message = u"Post(s) alterado(s) com sucesso!"
    return message, 200


@mod.route('/admin/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        posts = Post.query.filter(Post.id.in_(ids)).all()
        for post in posts:
            # deletar subjets inuteis ? 
            posts_subject_list = PostSubject.query.filter_by(id_post = post.id ).all();
            for post_subject in posts_subject_list:
                db.session.delete(post_subject)

            delete_s3_folder(os.path.join(mod.name, str(post.id)))
            db.session.delete(post)

        db.session.commit()
        return u"Post(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum post para excluí-lo.', 205


@mod.route('/admin/post/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    return render_template('blog/new.html', form=form, action=url_for('blog.create'))


@mod.route('/admin/post/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('blog/new.html', form=form)
    else:
        post = Post()
        post.title = form.title.data
        subjects = form.subject.data.replace(', ', ',').split(',')
        
        #add subjecs that not exist
        for subject_name in subjects :         
            subject_query = Subject.query.filter_by(name=subject_name)
            if (not subject_query.first()):
                new_subject = Subject()
                new_subject.name = subject_name
                db.session.add(new_subject)
                db.session.flush()

        post.author = form.author.data
        post.text_content = form.text_content.data
        post.text_call = form.text_call.data
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post.active = 0
        #temporario , tirar no banco
        post.subject_id = 1

        db.session.add(post)
        db.session.flush()
        
        #add relationship nxn
        for subject_name in subjects:
            subject = Subject.query.filter_by(name=subject_name).first_or_404()

            post_subject = PostSubject();
            post_subject.id_post = post.id
            post_subject.id_subject = subject.id
            db.session.add(post_subject)
        
        db.session.commit()

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, str(post.id), 'images')
            post.thumb = save_b64_image(form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()

        message = u'Muito obrigado! Seu post foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))


@mod.route('/admin/post/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    form = RegistrationForm()
    post = Post.query.filter_by(id=id).first_or_404()
    form.title.data = post.title
    form.author.data = post.author
    form.text_content.data = post.text_content
    form.text_call.data = post.text_call
    form.thumb.data = post.thumb

    subjects = Subject.query.all()
    subjects_dict = {}
    for row in subjects:
        subjects_dict[row.id] = row.name
    post_subject_list = PostSubject.query.filter_by(id_post=post.id).all()
    subject_names = ', '.join([ subjects_dict[x.id_subject] for x in post_subject_list ])
    
    form.subject.data = subject_names


    return render_template('blog/edit.html', form=form, action=url_for('blog.update', id=id))


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
        post.title = form.title.data
        subjects = form.subject.data.replace(', ', ',').split(',')
        
        #add subjecs that not exist
        for subject_name in subjects :         
            subject_query = Subject.query.filter_by(name=subject_name)
            if (not subject_query.first()):
                new_subject = Subject()
                new_subject.name = subject_name
                db.session.add(new_subject)
                db.session.flush()


        #temporario , tirar no banco
        post.subject_id = 1
        post.author = form.author.data
        post.text_content = form.text_content.data
        post.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #remove old relationship
        posts_subject_list = PostSubject.query.filter_by(id_post = post.id ).all();
        for post_subject in posts_subject_list:
            db.session.delete(post_subject)


        #add new relationship nxn
        for subject_name in subjects:
            subject = Subject.query.filter_by(name=subject_name).first_or_404()
            post_subject_new = PostSubject();
            post_subject_new.id_post = post.id
            post_subject_new.id_subject = subject.id
            db.session.add(post_subject_new)

        if len(form.thumb.data.split(',')) > 1:
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], mod.name, str(post.id), 'images')
            post.thumb = save_b64_image(form.thumb.data.split(',')[1], upload_folder, 'thumb')

        db.session.commit()

        message = u'Post editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('blog.admin'))
