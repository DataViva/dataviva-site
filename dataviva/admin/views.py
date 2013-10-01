from sqlalchemy import func
from flask import Blueprint, render_template, g, redirect, url_for, \
    flash, request, jsonify
from flask.ext.login import login_required
from flask.ext.babel import gettext
from dataviva import db
from datetime import datetime
# models
from dataviva.account.models import User
from dataviva.ask.models import Question, Status, Reply, Flag
# forms
from dataviva.admin.forms import AdminQuestionUpdateForm

import urllib2, urllib
from config import SITE_MIRROR

mod = Blueprint('admin', __name__, url_prefix='/admin')


@mod.before_request
def before_request():
    g.page_type = "admin"

###############################
# Views for ALL logged in users
# ---------------------------
@mod.route('/')
@login_required
def admin():
    return redirect(url_for('.admin_users'))

@mod.route('/users/')
@login_required
def admin_users():
    
    offset = request.args.get('offset', 0)
    limit = 50
    
    if request.is_xhr:
        
        # get all users EXCEPT the logged in user
        query = User.query.filter(User.id != g.user.id)
        
        items = query.limit(limit).offset(offset).all()
        items = [i.serialize() for i in items]
        
        return jsonify({"activities":items})
    
    return render_template("admin/admin_users.html")

@mod.route('/user/<int:user_id>/', methods = ['PUT','POST'])
def update_user(user_id):
    # test with:
    # curl -i -H "Content-Type: application/json" -X PUT 
    #   -d '{"role":2}' http://localhost:5000/admin/user/1
    
    if (g.user.is_authenticated() and g.user.role == 1) or (request.remote_addr == SITE_MIRROR.split(":")[1][2:]):
        
        user = User.query.get(user_id)

        if request.remote_addr != SITE_MIRROR.split(":")[1][2:]:
            
            user.role = request.json.get('role', user.role)
            form_json = {"role": user.role}
            
            try:
                opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
            except:
                flash(gettext("The server is not responding. Please try again later."))
                return jsonify({"error": gettext("The server is not responding. Please try again later.")})
        else:
            user.role = request.form.get("role")
            
        db.session.add(user)
        db.session.commit()
    
        return jsonify( {'user': user.serialize()} )
    else:
        abort(404)

@mod.route('/questions/')
@mod.route('/questions/<status>/')
@login_required
def admin_questions(status=None):
    
    if not status:
        return redirect(url_for(".admin_questions", status="pending"))
    
    if request.is_xhr:
    
        offset = request.args.get('offset', 0)
        limit = 50
    
        # get all users EXCEPT the logged in user
        curr_status = Status.query.filter_by(name=status).first_or_404()
        query = Question.query.filter_by(status = curr_status)
    
        items = query.limit(limit).offset(offset).all()
        items = [i.serialize() for i in items]
    
        return jsonify({"activities":items})
    
    return render_template("admin/admin_questions.html")

@mod.route('/questions/<status>/<int:question_id>/', methods=['GET', 'POST'])
def admin_questions_edit(status, question_id):
    
    q = Question.query.get_or_404(question_id)
    s = Status.query.filter_by(name=status).first_or_404()
    form = AdminQuestionUpdateForm()
    
    if form.validate_on_submit() or request.remote_addr == SITE_MIRROR.split(":")[1][2:]:

        if request.remote_addr != SITE_MIRROR.split(":")[1][2:]:
        
            form_json = {"status": form.status.data, "answer": form.answer.data, "previous_status": form.previous_status.data}
            
            try:
                opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
            except:
                flash(gettext("The server is not responding. Please try again later."))
                return redirect(url_for('.admin_questions_edit', status=status,question_id=question_id,form=form))

        previous_status = form.previous_status.data
        q.status = form.status.data
        q.status_notes = form.answer.data
        db.session.add(q)
        db.session.commit()
        flash(gettext('This question has now been updated.'))
        return redirect(url_for('.admin_questions', status=previous_status))
    
    # set defaults
    form.status.data = s
    form.previous_status.data = s.name
    form.answer.data = q.status_notes
    
    return render_template("admin/admin_questions_edit.html", 
                            question=q, status=status, form=form)

@mod.route('/replies/')
@login_required
def admin_replies():
    
    offset = request.args.get('offset', 0)
    limit = 50
    
    if request.is_xhr:
        
        # get all users EXCEPT the logged in user
        flags_subq = db.session.query(Flag, func.count('*') \
                        .label('flag_count')) \
                        .group_by(Flag.reply_id).subquery()
        replies = db.session.query(Reply, flags_subq.c.flag_count) \
                        .order_by(flags_subq.c.flag_count.desc())
        items = replies.limit(limit).offset(offset).all()
        items = [i[0].serialize() for i in items]
    
        return jsonify({"activities":items})
    
    return render_template("admin/admin_replies.html")

@mod.route('/reply/<int:reply_id>/', methods = ['PUT','POST'])
def update_reply(reply_id):
    # test with:
    # curl -i -H "Content-Type: application/json" -X PUT 
    #   -d '{"role":2}' http://localhost:5000/admin/user/1
    
    if (g.user.is_authenticated() and g.user.role == 1) or (request.remote_addr == SITE_MIRROR.split(":")[1][2:]):
    
        reply = Reply.query.get(reply_id)
        if request.remote_addr != SITE_MIRROR.split(":")[1][2:]:
            reply.hidden = request.json.get('hidden', reply.hidden)
            form_json = {"hidden": reply.hidden}
            try:
                opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
            except:
                flash(gettext("The server is not responding. Please try again later."))
                return jsonify({"error": gettext("The server is not responding. Please try again later.")})
        else:
            reply.hidden = request.form.get("hidden")
    
        db.session.add(reply)
        db.session.commit()
    
        return jsonify( {'reply': reply.serialize()} )
    else:
        abort(404)
    
    