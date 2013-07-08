from flask import Blueprint, render_template, g, redirect, url_for, flash
from flask.ext.login import login_required
from visual import db
from datetime import datetime
# models
from visual.account.models import User

mod = Blueprint('admin', __name__, url_prefix='/admin')


@mod.before_request
def before_request():
    if not g.user.is_admin():
        flash('You need admin privledges for this section of the site!')
        return redirect(url_for('account.activity'))

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
    # get all users EXCEPT the logged in user
    all_users = User.query.filter(User.id != g.user.id).all()
    return render_template("admin/admin_users.html", all_users=all_users)


'''
###############################
# Views for ADMIN logged in users
# ---------------------------
@mod.route('/questions/', defaults={'status': 'Pending', 'page': 1})
@mod.route('/questions/<status>/', defaults={'page': 1})
@mod.route('/questions/<status>/<int:page>/')
@login_required
def questions(status, page):

    status_dropdown = StatusForm()
    # if status_dropdown.validate_on_submit():
    curr_status = Status.query.filter_by(name=status.title()).first_or_404()
    status_dropdown.status.data = curr_status
    questions = Question.query.filter_by(status = curr_status)
    count = questions.count()
    questions = questions.order_by(Question.timestamp.desc()) \
                    .paginate(page, RESULTS_PER_PAGE, False).items
    
    if not questions and page != 1:
        abort(404)
    pagination = Pagination(page, RESULTS_PER_PAGE, count)
    
    return render_template('admin/questions.html', 
        questions = questions,
        pagination = pagination,
        status = curr_status,
        status_dropdown = status_dropdown)


###############################
# [AJAX] Views for editing questions
# ---------------------------
@mod.route('/question/<int:question_id>/')
@mod.route('/question/<int:question_id>/<action>/', methods=['GET', 'POST'])
@login_required
def question_edit(question_id, action=None):
    if not g.user.is_admin():
        return page_not_found("Must be admin for this action.")
    q = Question.query.get_or_404(question_id)
    form = StatusNotesForm()
    if form.validate_on_submit():
        s = Status.query.filter_by(name=action.title()).first()
        q.status = s
        q.status_notes = form.status_notes.data
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('admin.questions'))
    form.status_notes.data = q.status_notes
    return render_template('admin/snippets/status_notes_form.html', form=form)
    return render_template('admin/snippets/status_notes_form.html', form=form)
'''