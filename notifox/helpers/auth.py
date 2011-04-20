import hashlib
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render, Session
from notifox.model.user import User
from notifox.helpers.settings import salt

def user_exists(username):
    '''
    Checks whether user is already in user database.
    '''
    users = Session.query(User)
    if len(users.filter_by(name=username).all()) > 0:
        return True
    return False

def generate_password(password):
    '''
    Generate a passsword using a plaintext pass with the secret salt in the settings file.
    @returns hashed password
    '''
    m = hashlib.sha1()
    m.update(password)
    m.update(salt)
    return m.hexdigest()

def verify(username, password):
    '''
    Takes in a user/pass combo and returns whether it's valid login info.
    '''
    users = Session.query(User)
    m = hashlib.sha1()
    m.update(password)
    m.update(salt)
    hashpass = m.hexdigest()
    if len(users.filter_by(name=username, password=hashpass).all()) > 0:
        return True
    return False

class ChastityBelt(object):
    '''
    Helper decorator for ensuring that only logged in users have access to a given controller.
    '''
    def __init__(self, login_callback):
        self.login_callback = login_callback

    def __call__(self, fn):
        print "[ChastityBelt called]"
        if 'username' in session:
            # If this specific page requires administrator access, then ensure they're an admin.
            print "[++Session OK]"
            return fn
        else:
            print "[--Invalid session]"
            return self.login_callback
