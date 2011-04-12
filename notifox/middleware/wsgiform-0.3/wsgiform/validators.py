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

'''Form validation utilities.'''

import re, urllib
from xml.dom.expatbuilder import parseString

# Specialized regexes
_patterns = {
# US Social Security Number - Dennis Flynn - regexlib.com 
'ssn':r'(^|\s)(00[1-9]|0[1-9]0|0[1-9][1-9]|[1-6]\d{2}|7[0-6]\d|77[0-2])(-?|[\. ])([1-9]0|0[1-9]|[1-9][1-9])\3(\d{3}[1-9]|[1-9]\d{3}|\d[1-9]\d{2}|\d{2}[1-9]\d)($|\s|[;:,!\.\?])',
# US currency checker - Michael Ash - regexlib.com
'usd':r'^\$(\d{1,3}(\,\d{3})*|(\d+))(\.\d{2})?$',
# MAC Address - Ted Rudyk - regexlib.com 
'macaddr':r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$',
# IP4 address - Andrew Polshaw - regexlib.com
'ip4':r'^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$',
# IP6 address - Glynn Beeken - regexlib.com
'ip6':r'^(^(([0-9A-F]{1,4}(((:[0-9A-F]{1,4}){5}::[0-9A-F]{1,4})|((:[0-9A-F]{1,4}){4}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,1})|((:[0-9A-F]{1,4}){3}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,2})|((:[0-9A-F]{1,4}){2}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,3})|(:[0-9A-F]{1,4}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,4})|(::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,5})|(:[0-9A-F]{1,4}){7}))$|^(::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,6})$)|^::$)|^((([0-9A-F]{1,4}(((:[0-9A-F]{1,4}){3}::([0-9A-F]{1,4}){1})|((:[0-9A-F]{1,4}){2}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,1})|((:[0-9A-F]{1,4}){1}::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,2})|(::[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,3})|((:[0-9A-F]{1,4}){0,5})))|([:]{2}[0-9A-F]{1,4}(:[0-9A-F]{1,4}){0,4})):|::)((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{0,2})\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{0,2})$$',
# Complex password enforcer 1 upper 1 lower 1 num 1 special min/max - Matthew Hazzard - regexlib.com
'password':r'(?=^.{8,255}$)((?=.*\d)(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[a-z])|(?=.*[^A-Za-z0-9])(?=.*[A-Z])(?=.*[a-z])|(?=.*\d)(?=.*[A-Z])(?=.*[^A-Za-z0-9]))^.*',
# US state abbreviations - Michael Ash - regexlib.com
'usstates':r'^(A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$',
# Canada provice abbeviations - Matthew Hartman - regexlib.com
'canada':r'^(N[BLSTU]|[AMN]B|[BQ]C|ON|PE|SK)$',
# Credit Card - David Conorozzo - regexlib.com
'creditcard':r'^3(?:[47]\d([ -]?)\d{4}(?:\1\d{4}){2}|0[0-5]\d{11}|[68]\d{12})$|^4(?:\d\d\d)?([ -]?)\d{4}(?:\2\d{4}){2}$|^6011([ -]?)\d{4}(?:\3\d{4}){2}$|^5[1-5]\d\d([ -]?)\d{4}(?:\4\d{4}){2}$|^2014\d{11}$|^2149\d{11}$|^2131\d{11}$|^1800\d{11}$|^3\d{15}$',
# Malice detection - Shahar Bracha - regexlib.com
'malice':r'(script)|(&lt;)|(&gt;)|(%3c)|(%3e)|(SELECT)|(UPDATE)|(INSERT)|(DELETE)|(GRANT)|(REVOKE)|(UNION)|(&amp;lt;)|(&amp;gt;)',
# Malice protection - Brenden Salta - regexlib.com
'notmalice':r'^[^<>`~!/@\#}$%:;)(_^{&*=|\'+]+$',
# Email - Shaune Stark - regexlib.com
'email':r'^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@(([0-9a-zA-Z])+([-\w]*[0-9a-zA-Z])*\.)+[a-zA-Z]{2,9})$',
# URL - Brian Bothwell - regexlib.com
'url':r'^(file|ftp|gopher|hdl|http|https|imap|mailto|mms|news|nntp|prospero|rsync|rtsp|rtspu|shttp|sip|snews|svn|svn+ssh|telnet|wais)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\?\'\\\+&amp;%\$#\=~_\-]+))*$',
# DateTime mm/dd/yyyy hh:MM:ss - Michael Ash - regexlib.com
'datetime':r'(?=\d)^(?:(?!(?:10\D(?:0?[5-9]|1[0-4])\D(?:1582))|(?:0?9\D(?:0?[3-9]|1[0-3])\D(?:1752)))((?:0?[13578]|1[02])|(?:0?[469]|11)(?!\/31)(?!-31)(?!\.31)|(?:0?2(?=.?(?:(?:29.(?!000[04]|(?:(?:1[^0-6]|[2468][^048]|[3579][^26])00))(?:(?:(?:\d\d)(?:[02468][048]|[13579][26])(?!\x20BC))|(?:00(?:42|3[0369]|2[147]|1[258]|09)\x20BC))))))|(?:0?2(?=.(?:(?:\d\D)|(?:[01]\d)|(?:2[0-8])))))([-.\/])(0?[1-9]|[12]\d|3[01])\2(?!0000)((?=(?:00(?:4[0-5]|[0-3]?\d)\x20BC)|(?:\d{4}(?!\x20BC)))\d{4}(?:\x20BC)?)(?:$|(?=\x20\d)\x20))?((?:(?:0?[1-9]|1[012])(?::[0-5]\d){0,2}(?:\x20[aApP][mM]))|(?:[01]\d|2[0-3])(?::[0-5]\d){1,2})?$',
# DateTime yyyy/mm/dd hh:MM:ss - Michael Ash - regexlib.com
'eurodatetime':r'^(?=\d)(?:(?!(?:1582(?:\.|-|\/)10(?:\.|-|\/)(?:0?[5-9]|1[0-4]))|(?:1752(?:\.|-|\/)0?9(?:\.|-|\/)(?:0?[3-9]|1[0-3])))(?=(?:(?!000[04]|(?:(?:1[^0-6]|[2468][^048]|[3579][^26])00))(?:(?:\d\d)(?:[02468][048]|[13579][26]))\D0?2\D29)|(?:\d{4}\D(?!(?:0?[2469]|11)\D31)(?!0?2(?:\.|-|\/)(?:29|30))))(\d{4})([-\/.])(0?\d|1[012])\2((?!00)[012]?\d|3[01])(?:$|(?=\x20\d)\x20))?((?:(?:0?[1-9]|1[012])(?::[0-5]\d){0,2}(?:\x20[aApP][mM]))|(?:[01]\d|2[0-3])(?::[0-5]\d){1,2})?$',
# US Phone - Tim N Tousley - regexlib.com 
'usphone':r'^([a-zA-Z,#/ \.\(\)\-\+\*]*[2-9])([a-zA-Z,#/ \.\(\)\-\+\*]*[0-9]){2}([a-zA-Z,#/ \.\(\)\-\+\*]*[2-9])([a-zA-Z,#/ \.\(\)\-\+\*]*[0-9]){6}[0-9a-zA-Z,#/ \.\(\)\-\+\*]*$',
# UK Phone - Amos Hurd - regexlib.com 
'ukphone':r'(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$',
# International phone - Dmitry Kandiner - regexlib.com
'intlphone':r'^(\+[1-9][0-9]*(\([0-9]*\)|-[0-9]*-))?[0]?[1-9][0-9\- ]*$',
# Phone checker - Tim N Tousley - regexlib.com 
'phone':r'^([a-zA-Z,#/ \.\(\)\-\+\*]*[0-9]){7}[0-9a-zA-Z,#/ \.\(\)\-\+\*]*$',
# US-Canada postal/zip codes - Matthew Aznoe - regexlib.com 
'napost':r'^((\d{5}-\d{4})|(\d{5})|([AaBbCcEeGgHhJjKkLlMmNnPpRrSsTtVvXxYy]\d[A-Za-z]\s?\d[A-Za-z]\d))$',
# US Zip codes 5+4 +/- hyphen
'zip':r'(^\d{5}$)|(\d{5}-*\d{4}$)',
# UK postal codes - Scott Pite - regexlib.com
'ukpost':r'^[A-Za-z]{1,2}[\d]{1,2}([A-Za-z])?\s?[\d][A-Za-z]{2}$',
# ISBN - Michael Ash - regexlib.com
'isbn':r'ISBN\x20(?=.{13}$)\d{1,5}([- ])\d{1,7}\1\d{1,6}\1(\d|X)$',
# Number checker - Paul Auger - regexlib.com
'num':r'^((\d?)|(([-+]?\d+\.?\d*)|([-+]?\d*\.?\d+))|(([-+]?\d+\.?\d*\,\ ?)*([-+]?\d+\.?\d*))|(([-+]?\d*\.?\d+\,\ ?)*([-+]?\d*\.?\d+))|(([-+]?\d+\.?\d*\,\ ?)*([-+]?\d*\.?\d+))|(([-+]?\d*\.?\d+\,\ ?)*([-+]?\d+\.?\d*)))$',
# Euro VAT - Michal Valasek - regexlib.com
'vat':r'((DK|FI|HU|LU|MT|SI)(-)?\d{8})|((BE|EE|DE|EL|LT|PT)(-)?\d{9})|((PL|SK)(-)?\d{10})|((IT|LV)(-)?\d{11})|((LT|SE)(-)?\d{12})|(AT(-)?U\d{8})|(CY(-)?\d{8}[A-Z])|(CZ(-)?\d{8,10})|(FR(-)?[\dA-HJ-NP-Z]{2}\d{9})|(IE(-)?\d[A-Z\d]\d{5}[A-Z])|(NL(-)?\d{9}B\d{2})|(ES(-)?[A-Z\d]\d{7}[A-Z\d])',
}

patterns = dict((k, re.compile(v)) for k, v in _patterns.iteritems())

def getvalidator(chain):
    '''Returns a chained validator.

    @param chain List of validator names.
    '''
    return ChainValidator(chain)

def _validate(key, data):
    '''Validates data by key.'''
    if patterns[key].search(data): return True
    return False

# Member

def ismember(data, members):
    '''Validates data is a member.'''
    return data in members

def inrange(data, start, stop):
    '''Validates data falls within a numeric range.'''
    return int(data) in range(start, stop)

# Character
    
def isascii(data):
    '''Validates data is ASCII'''
    return isinstance(data, str)

def isunicode(data):
    '''Validates data is unicode.'''
    return isinstance(data, unicode)

def isnumber(data):
    '''Validates data is number.'''
    return data.isdigit()

def isfloat(data):
    '''Validates data is a float.'''
    # Make sure not int
    try:
        int(data)
    except ValueError:
        return isinstance(float(data), float)

def isalpha(data):
    '''Validates data is all alphabetical.'''   
    return data.isalpha()

def isalphanum(data):
    '''Validates data is alphanumeric.'''
    return data.isalnum()

def isspace(data):
    '''Validates data is all spaces.'''
    return data.isspace()

def istitle(data):
    '''Validates data is in title form.'''
    return data.istitle()

def isupper(data):
    '''Validates data is uppercase.'''
    return data.isupper()

def islower(data):
    '''Validates data is lowercase.'''
    return data.islower()

def islength(data, length):
    '''Validates data is under or equals a defined length.'''
    return len(data) <= length

def isempty(data):
    '''Validates data is empty.'''
    return data.strip() == ''

# User submissions

def malicious(data):
    '''Validates that data has certain potentially malicious content.'''
    return _validate('malice', data)

def notmalicious(data):
    '''Validates that data does not have certain potentially malicious content.'''
    return _validate('notmalice', data)

def isxml(data):
    '''Validates data is well-formed XML.'''
    try:
        parseString(data)
    except:
        return False
    return True

# Network Addresses

def isip4(data):
    '''Validates data is a valid IPv4 address.'''
    return _validate('ip4', data)

def isip6(data):
    '''Validates data is a valid IPv6 address.'''
    return _validate('ip6', data)

def ismacaddr(data):
    '''Validates data is a valid MAC address.'''
    return _validate('macaddr', data)

def isemail(data):
    '''Validates data is a valid email address.'''
    return _validate('email', data)

def isurl(data):
    '''Validates data is a valid URL.'''
    return _validate('url', data)

def isliveurl(data):
    '''Validates data is a live URL.'''
    try:
        urllib.urlopen(data)
    except:
        return False
    return True

# Username/password

def ispassword(data):
    '''Validates that data is a password with 1 upper 1 lower 1 num
    1 and at least 8 characters.
    '''
    return _validate('password', data)

# Postal codes

def iszip(data):
    '''Validates data is a valid US ZIP code.'''
    return _validate('zip', data)

def isukpost(data):
    '''Validates data is a valid UK postal code.'''
    return _validate('ukpost', data)

def isnapost(data):
    '''Validates data is a US ZIP or Canadian postal code.'''
    return _validate('napost', data)

# Territory names

def isprovince(data):
    '''Validates data is a valid Canadian provincial abbreviation.'''
    return _validate('canada', data)

def isstate(data):
    '''Validates that data is a US state abbreviation.'''
    return _validate('usstates', data)

# Date time

def isdatetime(data):
    '''Validates data is a valid format for mm/dd/yyyy hh:MM:ss.'''
    return _validate('datetime', data)

def isedatetime(data):
    '''Validates data is a valid format for yyyy/mm/dd hh:MM:ss.'''
    return _validate('eurodatetime', data)

# Numbers

def iscreditcard(data):
    '''Validates data is a valid format for a credit card number.'''
    return _validate('creditcard', data)

def isisbn(data):
    '''Validates data is ISBN.'''
    return _validate('isbn', data)

def isssn(data):
    '''Validates that data is a social security number.'''
    return _validate('ssn', data)

def isvat(data):
    '''Validates that data is a EU VAT number.'''
    return _validate('vat', data)

def isusd(data):
    '''Validates that data is a UK phone number.'''
    return _validate('usd', data)

# Phone numbers

def isphone(data):
    '''Validates that data is a phone number.'''
    return _validate('phone', data)

def isukphone(data):
    '''Validates that data is a UK phone number.'''
    return _validate('ukphone', data)

def isintlphone(data):
    '''Validates that data is an international phone number.'''
    return _validate('intlphone', data)

def isusphone(data):
    '''Validates that data is a US phone number.'''
    return _validate('usphone', data)

# Registry of validators
validators = dict(members=ismember, range=inrange, ascii=isascii,
    unicode=isunicode, number=isnumber, float=isfloat, alpha=isalpha,
    alphanum=isalphanum, space=isspace, cap=istitle, upper=isupper,
    lc=islower, length=islength, empty=isempty, malice=malicious,
    notmalice=notmalicious, xml=isxml, ip4=isip4, ip6=isip6,
    macaddr=ismacaddr, email=isemail, url=isurl, liveurl=isliveurl,
    password=ispassword, zip=iszip, ukpost=isukpost, napost=isnapost,
    province=isprovince, state=isstate, datetime=isdatetime, 
    edatetime=isedatetime, creditcard=iscreditcard, isbn=isisbn,
    ssn=isssn, vat=isvat, usd=isusd, phone=isphone, ukphone=isukphone,
    intlphone=isintlphone, usphone=isusphone)


class ChainValidator(object):

    '''Class to build a chain of validators'''    

    def __init__(self, chain):
        self.chain = chain

    def __call__(self, data):
        '''Validates against a chain of validating functions.'''
        for v in self.chain:
            # Load validator
            if not isinstance(v, basestring):
                validator = validators[v[0]]
            else:
                validator = validators[v]
            # One validation failure invalidates the entire chain
            try:
                if len(v) == 3:
                    if not validator(data, v[1], v[2]): return False
                elif len(v) == 2:
                    if not validator(data, v[1]): return False
                else:
                    if not validator(data): return False
            # Any exceptions cause validation failure
            except:
                return False
        return True