# (c) 2005 Ian Bicking and contributors; written for Paste
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

'''Authenticate an IP address.'''

from wsgiauth.util import Forbidden

__all__ = ['IP', 'ip']

def ip(authfunc, **kw):
    '''Decorator for IP address-based authentication.'''
    def decorator(application):
        return IP(application, authfunc, **kw)
    return decorator


class IP(object):

    '''On each request, `REMOTE_ADDR` is authenticated and access allowed based
    on IP address.
    '''

    def __init__(self, app, authfunc, **kw):
        self.app, self.authfunc = app, authfunc
        self.response = kw.get('response', Forbidden())

    def __call__(self, environ, start_response):
        ipaddr = environ.get('REMOTE_ADDR')
        if not self.authfunc(environ, ipaddr):
            return self.response(environ, start_response)            
        return self.app(environ, start_response)