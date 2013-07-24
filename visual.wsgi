import sys
sys.path.insert(0, '/web/testvisual.com')

from visual import app as application

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, True)
