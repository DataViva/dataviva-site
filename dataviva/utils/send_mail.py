''' Send email to users
    recipients=["dataviva@googlegroups.com","datavivaweb@gmail.com"]
    title="Hello"
    message="Invite friends: {0}".format(name)
'''
from dataviva import mail
from flask.ext.mail import Message


def send_mail(title, recipients, message):
    msg = Message(title, sender="dataviva", recipients=recipients)
    msg.body = message
    msg.html = msg.body
    mail.send(msg)
