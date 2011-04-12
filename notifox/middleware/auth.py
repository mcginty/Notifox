from pylons import request, response, session, templ_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.model.user import User

class ChastityMiddleware(object):
	def __init__(self, app, config):
		self.app = app

	def __call__(self, environ, start_response):
		if not self.authorized():
			pass
		pass
	pass

