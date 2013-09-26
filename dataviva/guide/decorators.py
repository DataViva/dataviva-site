from functools import wraps

from flask import g, flash, redirect, url_for, request

def requires_login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.user is None:
      flash(_('You need to be logged in to view this page.'))
      return redirect(url_for('users.login', next=request.path))
    return f(*args, **kwargs)
  return decorated_function