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

'''Persistent authentication tokens in URL query components.'''

import cgi
from wsgiauth.base import BaseAuth
from wsgiauth.util import Redirect, geturl

__all__ = ['URLAuth', 'urlauth']

def urlauth(authfunc, **kw):
    '''Decorator for persistent authentication tokens in URLs.'''
    def decorator(application):
        return URLAuth(application, authfunc, **kw)
    return decorator


class URLAuth(BaseAuth):

    '''Persists authentication tokens in URL query components.'''    

    authtype = 'url'

    def __init__(self, application, authfunc, **kw):
        super(URLAuth, self).__init__(application, authfunc, **kw)
        # Redirect method
        self.redirect = kw.get('redirect', Redirect)

    def authenticate(self, environ):
        '''Authenticates a token embedded in a query component.'''
        try:            
            query = cgi.parse_qs(environ['QUERY_STRING'])
            return self._authtoken(environ, query[self.name][0])
        except KeyError:
            return False
        
    def generate(self, env):
        '''Embeds authentication token in query component.'''
        env['QUERY_STRING'] = '='.join([self.name, self._gettoken(env)])

    def initial(self, environ, start_response):
        # Embed auth token
        self.generate(environ)
        # Redirect to requested URL with auth token in query string
        redirect = self.redirect(geturl(environ))
        return redirect(environ, start_response)     