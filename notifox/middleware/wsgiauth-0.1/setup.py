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

'''setup - setuptools based setup for wsgiauth.'''

import ez_setup
ez_setup.use_setuptools()

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name='wsgiauth',
      version='0.1',
      description='''WSGI authentication middleware.''',
      long_description='''WSGI authentication middleware that supports HTTP basic
      and digest authentication, IP authentication, and form-based or OpenID
      authentication using signed cookies or URL query parameters.''',
      author='L. C. Rees',
      author_email='lcrees@gmail.com',
      license='MIT',
      packages = ['wsgiauth'],
      zip_safe = True,
      keywords='WSGI dispatch middleware web HTTP decorators',
      classifiers=['Development Status :: 3 - Alpha',
                    'Environment :: Web Environment',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware'])