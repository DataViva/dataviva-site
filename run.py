from visual import app

from flask.ext.script import Manager
manager = Manager(app)
manager.run()
