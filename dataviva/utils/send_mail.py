''' Send email to users 
    recipients=["dataviva@googlegroups.com","datavivaweb@gmail.com"]
    title="Hello"
    message="Invite friends: {0}".format(name)
'''
def send_mail(title, recipients,message):   
    from dataviva import mail
    from flask.ext.mail import Message
    msg = Message(title,sender="datavivaweb@gmail.com",recipients=recipients)   
    msg.body = message
    msg.html = msg.body 
    mail.send(msg)