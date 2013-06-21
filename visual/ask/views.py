from sqlalchemy import and_, func
from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from visual import db, lm

from visual.account.models import User
from visual.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from visual.ask.forms import AskForm, ReplyForm, SearchForm
from visual.utils import Pagination, strip_html

mod = Blueprint('ask', __name__, url_prefix='/ask')

@mod.before_request
def before_request():
    g.page_type = mod.name

RESULTS_PER_PAGE = 10

@mod.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@mod.route('/questions/', methods=['GET', 'POST'], defaults={'page': 1})
@mod.route('/questions/<int:page>/', methods=['GET', 'POST'])
def index(page):
    # get URL parameters for results per page and ordering options
    order = request.args.get("order", "votes") # options = 'votes' or 'newest'
    results_per_page = int(request.args.get("results_per_page", RESULTS_PER_PAGE))
    
    # load forms for submitting new question or for searching
    search_form = SearchForm()
    
    # lets find the questions to load in the page
    # only the approved questions
    approved = Status.query.filter_by(name='Approved').first()
    questions = Question.query.filter_by(status = approved)
    # for pagination, we need to know the total num of questions
    count = questions.count()
    offset = (page - 1) * results_per_page
    
    # if we are ordering the questions by newest get them ordered chronologically
    if order == "newest":
        questions = questions.order_by(Question.timestamp.desc()) \
                        .paginate(page, RESULTS_PER_PAGE, False).items
    
    # otherwise we are ordering the questions by votes
    else:
        votes_subq = db.session.query(Vote, func.count('*').label('vote_count')).group_by(Vote.type_id).subquery()
        votes_questions = db.session.query(Question, votes_subq.c.vote_count) \
            .outerjoin(votes_subq, and_(Question.id==votes_subq.c.type_id, votes_subq.c.type==TYPE_QUESTION)) \
            .filter(Question.status == approved).order_by(votes_subq.c.vote_count.desc()) \
            .limit(results_per_page).offset(offset)
        questions = [q[0] for q in votes_questions]
            
    if not questions and page != 1:
        abort(404)
    pagination = Pagination(page, results_per_page, count, order)
    
    return render_template("ask/index.html",
        search_form = search_form,
        questions = questions,
        pagination = pagination)

@mod.route('/question/search')
def question_search():
    search_term = request.args.get('q')
    approved = Status.query.filter_by(name='Approved').first()
    questions_matched = Question.query.whoosh_search(search_term).filter_by(status = approved).all()
    matches = []
    for q in questions_matched:
        user = {"user": q.user.nickname}
        votes = {"votes": q.votes.count()}
        result = dict(q.serialize().items() + user.items() + votes.items())
        if "status_notes" in result:
            result["status_notes"] = strip_html(result["status_notes"])
        matches.append(result)
    return jsonify({"matches": matches})
    # return jsonify({"matches": [dict(q.serialize().items() + {"votes": q.votes.count()}.items()) for q in questions_matched]})

@mod.route('/question/<slug>', methods=['GET', 'POST'])
def answer(slug):
    reply_form = ReplyForm()
    question = Question.query.filter_by(slug=slug).first()
    if not question:
        question = Question.query.filter_by(id=slug).first_or_404()
        return redirect(url_for("ask.answer", slug=question.slug))
    
    if reply_form.validate_on_submit():
        if g.user is None or not g.user.is_authenticated():
            flash('You need to be signed in for this.')
            return redirect(url_for('admin.login'))
        timestamp = datetime.utcnow()
        reply = Reply(body=reply_form.reply.data, timestamp=timestamp, 
                        user=g.user, question=question, parent_id=reply_form.parent.data)
        db.session.add(reply)
        db.session.commit()
        if not reply_form.parent.data:
            reply.parent_id = reply.id
            db.session.add(reply)
            db.session.commit()
        flash('Reply submitted.')
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
        return jsonify({"error": "You need to be logged in for this action."})
        
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
        return jsonify({"error": "You need to be logged in for this action."})

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
        return jsonify({"error": "You need to be logged in for this action."})

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
            flash('You need to be signed in for this.')
            return redirect(url_for('account.login'))
        timestamp = datetime.utcnow()
        slug = Question.make_unique_slug(form.question.data)
        question = Question(question=form.question.data, body=form.body.data, timestamp=timestamp, user=g.user, slug=slug)
        if "," in form.tags.data:
            tags = form.tags.data.split(",")
            question.str_tags(tags)
        db.session.add(question)
        db.session.commit()
        flash('Your question has been submitted and is pending approval by a site administrator.')
        return redirect(url_for('ask.index'))
    return render_template("ask/ask.html", form = form)
