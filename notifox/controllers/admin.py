import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render, Session
from notifox.model.user import User

log = logging.getLogger(__name__)

class AdminController(BaseController):

    def __before__(self):
        if not 'username' in session:
            redirect(url(controller='index', action='index'))

    def index(self):
        # Return a rendered template
        #return render('/admin.mako')
        # or, return a string
        return 'Hello World'

    def userlist(self):
        if 'username' in session:
            c.users = Session.query(User).all()
            return render("/derived/auth/users.mako")
        else:
            redirect(url(controller='auth', action='login'))
