import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.helpers.auth import user_exists, verify, generate_password, ChastityBelt
from notifox.model.user import User
from notifox.lib.base import BaseController, render

log = logging.getLogger(__name__)

class IndexController(BaseController):

    def index(self):
        return render('/derived/index/index.mako')
