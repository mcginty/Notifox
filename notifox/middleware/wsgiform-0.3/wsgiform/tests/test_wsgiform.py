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

'''Unit tests for wsgiform.'''

import wsgiform.form as wsgiform
from wsgiform.validators import getvalidator
import unittest
import StringIO
import copy

class TestWsgiForm(unittest.TestCase):
    
    '''Test cases for wsgiform.'''
        
    test_env = {
        'CONTENT_LENGTH': '118',
        'wsgi.multiprocess': 0,
        'wsgi.version': (1, 0),
        'CONTENT_TYPE': 'application/x-www-form-urlencoded',
        'SERVER_NAME': '127.0.0.1',
        'wsgi.run_once': 0,
        'wsgi.errors': StringIO.StringIO(),
        'wsgi.multithread': 0,
        'SCRIPT_NAME': '',
        'wsgi.url_scheme': 'http',
        'wsgi.input': StringIO.StringIO(
'num=12121&str1=test&name=%3Ctag+id%3D%22Test%22%3EThis+is+a+%27test%27+%26+another.%3C%2Ftag%3E&state=NV&Submit=Submit'
            ), 
        'REQUEST_METHOD': 'POST',
        'HTTP_HOST': '127.0.0.1',
        'PATH_INFO': '/',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.0'}       

    def dummy_app(self, environ, func):
        return environ

    def dummy_sr(self, status, headers, exc_info=None):
        pass

    def test_fieldstorage(self):
        '''Parses form data into a FieldStorage instance.'''
        form = wsgiform.WsgiForm(self.dummy_app, style='fieldstorage')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.fieldstorage'].getfirst('num'), '12121')

    def test_dictionary(self):
        '''Parses form data into a dictionary.'''
        form = wsgiform.WsgiForm(self.dummy_app, style='dict')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['num'], '12121')

    def test_kwargs(self):
        '''Parses form data into keyword arguments.'''
        form = wsgiform.WsgiForm(self.dummy_app, style='kwargs')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgize.kwargs']['num'], '12121')

    def test_environ(self):
        '''Parses form data into individual environ entries.'''
        form = wsgiform.WsgiForm(self.dummy_app, style='environ')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.num'], '12121')

    def test_escape(self):
        '''Parses form data into a dictionary with HTML escaping. '''
        form = wsgiform.WsgiForm(self.dummy_app)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&lt;tag id=&quot;Test&quot;&gt;This is a &#39;test&#39; &amp; another.&lt;/tag&gt;')

    def test_hyperescape(self):
        '''Parses form data into a dictionary with HTML hyperescaping. '''
        form = wsgiform.WsgiForm(self.dummy_app, func='hyperescape')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&#60;tag id&#61;&#34;Test&#34;&#62;This is a &#39;test&#39; &#38; another.&#60;&#47;tag&#62;')                 

    def test_strictescape(self):
        '''Parses form data into a dictionary with strict HTML escaping.'''
        form = wsgiform.WsgiForm(self.dummy_app, strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&lt;tag id=&quot;Test&quot;&gt;This is a &#39;test&#39; &amp; another.&lt;/tag&gt;')

    def test_stricthyperescape(self):
        '''Parses form data into a dictionary with strict HTML hyperescaping.'''
        form = wsgiform.WsgiForm(self.dummy_app, func='hyperescape', strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], '&#60;tag id&#61;&#34;Test&#34;&#62;This is a &#39;test&#39; &#38; another.&#60;&#47;tag&#62;')        

    def test_sterilize(self):
        '''Parses form data into a dictionary with data sterilization.'''
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize')
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_strictsterilize(self):
        '''Parses form data into a dictionary with strict data sterilization.'''
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', strict=True)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_validation(self):
        '''Tests data validation.'''
        vdict = {'num':getvalidator(('number', ('range', 10000, 15000)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', validators=vdict)
        env = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(env['wsgiform.dict']['name'], 'tag idTestThis is a test  another.tag')

    def test_validation_false(self):
        '''Tests bad data validation.'''
        vdict = {'num':getvalidator(('float', ('range', 1000, 1500)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', validators=vdict)
        iteble = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(iteble[0], 'Data in field(s) num was invalid.')        

    def test_validation_strict(self):    
        '''Tests strict data validation.'''
        vdict = {'num':getvalidator(('number', ('range', 10000, 15000)))}
        form = wsgiform.WsgiForm(self.dummy_app, func='sterilize', strict=True, validators=vdict)
        iteble = form(copy.deepcopy(self.test_env), self.dummy_sr)
        self.assertEqual(iteble[0], 'Data in field(s) str1 name Submit state was invalid.')        
    

if __name__ == '__main__': unittest.main()