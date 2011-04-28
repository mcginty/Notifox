import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render, Session
from notifox.helpers.auth import user_exists, verify, generate_password, ChastityBelt
from notifox.model.user import User

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def __before__(self):
        self.users = Session.query(User)

    def login(self):
        out = render("/derived/auth/login.mako")
        if 'error' in session:
            del session['error']
            session.save()
        return out

    def login_post(self):
        if verify(request.params['username'], request.params['password']):
            me = self.users.filter_by(name=request.params['username'])
            session['username'] = request.params['username']
            session['id'] = me.id
        else:
            session['error'] = 'Invalid credentials.'
        session.save()
        redirect(url(controller='index', action='index'))

    def register(self):
        out = render("/derived/auth/register.mako")
        if 'error' in session:
            del session['error']
            session.save()
        return out

    def register_post(self):
        #TODO: make this work with a message queue system
        if 'username' not in request.params or 'password' not in request.params:
            return "This is a post-only interface."

        if user_exists(request.params['username']):
            session['error'] = 'Username exists already.'
            session.save()
            redirect(url(controller='auth', action='register'))
        hashedpass = generate_password(request.params['password'])
        registrant = User(request.params['username'], hashedpass, request.params['email'])
        Session.add(registrant)
        Session.commit()
        redirect(url(controller='index', action='index'))

    def logout(self):
        session.clear()
        session.save()
        redirect(url(controller='index', action='index'))
