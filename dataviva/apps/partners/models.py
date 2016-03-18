from dataviva import db

class Call(db.Model):
    __tablename__ = 'partner_call'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    link = db.Column(db.String(250))
    active = db.Column(db.Integer)

