import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/auth.mako')
        # or, return a string
        return 'Hello World'

    def register(self):
        return render("/derived/auth/register.mako")
