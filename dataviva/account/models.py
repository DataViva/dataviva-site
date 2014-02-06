from dataviva import db
from hashlib import md5
from dataviva.utils import AutoSerialize
from os import urandom

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_SUPER_ADMIN = 2

class User(db.Model, AutoSerialize):

    __tablename__ = 'account_user'
    
    id = db.Column(db.Integer, primary_key = True)
    google_id = db.Column(db.String(120), unique = True)
    twitter_id = db.Column(db.String(120), unique = True)
    facebook_id = db.Column(db.String(120), unique = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    fullname = db.Column(db.String(200))
    country = db.Column(db.String(80))
    language = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    website = db.Column(db.String(150))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    bio = db.Column(db.String(256))
    image = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime)
    questions = db.relationship("Question", backref = 'user', lazy = 'dynamic')
    replies = db.relationship("Reply", backref = 'user', lazy = 'dynamic')
    votes = db.relationship("Vote", backref = 'user', lazy = 'dynamic')
    flag = db.relationship("Flag", backref = 'user', lazy = 'dynamic')
    starred = db.relationship("Starred", backref = 'user', lazy = 'dynamic')
    agree_mailer = db.Column(db.Integer)
    
    def is_authenticated(self):
        return True
    
    def is_admin(self):
        return self.role
    
    def is_active(self):
        return True
    
    def is_anonymous(sef):
        return False
    
    def get_id(self):
        return unicode(self.id)
    
    def avatar(self, size):
        if self.email:
            return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)
        else:
            return 'http://www.gravatar.com/avatar/{0}?s=' + str(size) + '&d=identicon'.format(self.nickname.encode('hex'))
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname
    
    def serialize(self):
        auto_serialized = super(User, self).serialize()
        auto_serialized["avatar"] = self.avatar(50)

        return auto_serialized
        
class Starred(db.Model, AutoSerialize):

    __tablename__ = 'account_starred'
    app_id = db.Column(db.String(80), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key = True)
    app_name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<App %r starred by %r>' % (self.app_id, self.user.nickname)