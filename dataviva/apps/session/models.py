from dataviva.apps.session.login_providers import facebook, twitter, google
from dataviva.apps.account.models import User
from dataviva.utils.encode import sha512
from flask import Blueprint, request, render_template, session, redirect, Response

from flask.ext.login import login_user, logout_user
from forms import LoginForm


mod = Blueprint('session', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/session',
                static_folder='static')


@mod.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data, password=sha512(form.password.data)).first()
        if user:
            if user.confirmed:
                login_user(user, remember=True)
                return redirect("/")
            else:
                return Response("Confirm Pending", status=401, mimetype='application/json', )
        else:
            return Response("Email or Password Incorrect!", status=400, mimetype='application/json')

    else:
        return render_template('user/login.html', form=form)


@mod.route('/logout/')
def logout():
    session.pop('twitter_token', None)
    session.pop('google_token', None)
    session.pop('facebook_token', None)
    logout_user()
    return redirect('/')
