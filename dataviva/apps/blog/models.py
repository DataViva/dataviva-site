from dataviva import db
from sqlalchemy import ForeignKey


class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    subject = db.Column(db.String(100))
    text_call = db.Column(db.String(500))
    text_content = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    postage_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    authors = db.relationship('AuthorBlog', backref='blog_post', lazy='eager')

    def authors_str(self):
        author_names = [author.name for author in self.authors]
        return ', '.join(author_names)

    def date_str(self):
        return self.postage_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Post %r>' % (self.title)


class AuthorBlog(db.Model):
    __tablename__ = 'blog_author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    post_id = db.Column(db.Integer, ForeignKey('blog_post.id'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<AuthorBlog %r>' % (self.name)
