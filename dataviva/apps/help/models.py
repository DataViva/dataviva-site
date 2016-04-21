from dataviva import db


class HelpQuestions(Db.Model, AutoSerialize):
    __tablename__ = "help_questions"

    IdHelp_Questions = db.Column(db.Integer, primary_key=True)
    DsHelp_Questions = db.Column(db.String(400))
    TxHelp_Questions = db.Column(db.Text(4194304))