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

'''WSGI middleware for persistent authentication tokens in cookies.'''

from Cookie import SimpleCookie
from wsgiauth.base import BaseAuth

__all__ = ['Cookie', 'cookie']


def cookie(authfunc, **kw):
    '''Decorator for persistent authentication tokens in cookies.'''
    def decorator(application):
        return Cookie(application, authfunc, **kw)
    return decorator


class Cookie(BaseAuth):

    '''Persists authentication tokens in HTTP cookies.'''    

    authtype = 'cookie'

    def __init__(self, application, authfunc, **kw):
        super(Cookie, self).__init__(application, authfunc, **kw)
        # Cookie domain
        self.domain = kw.get('domain')
        # Cookie age
        self.age = kw.get('age', 7200)
        # Cookie path, comment
        self.path, self.comment = kw.get('path', '/'), kw.get('comment')    
        
    def authenticate(self, environ):
        '''Authenticates a token embedded in a cookie.'''
        try:
            cookies = SimpleCookie(environ['HTTP_COOKIE'])
            scookie = cookies[self.name]
            auth = self._authtoken(environ, scookie.value)
            # Tell user agent to expire cookie if invalid
            if not auth:
                scookie[scookie.value]['expires'] = -365*24*60*60
                scookie[scookie.value]['max-age'] = 0
            return auth
        except KeyError:
            return False

    def generate(self, environ):
        '''Returns an authentication token embedded in a cookie.'''
        scookie = SimpleCookie()
        scookie[self.name] = self._gettoken(environ)
        scookie[self.name]['path'] = self.path
        scookie[self.name]['max-age'] = self.age
        if self.domain is not None:
            scookie[self.name]['domain'] = self.domain
        if self.comment is not None:
            scookie[self.name]['comment'] = self.comment
        # Mark cookie as secure if using SSL
        if environ['wsgi.url_scheme'] == 'https':
            scookie[self.name]['secure'] = ''
        return scookie[self.name].OutputString()

    def initial(self, environ, start_response):
        '''Initial response to a request.'''
        def cookie_response(status, headers, exc_info=None):
            headers.append(('Set-Cookie', self.generate(environ)))
            return start_response(status, headers, exc_info)
        return self.application(environ, cookie_response)