from sqlalchemy import and_, or_, func
from datetime import datetime
from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from flask.ext.babel import gettext
from dataviva import db, lm, view_cache
# from config import SITE_MIRROR

from dataviva.apps.account.models import User
from dataviva.apps.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.apps.ask.forms import AskForm, ReplyForm, SearchForm

from dataviva.utils.cached_query import cached_query, api_cache_key

import urllib2, urllib

mod = Blueprint('ask', __name__, url_prefix='/<lang_code>/ask')

RESULTS_PER_PAGE = 10

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.locale)

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

@mod.route('/questions/', methods=['GET', 'POST'], defaults={'page': 1})
def question_list(page):

    # get URL parameters for results per page and ordering options
    order = request.args.get('order', 'votes') # options = 'votes' or 'newest'
    type = request.args.get('type', 'all') # options = 'all' or 'question' or 'comment' or 'contact'
    offset = request.args.get('offset', 0)
    search_term = request.args.get('q', None)
    if search_term:
      search_term = search_term.encode('utf-8')
    limit = 25
    lang = request.args.get('lang', None) or g.locale

    # lets find the questions to load in the page
    # only the approved questions
    approved = Status.query.filter_by(name='Approved').first()
    questions = Question.query.filter_by(status = approved)

    # if the user has submitted a search, filter by that term
    if search_term:
        like_str = "%{0}%".format(search_term)
        questions = questions.filter(or_(Question.question.like(like_str),Question.body.like(like_str),Question.status_notes.like(like_str)))

    if type == "question":
        questions = questions.filter_by(type_id='1')
    elif type == "comment":
        questions = questions.filter_by(type_id='2')
    elif type == "contact":
        questions = questions.filter_by(type_id='3')

    # if we are ordering the questions by newest get them ordered chronologically
    if order == "newest":

        if g.locale == "pt":
            questions = questions.order_by(Question.timestamp.desc(),Question.language.desc())
        else:
            questions = questions.order_by(Question.timestamp.desc(),Question.language)

        questions = questions.order_by(Question.timestamp.desc())
        questions = questions.limit(limit).offset(offset)
        questions = [q.serialize() for q in questions.all()]

    # otherwise we are ordering the questions by votes
    else:
        questions = questions.limit(limit).offset(offset)
        ids = [q.id for q in questions]
        # raise Exception(ids)
        votes_subq = db.session.query(Vote, func.count('*').label('vote_count')).group_by(Vote.type_id).subquery()

        if lang == "pt":
            questions = db.session.query(Question, votes_subq.c.vote_count) \
                .outerjoin(votes_subq, and_(Question.id==votes_subq.c.type_id, votes_subq.c.type==TYPE_QUESTION)) \
                .filter(Question.status == approved) \
                .filter(Question.id.in_(ids)) \
                .filter(Question.language==lang) \
                .order_by(votes_subq.c.vote_count.desc(),Question.language.desc())
        else:
            questions = db.session.query(Question, votes_subq.c.vote_count) \
                .outerjoin(votes_subq, and_(Question.id==votes_subq.c.type_id, votes_subq.c.type==TYPE_QUESTION)) \
                .filter(Question.status == approved) \
                .filter(Question.id.in_(ids)) \
                .filter(Question.language==lang) \
                .order_by(votes_subq.c.vote_count.desc(),Question.language)
            # .limit(limit).offset(offset)

        questions = [q[0].serialize() for q in questions]

    ret = jsonify({"activities":questions})

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Expires', '-1')
    ret.headers.add('Cache-Control', 'must-revalidate, private')

    return ret

@mod.route('/question/<slug>/vote/')
@mod.route('/question/<slug>/vote/<user>/')
def question_vote(slug, user=None):

    q = Question.query.filter_by(slug=slug).first_or_404()
    if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
        g.user = User.query.get(user)
    elif g.user is None or not g.user.is_authenticated:
        return jsonify({"error": gettext("You need to be logged in to vote.")})
    elif user is None and g.user is None:
        abort(404)

    # if user is None:
    #     try:
    #         opener = urllib2.urlopen("{0}ask/question/{1}/vote/{2}/".format(SITE_MIRROR,slug,g.user.id),None,5)
    #     except:
    #         return jsonify({"error": gettext("The server is not responding. Please try again later.")})

    vote = q.votes.filter_by(user=g.user).first()
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return jsonify({"success": -1})
    else:
        new_vote = Vote(user=g.user, type=TYPE_QUESTION, type_id=q.id)
        db.session.add(new_vote)
        db.session.commit()
        return jsonify({"success": 1})

@mod.route('/reply/<int:id>/vote/')
@mod.route('/reply/<int:id>/vote/<user>/')
def reply_vote(id, user=None):
    reply = Reply.query.get_or_404(id)
    # if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
    #     g.user = User.query.get(user)
    if g.user is None or not g.user.is_authenticated:
        return jsonify({"error": gettext("You need to be logged in to vote.")})
    # elif user is None and g.user is None:
    #     abort(404)

    # if user is None:
    #     try:
    #         opener = urllib2.urlopen("{0}ask/reply/{1}/vote/{2}/".format(SITE_MIRROR,id,g.user.id),None,5)
    #     except:
    #         return jsonify({"error": gettext("The server is not responding. Please try again later.")})

    vote = reply.votes.filter_by(user=g.user).first()
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return jsonify({"success": -1})
    else:
        new_vote = Vote(user=g.user, type=TYPE_REPLY, type_id=reply.id)
        db.session.add(new_vote)
        db.session.commit()
        return jsonify({"success": 1})

@mod.route('/reply/<int:id>/flag/')
@mod.route('/reply/<int:id>/flag/<user>/')
def reply_flag(id, user=None):

    reply = Reply.query.get_or_404(id)

    # if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
    #     g.user = User.query.get(user)
    if g.user is None or not g.user.is_authenticated:
        return jsonify({"error": gettext("You need to be logged in to flag replies.")})
    # elif user is None and g.user is None:
    #     abort(404)

    # if user is None:
    #     try:
    #         opener = urllib2.urlopen("{0}ask/reply/{1}/flag/{2}/".format(SITE_MIRROR,id,g.user.id),None,5)
    #     except:
    #         return jsonify({"error": gettext("The server is not responding. Please try again later.")})

    flag = reply.flags.filter_by(user=g.user).first()
    if flag:
        db.session.delete(flag)
        db.session.commit()
        return jsonify({"success": -1})
    else:
        new_flag = Flag(user=g.user, reply_id=reply.id)
        db.session.add(new_flag)
        db.session.commit()
        return jsonify({"success": 1})
