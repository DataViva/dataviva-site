from dataviva import db


class GraphTitle(db.Model):
    __tablename__ = 'graph_title'
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(255))
    subtitle_en = db.Column(db.String(255))
    dataset = db.Column(db.String(45))
    graph = db.Column(db.String(45))
    shapes = db.Column(db.String(45))
    type = db.Column(db.String(45))
    product = db.Column(db.Boolean)
    partner = db.Column(db.Boolean)
    location = db.Column(db.Boolean)
    industry = db.Column(db.Boolean)
    occupation = db.Column(db.Boolean)
