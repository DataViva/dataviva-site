from sqlalchemy import and_, func
from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from flask.ext.babel import gettext
from dataviva import db, lm
from config import SITE_MIRROR

from dataviva.account.models import User
from dataviva.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.ask.forms import AskForm, ReplyForm, SearchForm
from dataviva.utils import strip_html

import urllib2, urllib

mod = Blueprint('ask', __name__, url_prefix='/ask')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#742777"
    
    g.sabrina = {}
    g.sabrina["outfit"] = "lab"
    g.sabrina["face"] = "smirk"
    g.sabrina["hat"] = "glasses"

RESULTS_PER_PAGE = 10

@mod.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@mod.route('/questions/', methods=['GET', 'POST'], defaults={'page': 1})
@mod.route('/questions/<int:page>/', methods=['GET', 'POST'])
def index(page):
    # get URL parameters for results per page and ordering options
    order = request.args.get('order', 'votes') # options = 'votes' or 'newest'
    offset = request.args.get('offset', 0)
    search_term = request.args.get('q', None)
    limit = 25
    
    # load forms for submitting new question or for searching
    search_form = SearchForm()
    
    if request.is_xhr:
        # lets find the questions to load in the page
        # only the approved questions
        approved = Status.query.filter_by(name='Approved').first()
        questions = Question.query.filter_by(status = approved)

        # if the user has submitted a search, filter by that term
        if search_term:
            questions = questions.whoosh_search(search_term)

        # if we are ordering the questions by newest get them ordered chronologically
        if order == "newest":
            questions = questions.order_by(Question.timestamp.desc())
            questions = questions.limit(limit).offset(offset)
            questions = [q.serialize() for q in questions.all()]

        # otherwise we are ordering the questions by votes
        else:
            questions = questions.limit(limit).offset(offset)
            ids = [q.id for q in questions]
            # raise Exception(ids)
            votes_subq = db.session.query(Vote, func.count('*').label('vote_count')).group_by(Vote.type_id).subquery()
            questions = db.session.query(Question, votes_subq.c.vote_count) \
                .outerjoin(votes_subq, and_(Question.id==votes_subq.c.type_id, votes_subq.c.type==TYPE_QUESTION)) \
                .filter(Question.status == approved) \
                .filter(Question.id.in_(ids)) \
                .order_by(votes_subq.c.vote_count.desc()) \
                # .limit(limit).offset(offset)
            # raise Exception(votes_questions.all())
        
            questions = [q[0].serialize() for q in questions]

        return jsonify({"activities":questions})
    
    return render_template("ask/questions.html",
        search_form = search_form)

@mod.route('/question/<slug>/', methods=['GET', 'POST'])
def answer(slug):
    
    reply_form = ReplyForm()
    question = Question.query.filter_by(slug=slug).first_or_404()
    
    if request.method == 'POST':
        
        if request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
            g.user = User.query.get(request.form["user"])
        elif g.user is None or not g.user.is_authenticated():
            flash(gettext('You need to be signed in to reply to questions.'))
            return redirect(url_for('.answer', slug=question.slug))
            
        if "user" not in request.form:
            form_json = {"user": g.user.id, "reply": reply_form.reply.data, "parent": reply_form.parent.data}
            try:
                opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
            except:
                flash(gettext("The server is not responding. Please try again later."))
                return redirect(url_for('.answer', slug=question.slug))
            
        timestamp = datetime.utcnow()
        reply = Reply(body=reply_form.reply.data, timestamp=timestamp, 
                        user=g.user, question=question, parent_id=reply_form.parent.data)
        db.session.add(reply)
        db.session.commit()
        if not reply_form.parent.data:
            reply.parent_id = reply.id
            db.session.add(reply)
            db.session.commit()
        flash(gettext('Reply submitted.'))
        return redirect(url_for('ask.answer', slug=question.slug))
    else:
        question.vote = False
        if g.user.is_authenticated():
            vote = Vote.query.filter_by(type = 0, type_id = question.id, user_id = g.user.id).first()
            if vote:
                question.vote = True
        tags = [t.to_attr() for t in question.tags]
        for r in question.replies:
            r.vote = False
            if g.user.is_authenticated():
                vote = Vote.query.filter_by(type = 1, type_id = r.id, user_id = g.user.id).first()
                if vote:
                    r.vote = True
            r.flag = False
            if g.user.is_authenticated():
                flag = Flag.query.filter_by(reply_id = r.id, user_id = g.user.id).first()
                if flag:
                    r.flag = True
        return render_template("ask/answer.html",
            reply_form = reply_form,
            question = question,
            tags = tags)

@mod.route('/question/<slug>/vote/')
@mod.route('/question/<slug>/vote/<user>/')
def question_vote(slug, user=None):
    
    q = Question.query.filter_by(slug=slug).first_or_404()
    if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
        g.user = User.query.get(user)
    elif g.user is None or not g.user.is_authenticated():
        return jsonify({"error": gettext("You need to be logged in to vote.")})
    elif user is None and g.user is None:
        abort(404)
    
    if user is None:
        try:
            opener = urllib2.urlopen("{0}ask/question/{1}/vote/{2}/".format(SITE_MIRROR,slug,g.user.id),None,5)
        except:
            return jsonify({"error": gettext("The server is not responding. Please try again later.")})
        
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
    if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
        g.user = User.query.get(user)
    elif g.user is None or not g.user.is_authenticated():
        return jsonify({"error": gettext("You need to be logged in to vote.")})
    elif user is None and g.user is None:
        abort(404)
    
    if user is None:
        try:
            opener = urllib2.urlopen("{0}ask/reply/{1}/vote/{2}/".format(SITE_MIRROR,id,g.user.id),None,5)
        except:
            return jsonify({"error": gettext("The server is not responding. Please try again later.")})

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
    
    if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
        g.user = User.query.get(user)
    elif g.user is None or not g.user.is_authenticated():
        return jsonify({"error": gettext("You need to be logged in to flag replies.")})
    elif user is None and g.user is None:
        abort(404)
    
    if user is None:
        try:
            opener = urllib2.urlopen("{0}ask/reply/{1}/flag/{2}/".format(SITE_MIRROR,id,g.user.id),None,5)
        except:
            return jsonify({"error": gettext("The server is not responding. Please try again later.")})

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

@mod.route('/ask/', methods=['GET', 'POST'])
@mod.route('/ask/<user>/', methods=['GET', 'POST'])
def ask(user=None):
    form = AskForm()
    if request.method == 'POST':
        
        if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
            g.user = User.query.get(user)
        elif g.user is None or not g.user.is_authenticated():
            flash(gettext('You need to be logged in to ask questions.'))
            return redirect(url_for('account.login'))
        elif user is None and g.user is None:
            abort(404)
            
        if user is None:
            form_json = {"question": form.question.data, "body": form.body.data, "app": form.app.data, "tags": form.tags.data}
            try:
                opener = urllib2.urlopen("{0}ask/ask/{1}/".format(SITE_MIRROR,g.user.id),urllib.urlencode(form_json),5)
            except:
                flash(gettext("The server is not responding. Please try again later."))
                return render_template("ask/ask.html", form = form)
        
        timestamp = datetime.utcnow()
        slug = Question.make_unique_slug(form.question.data)
        question = Question(question=form.question.data, body=form.body.data, timestamp=timestamp, user=g.user, slug=slug)
        if "," in form.tags.data:
            tags = form.tags.data.split(",")
            question.str_tags(tags)
        db.session.add(question)
        db.session.commit()
        flash(gettext('Your question has been submitted and is pending approval.'))
        if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
            return jsonify({"status": "Success"})
        else:
            return redirect(url_for('ask.index'))
    return render_template("ask/ask.html", form = form)
