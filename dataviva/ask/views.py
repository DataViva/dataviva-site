from sqlalchemy import and_, func
from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from flask.ext.babel import gettext
from dataviva import db, lm

from dataviva.account.models import User
from dataviva.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.ask.forms import AskForm, ReplyForm, SearchForm
from dataviva.utils import strip_html

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

@mod.route('/question/<slug>', methods=['GET', 'POST'])
def answer(slug):
    reply_form = ReplyForm()
    question = Question.query.filter_by(slug=slug).first()
    if not question:
        question = Question.query.filter_by(id=slug).first_or_404()
        return redirect(url_for("ask.answer", slug=question.slug))
    
    if reply_form.validate_on_submit():
        if g.user is None or not g.user.is_authenticated():
            flash(_('You need to be signed in to reply to questions.'))
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
        flash(_('Reply submitted.'))
        return redirect(url_for('ask.answer', slug=question.slug))
    else:
        tags = [t.to_attr() for t in question.tags]
        return render_template("ask/answer.html",
            reply_form = reply_form,
            question = question,
            tags = tags)

@mod.route('/question/<slug>/vote/')
def question_vote(slug):
    q = Question.query.filter_by(slug=slug).first_or_404()
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": _("You need to be logged in to vote.")})
        
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
def reply_vote(id):
    reply = Reply.query.get_or_404(id)
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": _("You need to be logged in to vote.")})

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
def reply_flag(id):
    reply = Reply.query.get_or_404(id)
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": _("You need to be logged in to flag replies.")})

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
def ask():
    form = AskForm()
    if form.validate_on_submit():
        if g.user is None or not g.user.is_authenticated():
            flash(_('You need to be logged in to ask questions.'))
            return redirect(url_for('account.login'))
        timestamp = datetime.utcnow()
        slug = Question.make_unique_slug(form.question.data)
        question = Question(question=form.question.data, body=form.body.data, timestamp=timestamp, user=g.user, slug=slug)
        if "," in form.tags.data:
            tags = form.tags.data.split(",")
            question.str_tags(tags)
        db.session.add(question)
        db.session.commit()
        flash(_('Your question has been submitted and is pending approval.'))
        return redirect(url_for('ask.index'))
    return render_template("ask/ask.html", form = form)
