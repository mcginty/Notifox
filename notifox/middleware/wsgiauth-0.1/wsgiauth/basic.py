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

'''HTTP Basic Authentication

This module implements basic HTTP authentication as described in
HTTP 1.0:

http://www.w3.org/Protocols/HTTP/1.0/draft-ietf-http-spec.html#BasicAA
'''

from wsgiauth.base import Scheme, HTTPAuth

__all__ = ['basic']

def basic(realm, authfunc, **kw):
    '''Decorator for HTTP basic authentication.'''
    def decorator(application):
        return HTTPAuth(application, realm, authfunc, BasicAuth, **kw)
    return decorator


class BasicAuth(Scheme):

    '''Performs HTTP basic authentication.'''

    authtype = 'basic'

    def _response(self, environ, start_response):
        '''Default HTTP basic authentication response.'''
        # Send 401 response + realm
        start_response('401 Unauthorized',
            [('content-type', 'text/plain'),
            ('WWW-Authenticate', 'Basic realm="%s"' % self.realm)])
        return [self.message]

    def __call__(self, environ):
        # Check authorization
        authorization = environ.get('HTTP_AUTHORIZATION')
        # Request credentials if no authorization
        if authorization is None: return self.response
        # Verify scheme
        authmeth, auth = authorization.split(' ', 1)
        if authmeth.lower() != 'basic': return self.response
        # Get username, password
        auth = auth.strip().decode('base64')
        username, password = auth.split(':', 1)
        # Authorize user
        if self.authfunc(environ, username, password): return username
        return self.response