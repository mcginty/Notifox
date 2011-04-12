# Copyright (c) 2006 L. C. Rees
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of WsgiForm nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''WSGI middleware for validating form submissions and parsing them into
dictionaries, individual WSGI 'environ' dictionary entries, cgi.FieldStorage
instances, or keyword arguments passed to a WSGI application. Supports
automatically escaping and sterilizing form submissions.
'''

import cgi
import urllib
from StringIO import StringIO
from wsgiform.util import escapeform, hyperform, sterileform, getinput

__all__ = ['WsgiForm', 'form']

def _errorapp(environ, start_response):
    '''Default error handler for form validation errors.

    Replace with custom handler.
    '''
    start_response('200 OK', ('Content-type', 'text/plain'))
    return ['Data in field(s) %s was invalid.' %
            ' '.join(environ['wsgiform.error'])]

def validate(qdict, validators, environ, strict=False):
    '''Validates form data.

    qdict Dictionary of validators where the key is a form field
    environ A WSGI environment dictionary
    validators An iterable with validators
    strict Keys w/out validators are form errors (default: False)
    '''
    errors = []
    # Validate each form entry
    for key, value in qdict.iteritems():
        try:
            # Accumulate any errors
            if not validators[key](value): errors.append(key)
        except KeyError:
            if strict: errors.append(key)
    # Put any errors in environ error entry and fail
    if errors:
        environ['wsgiform.error'] = errors
        return False        
    return True

def form(**kw):
    '''Decorator for form parsing.'''
    def decorator(application):
        return WsgiForm(application, **kw)
    return decorator
    

class WsgiForm(object):

    '''Class that parses form data into dictionaries, individual 'environ'
    entries, FieldStorage instances, or keyword arguments that can be passed to
    WSGI applications in the environ dictionary.
    '''
    
    environ = None
    # Environ key styles
    keys = {'fieldstorage':'wsgiform.fieldstorage', 'dict':'wsgiform.dict',
        'kwargs':'wsgize.kwargs', 'environ':'wsgiform.%s',
        'routing_args':'wsgiorg.routing_args'}
    # Data sterilizing functions
    funclist = {'escape':escapeform, 'hyperescape':hyperform,
        'sterilize':sterileform} 

    def __init__(self, application, **kw):
        self.application = application
        # Style and key for form data passing format
        self.style = kw.get('style', 'dict')
        self.key = self.keys.get(self.style)
        # Dictionary of validating functions where keywords == form field names 
        self.validators = kw.get('validators', {})
        # Function to validate form submissions
        self.validate = kw.get('validfunc', validate)
        # WSGI application to handle form validation errors
        self.handler = kw.get('errapp', _errorapp)
        # Stop on errors, empty fields, and validation errors
        self.strict = kw.get('strict', False)
        # Function to escape metachars
        self.func = self.funclist[(kw.get('func', 'escape'))]
        
    def __call__(self, env, start_response):       
        qdict = self.func(env, self.strict)            
        # Validate form if validators present            
        if self.validators:
            if not self.validate(qdict, self.validators, env, self.strict):
                return self.handler(env, start_response)
        if self.style == 'fieldstorage':
            # Reparse query back into a query string
            cginput = StringIO(urllib.urlencode(qdict))
            # Put into cgi.FieldStorage instance
            qdict = cgi.FieldStorage(fp=cginput, environ=env)
        # Store form submissions as individual environ entries
        if self.style == 'environ':
            for k, v in qdict.iteritems(): env[self.key % k] = v
        # Store form submissions using wsgi.routing_vars style
        elif self.style == 'routing_args':
            args, kwargs = env.get(self.key, ((), {}))
            env[self.key] = (args, kwargs.update(qdict))
        # Store form submissions as kwargs, dict, or cgi.FieldStorage
        else:
            env[self.key] = qdict
        return self.application(env, start_response)