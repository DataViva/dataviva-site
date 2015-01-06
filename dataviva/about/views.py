from sqlalchemy import func, and_, or_
from datetime import datetime
from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app, abort
from flask.ext.babel import gettext
from dataviva import db, view_cache

from dataviva.attrs.models import Bra, Wld
from dataviva.rais.models import Cnae, Cbo
from dataviva.secex.models import Hs

from dataviva.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.ask.forms import AskForm, ReplyForm, SearchForm

from dataviva.utils.send_mail import send_mail
from dataviva.utils.cached_query import cached_query, make_cache_key

from config import ADMINISTRATOR_EMAIL, basedir
import os

mod = Blueprint('about', __name__, url_prefix='/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#d67ab0"

@mod.route('/analysis/')
def analysis():
    return render_template("about/analysis.html", page = "analysis")

@mod.route('/testimonial/')
def testimonial():
    return render_template("about/testimonial.html", page = "testimonial")

@mod.route('/data/<data>/')
def data(data):
    return render_template("about/data/index.html", data=data, page = "data")

@mod.route('/glossary/<term>/')
def glossary(term):
    return render_template("about/glossary/index.html", term=term, page = "glossary")

@mod.route('/apps/<app>/')
def apps(app):
    return render_template("about/apps/index.html", app=app, page = "apps")

@mod.route('/classification/<attr>/<depth>/')
def attrs(attr="bra",depth="2"):

    data_url = "/attrs/table/{0}/{1}/".format(attr,depth)

    depths = {}
    depths["bra"] = [2,4,7,8]
    depths["cnae"] = [1,3,6]
    depths["cbo"] = [1,2,4]
    depths["hs"] = [2,4,6]
    depths["wld"] = [2,5]

    return render_template("about/attrs.html", data_url=data_url, depths = depths[attr], page = "attrs", attr = attr, depth = int(depth))

@mod.route('/')
@mod.route('/contact/')
def contact():
    search_form = SearchForm()
    return render_template("about/ask/index.html", page = "ask", search_form = search_form)

@mod.route('/ask/', methods=['GET', 'POST'])
@mod.route('/ask/<user>/', methods=['GET', 'POST'])

def ask(user=None):
    form = AskForm()
    if request.method == 'POST':

        if g.user is None or not g.user.is_authenticated():
            flash(gettext('You need to be logged in to ask questions.'))
            return redirect(url_for('account.login'))

        if form.validate_on_submit():
            timestamp = datetime.utcnow()
            slug = Question.make_unique_slug(form.question.data)

            from ..utils.profanities_filter import ProfanitiesFilter

            file_banned_words = open(os.path.join(basedir, "dataviva/static/txt/blacklist.txt"))
            banned_words = [line.strip() for line in file_banned_words]

            filter = ProfanitiesFilter(banned_words, replacements = '*')
            _question = filter.clean(str(form.question.data.encode("utf-8")))
            _body =  filter.clean(str(form.body.data.encode("utf-8")))
            _type = filter.clean(str(form.type.data))


            question = Question(question=_question, body=_body, timestamp=timestamp, user=g.user, slug=slug, language=g.locale, type_id=_type)
            if "," in form.tags.data:
                tags = form.tags.data.split(",")
                question.str_tags(tags)
            db.session.add(question)
            db.session.commit()
            try:
                flash(gettext('Your message was sent successfully. Thank you for your contribution, it will be helpful to other users and is essential to improving our tool! Our team will contact you by e-mail shortly.'))
                send_mail('Aviso de nova publicacao no DataViva', [ADMINISTRATOR_EMAIL], render_template('about/ask/ask_feedback.html', question=question))
            except BaseException as e:
                print e
            # if user and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
            #     return jsonify({"status": "Success"})
            # else:
            return redirect(url_for('about.contact'))
        else:
            return render_template("about/ask/ask.html", page = "ask", form = form)

    return render_template("about/ask/ask.html", page = "ask", form = form)

@mod.route('/question/<slug>/', methods=['GET', 'POST'])
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def answer(slug):

    reply_form = ReplyForm()
    question = Question.query.filter_by(slug=slug).first_or_404()
    if request.method == 'POST':

        # if request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
        #     g.user = User.query.get(request.form["user"])
        if g.user is None or not g.user.is_authenticated():
            flash(gettext('You need to be signed in to reply to questions.'))
            return redirect(url_for('about.answer', slug=question.slug))

        # if "user" not in request.form:
        #     form_json = {"user": g.user.id, "reply": reply_form.reply.data, "parent": reply_form.parent.data}
        #     try:
        #         opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
        #     except:
        #         flash(gettext("The server is not responding. Please try again later."))
        #         return redirect(url_for('.answer', slug=question.slug))

        timestamp = datetime.utcnow()
        if not reply_form.parent.data:
            parent_id = 0
        else:
            parent_id = reply_form.parent.data

        hiddenFld = 2;

        from ..utils.profanities_filter import ProfanitiesFilter

        file_banned_words = open(os.path.join(basedir, "dataviva/static/txt/blacklist.txt"))
        banned_words = [line.strip() for line in file_banned_words]

        filter = ProfanitiesFilter(banned_words, replacements = '*')
        _body =  filter.clean(str(reply_form.reply.data))


        reply = Reply(body=_body, timestamp=timestamp,
                        user=g.user, question=question, parent_id=parent_id, hidden=hiddenFld)

        db.session.add(reply)
        db.session.commit()
        if not reply_form.parent.data:
            reply.parent_id = reply.id
            db.session.add(reply)
            db.session.commit()

        try:
            flash(gettext('Reply submitted. Your reply will show up after we review it.'))
             #envia email para o admin
            send_mail('Aviso de nova publicacao no DataViva', [ADMINISTRATOR_EMAIL], render_template('about/ask/ask_feedback.html', question=question))
        except:
                flash(gettext('Your Reply was not sent. Try later, please.'))

        return redirect(url_for('about.answer', slug=question.slug))
    else:

        question.vote = False
        if g.user.is_authenticated():
            vote = Vote.query.filter_by(type = 0, type_id = question.id, user_id = g.user.id).first()
            if vote:
                question.vote = True

        return render_template("about/ask/answer.html",
            reply_form = reply_form,
            question = question, page = "ask")

@mod.route('/terms_of_use', methods=['GET'])
def terms_of_use():
    return render_template("about/" + gettext("terms_of_use") + ".html", page='terms_of_use')
