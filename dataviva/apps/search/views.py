# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

from models import SearchQuestion, SearchSelector
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
    pass


@mod.route('/question/all', methods=['GET'])
def all_questions():
    result = SearchQuestion.query.all()
    questions = []
    for row in result:
        questions += [(row.id, row.profile_id, row.description, row.selectors_str(), row.answer)]
    return jsonify(questions=questions)


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
        profile_id = form.profile.data
        #Id=1, profile=Entrepreneurs / Empreendedores
        #Id=2, profile=Development Agents / Agentes de Desenvolvimento
        #Id=3, profile=Students and Professionals / Estudantes e Profissionais
        profile_id = 1
        question.profile_id = profile_id
        question.description = form.description.data
        question.answer = form.answer.data

        selector_input_list = form.selector.data.split(',')
        for selector_input in selector_input_list:
            question.selectors.append(SearchSelector(selector_input))

        db.session.add(question)
        db.session.commit()

        message = u'Muito obrigado! Sua pesquisa foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('search.admin'))
