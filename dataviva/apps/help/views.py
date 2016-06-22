# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, url_for, flash, redirect, jsonify, request
from dataviva.apps.general.views import get_locale
from flask.ext.login import login_required
from dataviva.apps.admin.views import required_roles
from dataviva import db
from models import HelpSubject, HelpSubjectQuestion
from dataviva.apps.embed.models import Crosswalk_oc, Crosswalk_pi
from urlparse import urlparse
from forms import RegistrationForm


mod = Blueprint('help', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/help')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
    subjects = HelpSubject.query.all()
    return render_template('help/index.html', subjects=subjects)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    subjects = HelpSubject.query.all()
    return render_template('help/admin.html', subjects=subjects, lang=g.locale)


@mod.route('/admin/subject/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    form.subject_choices(lang=g.locale)
    return render_template('help/new.html', form=form, action=url_for('help.create'))


@mod.route('/admin/subject/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    form.subject_choices(lang=g.locale)
    if form.validate() is False:
        return render_template('help/new.html', form=form)
    else:
        subject = HelpSubjectQuestion()
        subject.subject_id = int(form.subject.data)
        subject.description_en = form.description_en.data
        subject.description_pt = form.description_pt.data
        subject.answer_en = form.answer_en.data
        subject.answer_pt = form.answer_pt.data
        subject.active = 0

        db.session.add(subject)
        db.session.commit()

        message = u'Muito obrigado! Sua pergunta foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('help.admin'))


@mod.route('/admin/subject/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    form = RegistrationForm()
    form.subject_choices(lang=g.locale)
    subject = HelpSubjectQuestion.query.filter_by(id=id).first_or_404()
    form.subject.data = str(subject.subject_id)
    form.description_en.data = subject.description_en
    form.description_pt.data = subject.description_pt
    form.answer_en.data = subject.answer_en
    form.answer_pt.data = subject.answer_pt
    return render_template('help/edit.html', form=form, action=url_for('help.update', id=id))


@mod.route('/admin/subject/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    form = RegistrationForm()
    form.subject_choices(lang=g.locale)
    if form.validate() is False:
        return render_template('help/new.html', form=form)
    else:
        subject = HelpSubjectQuestion.query.filter_by(id=id).first_or_404()
        subject.subject_id = int(form.subject.data)
        subject.description_en = form.description_en.data
        subject.description_pt = form.description_pt.data
        subject.answer_en = form.answer_en.data
        subject.answer_pt = form.answer_pt.data

        db.session.add(subject)
        db.session.commit()

        message = u'Pergunta editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('help.admin'))


@mod.route('/admin/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        subjects = HelpSubjectQuestion.query.filter(HelpSubjectQuestion.id.in_(ids)).all()
        for subject in subjects:
            db.session.delete(subject)

        db.session.commit()
        return u"Pergunta(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma pergunta para excluí-la.', 205


@mod.route('/admin/subject/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        subject = HelpSubjectQuestion.query.filter_by(id=id).first_or_404()
        setattr(subject, status, status_value == u'true')
        db.session.commit()

    message = u"Perguntas(s) alterada(s) com sucesso!"
    return message, 200


@mod.route('/subject/all', methods=['GET'])
def all_posts():
    result = HelpSubjectQuestion.query.all()
    subjects = []
    for row in result:
            subjects += [(row.id, row.subject.name(), row.description(), row.answer(), row.active)]
    return jsonify(subjects=subjects)


@mod.route('/crosswalk/pi')
@mod.route('/crosswalk/ip')
@mod.route('/crosswalk/oc')
@mod.route('/crosswalk/co')
def crosswalk():
    url = urlparse(request.url)
    crosswalk_table = url.path.split('/')[-1]

    data = []

    if crosswalk_table == 'pi' or crosswalk_table == 'ip':
        result = Crosswalk_pi.query.all()
        if crosswalk_table == 'pi':
            for row in result:
                data += [(row.hs_id, row.cnae_id)]
        else:
            for row in result:
                data += [(row.cnae_id, row.hs_id)]
    else:
        result = Crosswalk_oc.query.all()
        if crosswalk_table == 'oc':
            for row in result:
                data += [(row.cbo_id, row.course_hedu_id)]
        else:
            for row in result:
                data += [(row.course_hedu_id, row.cbo_id)]

    aggregated_data = []
    row_index = 0
    data.sort() 
    while row_index < (len(data)):
        category = data[row_index][0]
        crossings = [data[row_index][1]]
        
        if row_index == len(data)-1:
            aggregated_data += [(category, crossings)];
            break;
            
        while category == data[row_index+1][0]:
            crossings.append(data[row_index+1][1])
            row_index += 1

            if row_index == len(data)-1: 
                break;

        aggregated_data += [(category, crossings)];
        row_index += 1
        
    return jsonify(data=aggregated_data)
