# -*- coding: utf-8 -*-
import os

'''Used for finding environment variables through configuration
   if a default is not given, the site will raise an exception'''


def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)


''' Base directory of where the site is held '''
basedir = os.path.abspath(os.path.dirname(__file__))


UPLOAD_FOLDER = os.path.join(basedir, 'dataviva/static/uploads/')


''' CSRF (cross site forgery) for signing POST requests to server '''
CSRF_EN = True

''' Secret key should be set in environment var '''
SECRET_KEY = get_env_variable(
    "DATAVIVA_SECRET_KEY", "default-dataviva.mg-secr3t")

''' Default debugging to True '''
DEBUG = True
DEBUG_WITH_APTANA = True
SQLALCHEMY_ECHO = True
GZIP_DATA = get_env_variable("DATAVIVA_GZIP_DATA", True)

''' Whether or not to allow User Account Activity '''
ACCOUNTS = get_env_variable("DATAVIVA_ACCOUNTS", True)

'''
    Details for connecting to the database, credentials set as environment
    variables.
'''
SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(
    get_env_variable("DATAVIVA_DB_USER", "root"),
    get_env_variable("DATAVIVA_DB_PW", ""),
    get_env_variable("DATAVIVA_DB_HOST", "localhost"),
    get_env_variable("DATAVIVA_DB_NAME", "dataviva"))

''' If user prefers to connect via socket set env var '''
if "DATAVIVA_DB_SOCKET" in os.environ:
    SQLALCHEMY_DATABASE_URI += "?unix_socket=" + \
        get_env_variable("DATAVIVA_DB_SOCKET")

''' If an env var for production is set turn off all debugging support '''
if "DATAVIVA_PRODUCTION" in os.environ:
    SQLALCHEMY_ECHO = False
    DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SESSION_COOKIE_DOMAIN = ".dataviva.info"

''' Available languages '''
LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

''' For full text search '''
WHOOSH_BASE = os.path.join(basedir, 'search.db')

'''
    Oauth tokens set in environment variables from their respecive sources
'''
GOOGLE_OAUTH_ID = get_env_variable("DATAVIVA_OAUTH_GOOGLE_ID")
GOOGLE_OAUTH_SECRET = get_env_variable("DATAVIVA_OAUTH_GOOGLE_SECRET")
TWITTER_OAUTH_ID = get_env_variable("DATAVIVA_OAUTH_TWITTER_ID")
TWITTER_OAUTH_SECRET = get_env_variable("DATAVIVA_OAUTH_TWITTER_SECRET")
FACEBOOK_OAUTH_ID = get_env_variable("DATAVIVA_OAUTH_FACEBOOK_ID")
FACEBOOK_OAUTH_SECRET = get_env_variable("DATAVIVA_OAUTH_FACEBOOK_SECRET")
AWS_ACCESS_KEY = get_env_variable('DATAVIVA_OAUTH_AWS_ID')
AWS_SECRET_KEY = get_env_variable('DATAVIVA_OAUTH_AWS_SECRET')

''' S3 Buckets '''
S3_BUCKET = get_env_variable('S3_BUCKET', 'dataviva-dev')
S3_HOST = get_env_variable('S3_HOST', 'https://dataviva.s3.amazonaws.com')

'''
    Mail credentials to send automatic emails to users
'''
MAIL_SERVER = get_env_variable("DATAVIVA_MAIL_SERVER", 'smtp.gmail.com')
MAIL_PORT = get_env_variable("DATAVIVA_MAIL_PORT", 587)
MAIL_USE_TLS = get_env_variable("DATAVIVA_MAIL_USE_TLS", False)
MAIL_USE_SSL = get_env_variable("DATAVIVA_MAIL_USE_SSL", False)
MAIL_USERNAME = get_env_variable("DATAVIVA_MAIL_USERNAME", 'contato@dataviva.info')
MAIL_PASSWORD = get_env_variable("DATAVIVA_MAIL_PASSWORD", "")

'''
    Administrator email
'''
ADMINISTRATOR_EMAIL = 'contato@dataviva.info'

'''
    Pagination
'''
ITEMS_PER_PAGE = 10
BOOTSTRAP_VERSION = 3
'''
    TEST USER
'''
TEST_USER_EMAIL = get_env_variable("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = get_env_variable("TEST_USER_PASSWORD", "")