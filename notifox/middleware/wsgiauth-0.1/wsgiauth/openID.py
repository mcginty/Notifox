# (c) 2005 Ben Bangert
# (c) 2005 Clark C. Evans
# Copyright (c) 2006 L. C. Rees.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

'''OpenID Authentication (Consumer)

OpenID is a distributed authentication system for single sign-on:

    http://openid.net/

This module is based on the consumer.py example that comes with the Python
OpenID library 1.1+.
'''

import cgi
import urlparse
import sys
from Cookie import SimpleCookie
try:
    import openid
except ImportError:
    print >> sys.stderr, '''Failed to import the OpenID library.
In order to use this example, you must either install the library
(see INSTALL in the root of the distribution) or else add the
library to python's import path (the PYTHONPATH environment variable).

For more information, see the README in the root of the library
distribution or http://www.openidenabled.com/
'''
    sys.exit(1)
from openid.store import filestore
from openid.consumer import consumer
from openid.oidutil import appendArgs
from openid.cryptutil import randomString
from yadis.discover import DiscoveryFailure
from urljr.fetchers import HTTPFetchingError
from wsgiauth.util import geturl, getpath, Redirect, Response
from wsgiauth.cookie import Cookie

__all__ = ['OpenID', 'openid']

def quote(s):
    '''Quotes URLs passed as query parameters.'''
    return '"%s"' % cgi.escape(s, 1)

def openid(store, **kw):
    '''Decorator for OpenID authorized middleware.'''
    def decorator(application):
        return OpenID(application, store, **kw)
    return decorator

# Fallback session tracker
_tracker = {}
# Fallback template
TEMPLATE = '''<html>
  <head><title>OpenID Form</title></head>
  <body>
    <h1>%s</h1>
    <p>Enter your OpenID identity URL:</p>
      <form method="get" action=%s>
        Identity&nbsp;URL:
        <input type="text" name="openid_url" value=%s />
        <input type="submit" value="Verify" />
      </form>
    </div>
  </body>
</html>'''

class OpenID(Cookie):

    def __init__(self, app, store, **kw):
        # Make OpenIDAuth the authorization function
        auth = OpenIDAuth(store, **kw)
        super(OpenID, self).__init__(app, auth, **kw)
        self.authorize = auth

    def initial(self, environ, start_response):
        '''Initial response to a request.'''
        # Add authentication cookie
        def cookie_response(status, headers, exc_info=None):            
            headers.append(('Set-Cookie', self.generate(environ)))
            return start_response(status, headers, exc_info)
        # Redirect to original URL
        redirect = Redirect(environ['openid.redirect'])
        return redirect(environ, cookie_response)
        

class OpenIDAuth(object):

    '''Authenticates a URL against an OpenID Server.'''

    cname = '_OIDA_'

    def __init__(self, store, **kw):
        # OpenID store
        self.store = filestore.FileOpenIDStore(store)     
        # Session tracker
        self.tracker = kw.get('tracker', _tracker)
        # Set template
        self.template = kw.get('template', TEMPLATE)

    def __call__(self, environ):
        # Base URL
        environ['openid.baseurl'] = geturl(environ, False, False)
        # Query string
        environ['openid.query'] = dict(cgi.parse_qsl(environ['QUERY_STRING']))
        # Path
        path = getpath(environ)
        # Start verification
        if path == '/verify':
            return self.verify(environ)
        # Process response
        elif path == '/process':
            return self.process(environ)
        # Prompt for URL
        else:            
            message = 'Enter an OpenID Identifier to verify.'
            return self.response(message, environ)

    def verify(self, environ):
        '''Process the form submission, initating OpenID verification.'''
        # First, make sure that the user entered something
        openid_url = environ['openid.query'].get('openid_url')
        # Ensure a URL is entered
        if not openid_url:
            message = 'Enter an OpenID Identifier to verify.'
            return self.response(message, environ)
        # Start open id session
        oidconsumer = self.getconsumer(environ)
        # Start verification
        try:
            request = oidconsumer.begin(openid_url)
        # Handle HTTP errors
        except HTTPFetchingError, exc:
            message = 'Error in discovery: %s' % cgi.escape(str(exc.why))
            return self.response(message, environ, openid_url)
        # Handle Discovery errors
        except DiscoveryFailure, exc:
            message = 'Error in discovery: %s' % cgi.escape(str(exc[0]))
            return self.response(message, environ, openid_url)
        else:
            # Handle URLs that don't have a discernable OpenID server
            if request is None:
                fmt = 'No OpenID services found for %s'
                return self.response(fmt % cgi.escape(openid_url), environ)
            # Start redirect
            else:
                return self.redirect(environ, request)      

    def process(self, environ):
        '''Handle redirect from the OpenID server.'''
        oidconsumer, openid_url = self.getconsumer(environ), ''
        # Verify OpenID server response
        info = oidconsumer.complete(environ['openid.query'])
        # Handle successful responses
        if info.status == consumer.SUCCESS:            
            # Fetch original requested URL
            redirecturl = self.tracker[self.getsid(environ)]['redirect']
            environ['openid.redirect'] = redirecturl
            # Handle i-names
            if info.endpoint.canonicalID:                    
                return info.endpoint.canonicalID
            # Otherwise, return identity URL as user name
            else:
                return info.identity_url
        # Handle failure to verify a URL where URL is returned.
        elif info.status == consumer.FAILURE and info.identity_url:
            openid_url = info.identity_url
            message = 'Verification of %s failed.' % cgi.escape(openid_url)
        # User cancelled verification
        elif info.status == consumer.CANCEL:            
            message = 'Verification cancelled'
        # Handle other errors
        else:            
            message = 'Verification failed.'
        return self.response(message, environ, openid_url)

    def buildurl(self, environ, action, **query):
        '''Build a URL relative to the server base url, with the given
        query parameters added.'''
        base = urlparse.urljoin(environ['openid.baseurl'], action)
        return appendArgs(base, query)

    def getconsumer(self, environ):
        '''Get an OpenID consumer with session.'''
        return consumer.Consumer(self.getsession(environ), self.store)

    def response(self, message, env, url=''):
        '''Default response.'''
        # Set OpenID session cookie
        hdrs = [('Set-Cookie', self.setsession(env))]
        # Build message
        cmessage = (message, quote(self.buildurl(env, 'verify')), quote(url))
        return Response(cmessage, template=self.template, headers=hdrs)

    def redirect(self, environ, request):
        '''Redirect response.'''
        # Set OpenID session cookie
        hdrs = [('Set-Cookie', self.setsession(environ))]
        # Build redirect URL
        trust_root = environ['openid.baseurl']                
        return_to = self.buildurl(environ, 'process')
        redirect_url = request.redirectURL(trust_root, return_to)
        return Redirect(redirect_url, headers=hdrs)

    def getsession(self, environ):
        '''Return the existing session or a new session'''
        # Get value of cookie header that was sent
        sid = self.getsid(environ)
        # If a session id was not set, create a new one
        if sid is None:
            sid = randomString(16, '0123456789abcdef')
            session = None
        else:
            session = self.tracker.get(sid)
        # If no session exists for this session ID, create one
        if session is None:
            session = self.tracker[sid] = {}
            session['redirect'] = geturl(environ)
        session['id'] = sid        
        return session

    def getsid(self, environ):
        '''Returns a session identifier.'''
        # Fetch cookie
        cookie_str = environ.get('HTTP_COOKIE')        
        if cookie_str:
            cookie_obj = SimpleCookie(cookie_str)
            sid_morsel = cookie_obj.get(self.cname, None)
            # Get session id from cookie
            if sid_morsel is not None:
                sid = sid_morsel.value
            else:
                sid = None
        else:
            sid = None
        return sid

    def setsession(self, environ):
        '''Returns a session identifier.'''
        sid = self.getsession(environ)['id']
        return '%s=%s;' % (self.cname, sid)     