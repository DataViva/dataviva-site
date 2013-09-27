from sqlalchemy import func
from flask import Blueprint, render_template, g, redirect, url_for, \
    flash, request, jsonify
from flask.ext.login import login_required
from dataviva import db
from datetime import datetime
# models
from dataviva.account.models import User
from dataviva.ask.models import Question, Status, Reply, Flag
# forms
from dataviva.admin.forms import AdminQuestionUpdateForm

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

@mod.route('/user/<int:user_id>/', methods = ['PUT'])
@login_required
def update_user(user_id):
    # test with:
    # curl -i -H "Content-Type: application/json" -X PUT 
    #   -d '{"role":2}' http://localhost:5000/admin/user/1
    
    user = User.query.get(user_id)
    user.role = request.json.get('role', user.role)
    db.session.add(user)
    db.session.commit()
    
    return jsonify( {'user': user.serialize()} )

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
@login_required
def admin_questions_edit(status, question_id):
    
    q = Question.query.get_or_404(question_id)
    s = Status.query.filter_by(name=status).first_or_404()
    form = AdminQuestionUpdateForm()
    
    if form.validate_on_submit():
        previous_status = form.previous_status.data
        q.status = form.status.data
        q.status_notes = form.answer.data
        db.session.add(q)
        db.session.commit()
        flash(_('This question has now been updated.'))
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