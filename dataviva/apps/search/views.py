# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

from models import SearchQuestion, SearchSelector, SearchProfile
from dataviva import db
from forms import RegistrationForm


mod = Blueprint('search', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/search')


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
    return redirect(url_for('search.admin'))


@mod.route('/selector/all', methods=['GET'])
def all_selectors():
    result = SearchSelector.query.all()
    selectors = []

    for row in result:
        selectors += [(row.id, row.name())]

    return jsonify(selectors=selectors)


@mod.route('/question/all', methods=['GET'])
def all_questions():
    questions_query = SearchQuestion.query.all()
    questions = []

    for row in questions_query:
        questions += [(
            row.id,
            SearchProfile.query.filter_by(id=row.profile_id).first_or_404().name(),
            row.description(),
            row.selectors,
            row.answer
        )]
        
    return jsonify(questions=questions)


@mod.route('/profile/<id>', methods=['GET'])
def profile_questions(id):
    profile = SearchProfile.query.filter_by(id=id).first_or_404().name()

    questions = {}
    questions_query = SearchQuestion.query.filter_by(profile_id=id)
    for row in questions_query.all():

        selectors = sorted(row.selectors, key=lambda x: x.order, reverse=False)

        questions[row.id] = {
            'description': row.description(),
            'selectors': [rl.selector.id for rl in selectors],
            'answer': row.answer
        }

    return jsonify(
        questions=questions,
        profile=profile,
        template=render_template('search/modal.html'))


@mod.route('/admin', methods=['GET'])
def admin():
    questions = SearchQuestion.query.all()
    return render_template('search/admin.html', questions=questions)


@mod.route('/admin/question/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('search/new.html', form=form, action=url_for('search.create'))


@mod.route('/admin/question/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('search/new.html', form=form)
    else:
        question = SearchQuestion()
        question.profile_id = form.profile.data
        question.description_en = form.description_en.data
        question.description_pt = form.description_pt.data
        question.answer = form.answer.data

        db.session.add(question)
        db.session.flush()

        selector_input_list = form.selector.data.split(',')
        for selector_input in selector_input_list:
            import pdb; pdb.set_trace()
            question.selectors.append(int(question.id), selector_input)

        db.session.add(question)
        db.session.commit()

        message = u'Muito obrigado! Sua pergunta foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('search.admin'))


@mod.route('/admin/question/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    question = SearchQuestion.query.filter_by(id=id).first_or_404()
    form.profile.data = question.profile_id
    form.description_en.data = question.description_en
    form.description_pt.data = question.description_pt
    form.answer.data = question.answer
    form.selector.data = ', '.join((question.selectors).split(','))
    return render_template('search/edit.html', form=form, action=url_for('search.update', id=id))


@mod.route('admin/question/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('search/edit.html', form=form)
    else:
        question = SearchQuestion.query.filter_by(id=id).first_or_404()
        profile_id = form.profile.data
        question.profile_id = profile_id
        question.description_en = form.description_en.data
        question.description_pt = form.description_pt.data
        question.answer = form.answer.data
        question.selectors = []

        selector_input_list = form.selector.data.split(',')
        for selector_input in selector_input_list:
            question.selectors.append(SearchSelector(selector_input))

        db.session.commit()

        message = u'Pergunta editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('search.admin'))


@mod.route('/admin/delete', methods=['POST'])
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        questions = SearchQuestion.query.filter(SearchQuestion.id.in_(ids)).all()
        for question in questions:
            db.session.delete(question)

        db.session.commit()
        return u"Pergunta(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma pergunta para excluí-la.', 205
