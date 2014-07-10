from dataviva import app
from flask.ext.script import Manager
app.debug = True
manager = Manager(app)
manager.run()
