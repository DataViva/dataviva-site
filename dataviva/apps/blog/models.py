from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base()

association_table = Table('blog_post_subject', Base.metadata,
    Column('post_id', Integer, ForeignKey('blog_post.id')),
    Column('subject_id', Integer, ForeignKey('blog_subject.id'))
)


class Post(Base):
    __tablename__ = 'blog_post'
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    author = Column(String(100))
    text_call = Column(String(500))
    text_content = Column(Text(4194304))
    thumb = Column(Text(4194304))
    postage_date = Column(DateTime)
    active = Column(Boolean)

    subjects = relationship(
        "Subject",
        secondary=association_table,
        back_populates="posts")

    def __init__(self, title=None, author=None, text_call=None, 
                    text_content=None, thumb=None, postage_date=None, 
                    active=False):
        self.title = title 
        self.author = author 
        self.text_call = text_call 
        self.text_content = text_content 
        self.thumb = thumb 
        self.postage_date = postage_date 
        self.active = active

    def date_str(self):
        return self.postage_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Subject(Base):
    __tablename__ = 'blog_subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    posts = relationship(
        "Post",
        secondary=association_table,
        back_populates="subjects")

    def __init__(self, name=None):
        self.name = name
    
    def __repr__(self):
        return '<PostSubject %r>' % (self.name)
