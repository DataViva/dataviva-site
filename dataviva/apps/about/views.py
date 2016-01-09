from sqlalchemy import func, and_, or_
from datetime import datetime
from flask import Blueprint, request, make_response, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app, abort
from flask.ext.babel import gettext
from dataviva import db, view_cache

from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Bra, Wld, Course_hedu, Hs
from dataviva.api.rais.models import Cnae, Cbo

from dataviva.apps.ask.models import Question, Reply, Status, Vote, TYPE_QUESTION, TYPE_REPLY, Flag
from dataviva.apps.ask.forms import AskForm, ReplyForm, SearchForm

from dataviva.utils.send_mail import send_mail
from dataviva.utils.cached_query import cached_query, api_cache_key

from dataviva.apps.charts.models import Crosswalk_oc, Crosswalk_pi

from config import ADMINISTRATOR_EMAIL, basedir
import os

mod = Blueprint('about', __name__, url_prefix='/<lang_code>/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#d67ab0"

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

@mod.route('/crosswalk/<attr1>/<attr2>/')
def crosswalk(attr1, attr2):
    attr_table_map = {"cbo" : (gettext("Occupation"), Cbo), "course_hedu" : (gettext("Major"), Course_hedu),
                      "hs": (gettext("Product"), Hs), "cnae": (gettext("Industry"), Cnae)}
    col1, Attr1_Table = attr_table_map[attr1]
    col2, Attr2_Table = attr_table_map[attr2]
    cbo_mode = "cbo" in [attr1, attr2]
    Crosswalk_table = Crosswalk_oc if cbo_mode else Crosswalk_pi
    filename = "cbo-course" if cbo_mode else "hs-cnae"
    filename = filename + "_" + g.locale + ".csv"

    crosswalks = Crosswalk_table.query.all()
    attr1_list = set([ getattr(x, attr1+"_id") for x in crosswalks])
    attr2_list = set([ getattr(x, attr2+"_id") for x in crosswalks])

    attr1_to_attr2 = dict.fromkeys(attr1_list, set())

    for x in crosswalks:
       attr1_to_attr2[getattr(x, attr1+"_id")] = attr1_to_attr2[getattr(x, attr1+"_id")].union([getattr(x, attr2+"_id")])

    attr1_lookup = Attr1_Table.query.filter(Attr1_Table.id.in_(attr1_list)).all()
    attr1_lookup = {x.id: x for x in attr1_lookup}
    attr2_lookup = Attr2_Table.query.filter(Attr2_Table.id.in_(attr2_list)).all()
    attr2_lookup = {x.id: x for x in attr2_lookup}

    full_map = {}
    for attr_id1 in attr1_to_attr2:
        if not attr_id1 in attr1_lookup: continue
        attr1_obj = attr1_lookup[attr_id1]
        attr2_objs = [attr2_lookup[attr2_id] for attr2_id in attr1_to_attr2[attr_id1] if attr2_id in attr2_lookup]
        if attr2_objs:
            full_map[attr1_obj] = attr2_objs

    title = gettext(col1) + gettext(" to ") + gettext(col2)

    return render_template("about/crosswalk.html", filename=filename, crosswalk=full_map, title=title, col1=col1, col2=col2, page="crosswalk", attrs="{}-{}".format(attr1, attr2))


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
def attrs(attr="bra",depth="3"):

    data_url = "/attrs/table/{0}/{1}/".format(attr,depth)

    depths = {}
    depths["bra"] = [1,3,5,7,9]
    depths["cnae"] = [1,3,6]
    depths["cbo"] = [1,4]
    depths["hs"] = [2,6]
    depths["wld"] = [2,5]
    depths["course_hedu"] = [2,6]
    depths["university"] = [5]
    depths["course_sc"] = [2,5]

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

        if g.user is None or not g.user.is_authenticated:
            flash(gettext('You need to be logged in to ask questions.'))
            return redirect(url_for('account.login'))

        if form.validate_on_submit():
            timestamp = datetime.utcnow()
            slug = Question.make_unique_slug(form.question.data)

            from dataviva.utils.profanities_filter import ProfanitiesFilter

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
        if g.user is None or not g.user.is_authenticated:
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

        from dataviva.utils.profanities_filter import ProfanitiesFilter

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
        if g.user.is_authenticated:
            vote = Vote.query.filter_by(type = 0, type_id = question.id, user_id = g.user.id).first()
            if vote:
                question.vote = True

        return render_template("about/ask/answer.html",
            reply_form = reply_form,
            question = question, page = "ask")

@mod.route('/terms_of_use', methods=['GET'])
def terms_of_use():
    return render_template("about/" + gettext("terms_of_use") + ".html", page='terms_of_use')
