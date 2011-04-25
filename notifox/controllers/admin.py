import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render, Session
from notifox.model.user import User
from notifox.model.page import Page

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

    def users(self):
        if 'del' in request.params:
            badboy = Session.query(User).filter_by(id=request.params['del']).all()
            if len(badboy) > 0:
                Session.delete(badboy[0])
                Session.commit()
        c.users = Session.query(User).all()
        return render("/derived/admin/users.mako")

    def pages(self):
        c.pages = Session.query(Page).all()
        return render("/derived/admin/pages.mako")
