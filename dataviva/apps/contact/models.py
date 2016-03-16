from dataviva import db
import smtplib


class Form(db.Model):
    __tablename__ = 'contact_form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    email = db.Column(db.Text())
    message = db.Column(db.String(250))
    postage_date = db.Column(db.DateTime)

    def date_str(self):
        return self.postage_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Article %r>' % (self.title)

    sender = email
    receivers = ['contato@dataviva.info']

#       try:
#       smtpObj = smtplib.SMTP('localhost')
#       smtpObj.sendmail(sender, receivers, message)
#       print "Successfully sent e-mail"
#    except SMTPException:
#       print "Error: unable to send e-mail"