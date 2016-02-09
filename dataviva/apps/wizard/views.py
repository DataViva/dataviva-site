# -*- coding: utf-8 -*-
from flask import Blueprint, g, jsonify, request, render_template
from dataviva.apps.wizard.questions_tree import SESSIONS

mod = Blueprint('wizard', __name__, url_prefix='/<lang_code>/wizard')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.route('/session/<session_name>', methods=['GET'])
def session(session_name):

    session_obj = SESSIONS.get(session_name, False)
    return jsonify({
        "session_name": session_name,
        "title": session_obj.title,
        "options": map(lambda x: x.serialize, session_obj.options)
    })


@mod.route('/submit_answer/', methods=['POST'])
def submit_answer():

    rjson = request.get_json()
    session_name = rjson["session_name"]
    path_option = rjson.get("path_option", None)
    selectors = rjson.get("selectors", [])

    session = SESSIONS.get(session_name)
    resp = {
        "session_name": session_name,
        "path_option": path_option,
        "selectors": selectors,
        "current_step": None
    }

    if path_option:
        path = None
        for op in session.options:
            if op.id == path_option:
                path = op
                break
        resp["current_step"] = path.selectors[len(selectors)]

    return jsonify(resp)


@mod.route('/location_selector/', methods=['GET'])
def location_selector():
    return render_template("selectors/location.html")


@mod.route('/product_selector/', methods=['GET'])
def product_selector():
    return render_template("selectors/product.html")
