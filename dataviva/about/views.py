from sqlalchemy import func, and_, or_
from datetime import datetime
from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app, abort
from flask.ext.babel import gettext
from dataviva import db, view_cache

from dataviva.attrs.models import Bra, Wld, Course_hedu, Hs
from dataviva.rais.models import Cnae, Cbo

from dataviva.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.ask.forms import AskForm, ReplyForm, SearchForm

from dataviva.utils.send_mail import send_mail
from dataviva.utils.cached_query import cached_query, make_cache_key

from dataviva.apps.models import Crosswalk_oc, Crosswalk_pi

from config import ADMINISTRATOR_EMAIL, basedir
import os

mod = Blueprint('about', __name__, url_prefix='/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#d67ab0"

@mod.route('/crosswalk/oc/<attr1>/<attr2>/')
def crosswalk_oc(attr1, attr2):
    oc = Crosswalk_oc.query.all()
    cbos = set([x.cbo_id for x in oc])
    courses = set([x.course_hedu_id for x in oc])

    cbo_to_course = dict.fromkeys(cbos, set())
    course_to_cbo = dict.fromkeys(courses, set())

    for x in oc:
       cbo_to_course[x.cbo_id] = cbo_to_course[x.cbo_id].union([x.course_hedu_id])
       course_to_cbo[x.course_hedu_id] = course_to_cbo[x.course_hedu_id].union([x.cbo_id])

    # load attrs
    cbo_attrs = Cbo.query.filter(Cbo.id.in_(cbos)).all()
    cbo_attrs = {x.id: x for x in cbo_attrs}

    course_attrs = Course_hedu.query.filter(Course_hedu.id.in_(courses)).all()
    course_attrs = {x.id: x for x in course_attrs}

    oc = {}
    for cbo in cbo_to_course:
        cbo_name = cbo_attrs[cbo]
        course_names = [course_attrs[course] for course in cbo_to_course[cbo] if course in course_attrs]
        if course_names:
            oc[cbo_name] = course_names

    co = {}
    for course in course_to_cbo:
        if course in course_attrs:
            course_name = course_attrs[course]
            cbo_names = [cbo_attrs[cbo] for cbo in course_to_cbo[course] if cbo in cbo_attrs]
            if cbo_names:
                co[course_name] = cbo_names

    cbo_mode = attr1 == "cbo"
    full_map = oc if cbo_mode else co
    col1 = gettext("Occupation" if cbo_mode else "Course")
    col2 = gettext("Courses" if cbo_mode else "Occupations")
    tmp = "%s to %s Crosswalk" % (col1, col2)
    title=gettext(tmp)
    return render_template("about/crosswalk.html", crosswalk=full_map, title=title, col1=col1, col2=col2)

@mod.route('/crosswalk/pi/<attr1>/<attr2>/')
def crosswalk_pi(attr1, attr2):
    pi = Crosswalk_pi.query.all()
    hss = set([x.hs_id for x in pi])
    cnaes = set([x.cnae_id for x in pi])

    hs_to_cnae = dict.fromkeys(hss, set())
    cnae_to_hs = dict.fromkeys(cnaes, set())

    for x in pi:
       hs_to_cnae[x.hs_id] = hs_to_cnae[x.hs_id].union([x.cnae_id])
       cnae_to_hs[x.cnae_id] = cnae_to_hs[x.cnae_id].union([x.hs_id])

    hs_attrs = Hs.query.filter(Hs.id.in_(hss)).all()
    hs_attrs = {x.id: x for x in hs_attrs}

    cnae_attrs = Cnae.query.filter(Cnae.id.in_(cnaes)).all()
    cnae_attrs = {x.id: x for x in cnae_attrs}

    pi = {}
    for hs in hs_to_cnae:
        cbo_name = hs_attrs[hs]
        cnae_names = [cnae_attrs[cnae] for cnae in hs_to_cnae[hs] if cnae in cnae_attrs]
        if cnae_names:
            pi[cbo_name] = cnae_names
    ip = {}
    for cnae in cnae_to_hs:
        if cnae in cnae_attrs:
            cnae_name = cnae_attrs[cnae]
            hs_names = [hs_attrs[hs] for hs in cnae_to_hs[cnae] if hs in hs_attrs]
            if hs_names:
                ip[cnae_name] = hs_names

    hs_mode = attr1 == "hs"
    full_map = pi if hs_mode else ip
    col1 = gettext("Product" if hs_mode else "Course")
    col2 = gettext("Courses" if hs_mode else "Products")
    tmp = "%s to %s Crosswalk" % (col1, col2)
    title=gettext(tmp)
    return render_template("about/crosswalk.html", crosswalk=full_map, title=title, col1=col1, col2=col2)

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
    depths["bra"] = [1,3,5,8,9]
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
