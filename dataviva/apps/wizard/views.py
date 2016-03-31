# -*- coding: utf-8 -*-
from flask import Blueprint, g, jsonify, request, render_template
from dataviva.apps.wizard.sessions import SESSIONS
from dataviva.apps.general.views import get_locale

mod = Blueprint('wizard', __name__, url_prefix='/<lang_code>/wizard')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/session/<session_name>', methods=['GET'])
def session(session_name):
    session_obj = SESSIONS.get(session_name, False)

    return jsonify({
        "session_name": session_name,
        "session_title": session_obj.session_title,
        "title": session_obj.title,
        "questions": map(lambda x: x.serialize, session_obj.questions),
    })


@mod.route('/submit_answer/', methods=['POST'])
def submit_answer():

    rjson = request.get_json()
    session_name = rjson["session_name"]
    path_option = rjson.get("path_option", None)
    selector_choices = rjson.get("selector_choices", [])

    session = SESSIONS.get(session_name)
    resp = {
        "session_name": session_name,
        "path_option": path_option,
        "selectors": selector_choices,
        "current_step": None,
        "redirect_url": None
    }

    if path_option:
        path = None
        for op in session.questions:
            if op.id == path_option:
                path = op
                break

        if len(selector_choices) == len(path.selectors):
            resp["current_step"] = {"title": ""}
            resp["redirect_url"] = path.redirect % (
                selector_choices[0], selector_choices[1])
        else:
            resp["current_step"] = path.selectors[len(selector_choices)]

    return jsonify(resp)


@mod.route('/location_selector/', methods=['GET'])
def location_selector():
    return render_template("selectors/location.html")


@mod.route('/basic_course_selector/', methods=['GET'])
def basic_course():
    return render_template("selectors/basic_course.html")


@mod.route('/product_selector/', methods=['GET'])
def product_selector():
    return render_template("selectors/product.html")


@mod.route('/major_selector/', methods=['GET'])
def major_selector():
    return render_template("selectors/major.html")


@mod.route('/industry_selector/', methods=['GET'])
def industry_selector():
    return render_template("selectors/industry.html")


@mod.route('/university_selector/', methods=['GET'])
def university_selector():
    return render_template("selectors/university.html")


@mod.route('/occupation_selector/', methods=['GET'])
def occupation_selector():
    return render_template("selectors/occupation.html")


@mod.route('/trade_partner_selector/', methods=['GET'])
def trade_partner_selector():
    return render_template("selectors/trade_partner.html")
