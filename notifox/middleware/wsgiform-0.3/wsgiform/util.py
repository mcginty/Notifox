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

'''Utilities for server-side form processing.'''

import cgi
import re
import string
from StringIO import StringIO
from xml.sax import saxutils

__all__ = ['hyperescape', 'escape', 'sterilize', 'escapeform', 'hyperform',
    'sterileform']

_trans = string.maketrans('', '')

def getinput(environ):
    '''Non-destructively retrieves wsgi.input value.'''
    wsginput = environ['wsgi.input']
    # Non-destructively fetch string value of wsgi.input
    if hasattr(wsginput, 'getvalue'):
        qs = wsginput.getvalue()
    # Otherwise, read and reconstruct wsgi.input
    else:
        # Never read more than content length
        clength = int(environ['CONTENT_LENGTH'])
        qs = wsginput.read(clength)
        environ['wsgi.input'] = StringIO(qs)
    return qs

def formparse(environ, strict=False):
    '''Stores data from form submissions in a dictionary.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    '''
    qdict = cgi.parse(StringIO(getinput(environ)), environ, strict, strict)
    # Remove invididual entries from list and store as naked string
    for key, value in qdict.iteritems():
        if len(value) == 1: qdict[key] = value[0]
    return qdict

def _runfunc(qdict, func):
    '''Runs a function on a dictionary.

    @param qdict Dictionary
    @param func Function
    '''
    # Handle single entries
    for key, value in qdict.iteritems():
        if isinstance(value, basestring):
            qdict[key] = func(value)
        # Handle lists
        elif isinstance(value, list):
            for num, item in enumerate(value):
                if isinstance(item, basestring): value[num] = func(item)
    return qdict

def escape(data):
    '''Escapes &, <, >, ", and ' with HTML entities.

    @param data Text data
    '''
    return saxutils.escape(data, {'"':"&quot;", "'":'&#39;'})

def escapeform(environ, strict=False):
    '''Escapes common XML/HTML entities in form data.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    '''    
    return _runfunc(formparse(environ, strict), escape)

def hyperescape(data):
    '''Escapes punctuation with HTML entities except ., -, and _.

    @param data Text data
    '''
    # Escape &
    data = re.sub(r'&(?!#\d\d;)', '&#38;', data)
    # Escape ;
    data = re.sub(r'(?<!&#\d\d);', '&#59;', data)
    # Escape #
    data = re.sub(r'(?<!&)#(?!\d\d;)', '&#35;', data)
    # Escape other chars except ., -, and _
    for char in '<>"\'()!${}*+,%/:=?@[\\]^`|~':
        data = data.replace(char, '&#%d;' % ord(char))
    return data

def hyperform(environ, strict=False):
    '''Hyper-escapes all XML/HTML entitites in form data.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    '''    
    return _runfunc(formparse(environ, strict), hyperescape) 

def sterileform(environ, strict=False):
    '''Removes all form data characters except alphanumerics, ., -, and _.

    @param environ Environment dictionary
    @param strict Stops on errors (default: False)
    '''
    return _runfunc(formparse(environ, strict), sterilize)

def sterilize(data):
    '''Removes all ASCII characters except alphanumerics, ., -, and _.

    @param data Text data
    '''
    return data.translate(_trans, '&#;<>"\'()!${}*+,%/:=?@[\\]^`|~')