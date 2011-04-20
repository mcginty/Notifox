from pylons import request, response, session
from pylons.controllers.util import abort, redirect

from notifox.model.user import User

class AuthenticationMiddleware(object):
	def __init__(self, app, config):
		self.app = app

	def __call__(self, environ, start_response):
		session['username'] = 'test.'
		if not session.get('username'):
			return ['This request passed through MyMiddleware'] + self.app(environ, start_response)
		else:
			return ['Not logged in, asshole.']
