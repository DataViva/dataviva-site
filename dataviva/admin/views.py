from sqlalchemy import func
from flask import Blueprint, render_template, g, redirect, url_for, \
    flash, request, jsonify, make_response
from flask.ext.login import login_required
from flask.ext.babel import gettext
from dataviva import db
from datetime import datetime
# models
from dataviva.account.models import User
from dataviva.ask.models import Question, Status, Reply, Flag, Vote
# forms
from dataviva.admin.forms import AdminQuestionUpdateForm
from dataviva.utils.jinja_helpers import jinja_strip_html

#utils
from ..utils import send_mail

from functools import wraps

# import urllib2, urllib
# from config import SITE_MIRROR

mod = Blueprint('admin', __name__, url_prefix='/admin')

def get_current_user_role():
    return g.user.role

def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return gettext("You dont have permission to view this page.")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@mod.before_request
def before_request():
    g.page_type = "admin"

###############################
# Views for ALL logged in users
# ---------------------------
@mod.route('/')
@login_required
@required_roles(1)
def admin():
    return redirect(url_for('.admin_users'))

@mod.route('/users/')
@login_required
@required_roles(1)
def admin_users():

    ret = make_response(render_template("admin/admin_users.html"))

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/userslist/')
@login_required
@required_roles(1)
def admin_users_list():

    offset = request.args.get('offset', 0)
    limit = 50

    # get all users EXCEPT the logged in user
    query = User.query.filter(User.id != g.user.id)

    items = query.limit(limit).offset(offset).all()
    items = [i.serialize() for i in items]

    ret = jsonify({"activities":items})

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/user/<int:user_id>/', methods = ['PUT','POST'])
@required_roles(1)
def update_user(user_id):
    # test with:
    # curl -i -H "Content-Type: application/json" -X PUT
    #   -d '{"role":2}' http://localhost:5000/admin/user/1

    if g.user.is_authenticated() and g.user.role == 1:

        user = User.query.get(user_id)

        user.role = request.json.get('role', user.role)

        db.session.add(user)
        db.session.commit()

        return jsonify( {'user': user.serialize()} )
    else:
        abort(404)

@mod.route('/questions/')
@mod.route('/questions/<status>/')
@login_required
@required_roles(1)
def admin_questions(status=None):

    if not status:
        return redirect(url_for(".admin_questions", status="pending"))

    ret = make_response(render_template("admin/admin_questions.html"))

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/questionslist/<status>/')
@login_required
@required_roles(1)
def admin_questions_list(status=None):

    offset = request.args.get('offset', 0)
    limit = 50

    # get all users EXCEPT the logged in user
    curr_status = Status.query.filter_by(name=status).first_or_404()
    query = Question.query.filter_by(status = curr_status)

    items = query.limit(limit).offset(offset).all()
    items = [i.serialize() for i in items]
    for i in items:
        i["question"] = jinja_strip_html(i["question"])

    ret = jsonify({"activities":items})

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/mail/', methods=['GET', 'POST'])
def admin_mail():
    status = "2"
    return render_template('admin/mail/ask_feedback.html', status=status)

@mod.route('/questions/<status>/<int:question_id>/', methods=['GET', 'POST'])
@required_roles(1)
def admin_questions_edit(status, question_id):

    q = Question.query.get_or_404(question_id)
    s = Status.query.filter_by(name=status).first_or_404()
    form = AdminQuestionUpdateForm()

    if request.method == "POST":

        previous_status = form.previous_status.data
        q.status = form.status.data
        q.status_notes = form.answer.data
        q.body = form.body.data
        q.question = form.question.data
        q.language = form.language.data
        db.session.add(q)
        db.session.commit()

        user = User.query.get(q.user_id)

        # if status is approve or rejected send email
        status_id = request.form['status']
        subject = gettext('DataViva Reply')

        if (status_id == "2" or status_id == "3") and int(user.agree_mailer) > 0 :
            send_mail(subject, [user.email], render_template('admin/mail/ask_feedback.html', title=subject, status=status_id, user=user))

        flash(gettext('This question has now been updated.'))

        return redirect(url_for('.admin_questions', status=previous_status))

    # set defaults
    form.status.data = s
    form.language.data = q.language
    form.previous_status.data = s.name
    form.answer.data = q.status_notes
    form.question.data = q.question
    form.body.data = q.body

    return render_template("admin/admin_questions_edit.html",
                            question=q, status=status, form=form)
    
    
@mod.route('/questions/delete/<int:question_id>/', methods=['GET', 'POST'])
@required_roles(1)
def admin_questions_delete(question_id):

    q = Question.query.get_or_404(question_id)
    s = Status.query.filter_by(name=q.status).first()
    status = s
    db.session.delete(q)
    db.session.commit()
    flash(gettext('The item was successfully deleted.'))
    
    return redirect(url_for(".admin_questions", status=status))
    

@mod.route('/replies/')
@login_required
@required_roles(1)
def admin_replies():

    ret = make_response(render_template("admin/admin_replies.html"))

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/replieslist/')
@login_required
@required_roles(1)
def admin_replies_list():

    offset = request.args.get('offset', 0)
    limit = 50

    # get all users EXCEPT the logged in user
   
    reply = Reply.query.filter_by(hidden=2)
    question = Question.query

    items = reply.order_by(Reply.hidden.desc(), Reply.timestamp.desc()).limit(limit).offset(offset).all()
    items = [i.serialize() for i in items]
    for i in items:
        i["body"] = strip_html(i["body"])
        q = question.get(i["question_id"])
        i['question_title'] = q.question
        
    ret = jsonify({"activities":items})

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret


@mod.route('/replies/question/<int:question_id>/')
@login_required
@required_roles(1)
def admin_replies_question(question_id):
   
    questions = Question.query.get_or_404(question_id)
    reply = Reply.query.filter_by(question_id=question_id)
    replies = reply.order_by(Reply.hidden.asc(), Reply.timestamp.desc()).limit(50).offset(0).all()
    user = User.query.get(questions.user_id)
    questions.replies = replies
    #questions.user = user
    
    return render_template("admin/admin_replies_question.html", q=questions)
    

@mod.route('/replieslist/question/<int:questionid>/')
@login_required
@required_roles(1)
def admin_replies_question_list(questionid):

    offset = request.args.get('offset', 0)
    limit = 50

    # get all users EXCEPT the logged in user
   
    reply = Reply.query.filter_by(question_id=questionid)
    items = reply.order_by(Reply.hidden.desc(), Reply.timestamp.desc()).limit(limit).offset(offset).all()
    
    items = [i.serialize() for i in items]
    
    for i in items:
        i["body"] = strip_html(i["body"])
        
        
    ret = jsonify({"activities":items})

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/replies/delete/<int:reply_id>/')
@required_roles(1)
def delete_reply_question(reply_id):
    
    vote = Vote.query.filter_by(type_id=reply_id).delete()
    
    reply = Reply.query.get(reply_id)
    question = reply.question_id
    
    db.session.delete(reply)
    db.session.commit()
    
    flash(gettext('The item was successfully deleted.'))
    
    return redirect(url_for(".admin_replies_question", question_id=question))
    


@mod.route('/reply/delete/<int:reply_id>/', methods = ['GET'])
@required_roles(1)
def delete_reply(reply_id):
    
    
    
    reply = Reply.query.get(reply_id)
    
    db.session.delete(reply)
    db.session.commit()
    flash(gettext('The item was successfully deleted.'))
    
    return redirect(url_for(".admin_replies"))


@mod.route('/reply/<int:reply_id>/', methods = ['PUT','POST'])
@required_roles(1)
def update_reply(reply_id):
    # test with:
    # curl -i -H "Content-Type: application/json" -X PUT
    #   -d '{"role":2}' http://localhost:5000/admin/user/1

    if g.user.is_authenticated() and g.user.role == 1:

        reply = Reply.query.get(reply_id)

        reply.hidden = request.json.get('hidden', reply.hidden)

        db.session.add(reply)
        db.session.commit()

        return jsonify( {'reply': reply.serialize()} )
    else:
        abort(404)
