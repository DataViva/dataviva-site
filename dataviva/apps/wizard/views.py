# -*- coding: utf-8 -*-
from flask import Blueprint, g, jsonify, request
from dataviva.apps.wizard.questions_tree import (
    WizTree,
    get_next_step,
    get_step_options
)

mod = Blueprint('wizard', __name__, url_prefix='/<lang_code>/wizard')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.route('/start_session/<session_name>', methods=['GET'])
def start_session(session_name):
    wiz = WizTree.get(session_name, None)
    next_step = get_next_step(wiz, [])
    ns = {
        "title": next_step["title"],
        "options": get_step_options(next_step),
    }
    return jsonify({
        "session_name": session_name,
        "previous_answers": [],
        "current_step": ns,
    })


@mod.route('/submit_answer/', methods=['POST'])
def submit_answer():

    rjson = request.get_json()

    session_name = rjson["session_name"]
    prev = rjson.get("previous_answers", [])
    curr = rjson.get("current_answer", None)
    prev.append(curr)

    wiz = WizTree.get(session_name, None)
    next_step = get_next_step(wiz, prev)
    ns = {
        "title": next_step["title"],
        "options": get_step_options(next_step),
    }

    return jsonify({
        "session_name": session_name,
        "previous_answers": prev,
        "current_step": ns,
    })
