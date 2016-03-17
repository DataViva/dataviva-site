from dataviva import db

class Edict(db.Model):
    __tablename__ = 'partner_edict'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    link = db.Column(db.String(250))

