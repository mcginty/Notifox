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

import unittest
import wsgiform.validators as validators

class TestValidators(unittest.TestCase):

    def sixcheck(self, func, array):
        num = 0
        if func(array[0]): num += 1
        if func(array[1]): num += 1
        if func(array[2]): num += 1
        if not func(array[3]): num += 1
        if not func(array[4]): num += 1
        if not func(array[5]): num += 1   
        return num == 6

    def twocheck(self, func, array):
        num = 0
        if func(array[0]): num += 1
        if not func(array[1]): num += 1
        return num == 2

    def test_isascii(self):
        array = ('', u'')
        self.assertEqual(self.twocheck(validators.isascii, array), True)

    def test_isunicode(self):
        array = (u'', '')
        self.assertEqual(self.twocheck(validators.isunicode, array), True)

    def test_isfloat(self):
        array = ('4.133', '4')
        self.assertEqual(self.twocheck(validators.isfloat, array), True)

    def test_ismember(self):
        array = ['1', '2', '3', '4']
        self.assertEqual(validators.ismember('2', array), True)

    def test_inrange(self):
        self.assertEqual(validators.inrange('2', 1, 10), True)        

    def test_isnumber(self):
        array = ('4', 'a')
        self.assertEqual(self.twocheck(validators.isnumber, array), True)

    def test_isalpha(self):
        array = ('afafaeb', 'afaf3ae6b')
        self.assertEqual(self.twocheck(validators.isalpha, array), True)

    def test_isalphanum(self):
        array = ('afaf3ae6b', '.]}:"')
        self.assertEqual(self.twocheck(validators.isalphanum, array), True)

    def test_isspace(self):
        array = ('   ', '.]}:"')
        self.assertEqual(self.twocheck(validators.isspace, array), True)

    def test_istitle(self):
        array = ('Title', 'title')
        self.assertEqual(self.twocheck(validators.istitle, array), True)

    def test_isupper(self):
        array = ('TITLE', 'title')
        self.assertEqual(self.twocheck(validators.isupper, array), True)

    def test_islower(self):
        array = ('title', 'TITLE')
        self.assertEqual(self.twocheck(validators.islower, array), True)

    def test_islength(self):
        st = 'werwafeafe'
        self.assertEqual(validators.islength(st, 10), True)

    def test_isempty(self):
        array = (' ', 'eare')
        self.assertEqual(self.twocheck(validators.isempty, array), True)

    def test_malicious(self):
        array = ('http://www.domain.com/page.asp?param=&lt;/script&gt;',
        'https://www.domain.com/page.asp?param=;SELECT',
        'https://www.domain.com/page.asp?param=;INSERT',
        'https://www.domain.com/page.asp?param=RealParam',
        'https://www.domain.com/page.asp?param=RealParam1',         
        'https://www.domain.com/page.asp?param=RealParam2'        )
        self.assertEqual(self.sixcheck(validators.malicious, array), True)    

    def test_notmalicious(self):
        array = ('Normal input', 'This is a test', 'Test Test',
        'http://www.domain.com/page.asp?param=&lt;/script&gt;',
        'https://www.domain.com/page.asp?param=;SELECT',
        'https://www.domain.com/page.asp?param=;INSERT')        

    def test_isxml(self):
        array = ('<html><head></head><body></body></html>', '<html></head></body>')
        self.assertEqual(self.twocheck(validators.isxml, array), True)

    def test_isip4(self):
        array = ('0.0.0.0', '255.255.255.02', '192.168.0.136',
            '256.1.3.4', '023.44.33.22', '10.57.98.23.')
        self.assertEqual(self.sixcheck(validators.isip4, array), True)

    def test_isip6(self):
        array = ('::0:0:0:FFFF:129.144.52.38', 'FEDC:BA98::3210:FEDC:BA98:7654:3210',
            '::13.1.68.3', 'FEDC:BA98:7654:3210:FEDC:BA98:7654:3210:1234',
            '3210:FEDC:BA98:7654:3210:1234', ':FEDC:BA98:7654:3210:')
        self.assertEqual(self.sixcheck(validators.isip6, array), True)

    def test_ismacaddr(self):
        array = ('01:23:45:67:89:ab', '01:23:45:67:89:AB', 'fE:dC:bA:98:76:54',
            '01:23:45:67:89:ab:cd', '01:23:45:67:89:Az', '01:23:45:56:')
        self.assertEqual(self.sixcheck(validators.ismacaddr, array), True)

    def test_isemail(self):
        array = ('bob@smith.com', 'bob@j.smith.museum', 'bob.smith@a-1.smith.com',
            'bob@.com', 'bob@-a.smith.com', 'bob@-a.com')
        self.assertEqual(self.sixcheck(validators.isemail, array), True)

    def test_isurl(self):
        array = ('https://localhost', "https://64.81.85.161/site/file.php?cow=moo's",
            'ftp://user:pass@site.com:21/file/dir', 'sysrage.net', 'site.com',
            'http://site.com/dir//')
        self.assertEqual(self.sixcheck(validators.isurl, array), True)

    def test_isliveurl(self):
        array = ('http://www.python.org/', 'http://www.pythonorgy.org/')
        self.assertEqual(self.twocheck(validators.isliveurl, array), True)

    def test_ispassword(self):
        array = ('Passw0rd', 'assW@rd1', '1B2a345@#$%',
            '123123123', 'Password', 'asdf&amp;')
        self.assertEqual(self.sixcheck(validators.ispassword, array), True)

    def test_iszip(self):
        array = ('14467', '144679554', '14467-9554', '14467 955', '14467-', '1446-9554')
        self.assertEqual(self.sixcheck(validators.iszip, array), True)

    def test_isukpost(self):
        array = ('CF1 2AA', 'cf564fg', 'CC1 2AF', 'a1234d', 'A12 77Y', 'A12 77')
        self.assertEqual(self.sixcheck(validators.isukpost, array), True)
    
    def test_isnapost(self):
        array = ('00501', '84118-3423', 'n3a 3B7', '501-342', '123324', 'Q4B 5C5')
        self.assertEqual(self.sixcheck(validators.isnapost, array), True)

    def test_isprovince(self):
        array = ('ON', 'SK', 'QC', 'UT', 'ND', 'SD')
        self.assertEqual(self.sixcheck(validators.isprovince, array), True)

    def test_isstate(self):
        array = ('AL', 'CA', 'AA', 'New York', 'California', 'ny')
        self.assertEqual(self.sixcheck(validators.isstate, array), True)

    def test_isdatetime(self):
        array = ('12/25/2003', '08:03:31', '02/29/2004 12 AM',
            '02/29/2003 1:34 PM', '13:23 PM', '24:00:00')
        self.assertEqual(self.sixcheck(validators.isdatetime, array), True)

    def test_isedatetime(self):
        array = ('2003/12/25', '08:03:31', '2004/02/29 12 AM',
            '2003/02/29 1:34 PM', '13:23 PM', '24:00:00')

    def test_iscreditcard(self):
        array = ('341-1111-1111-1111', '5431-1111-1111-1111', '30569309025904',
            '30-5693-0902-5904', '5631-1111-1111-1111', '31169309025904')
        self.assertEqual(self.sixcheck(validators.iscreditcard, array), True)

    def test_isisbn(self):
        array = ('ISBN 0 93028 923 4', 'ISBN 1-56389-668-0', 'ISBN 1-56389-016-X',
            '123456789X', 'ISBN 9-87654321-2', 'ISBN 123 456-789X')
        self.assertEqual(self.sixcheck(validators.isisbn, array), True)

    def test_isssn(self):
        array = ('123-45-6789', '123 45 6789', '123456789', '12345-67-890123',
          '1234-56-7890', '123-45-78901')
        self.assertEqual(self.sixcheck(validators.isssn, array), True)     

    def test_isvat(self):
        array = ('CZ-7907111883', 'ESA12345678', 'FRAB123456789',
            'CZ55912', 'XY123456', 'FR-IB123456789')
        self.assertEqual(self.sixcheck(validators.isvat, array), True) 

    def test_isusd(self):
        array = ('$0.84', '$123458', '$1,234,567.89', '$12,3456.01', '12345', '$1.234')
        self.assertEqual(self.sixcheck(validators.isusd, array), True)   

    def test_isintlphone(self):
        array = ('+123(45)678-910', '+123-045-67 89 10', '01-234-56-78',
            '123(45)678 91011', '(12)345-678', '+0(12)345-6789')
        self.assertEqual(self.sixcheck(validators.isintlphone, array), True)  

    def test_isukphone(self):
        array = ('+447222555555', '+44 7222 555 555', '(0722) 5555555 #2222',
            '(+447222)555555', '+44(7222)555555', '(0722) 5555555 #22')
        self.assertEqual(self.sixcheck(validators.isukphone, array), True)

    def test_isusphone(self):
        array = ('987-654-3210 ', '(555) 487-1391 x652', 'phn (555) 987-6743 ext. 21012',
            '123 456-7890', '(555) 000-1111', '923-907')
        self.assertEqual(self.sixcheck(validators.isusphone, array), True)

    def test_isphone(self):
        array = ('1234567', '12345678', '(555) 987-6543 ext 210',
            '123456', '555-123', '434232')
        self.assertEqual(self.sixcheck(validators.isphone, array), True)

    def test_chainvalidate(self):
        chain = ('number', 'alphanum', ('range', 1, 15))
        self.assertEqual(validators.getvalidator(chain)('13'), True)

    def test_chainvalidatefalse(self):
        chain = ('number', 'alphanum', ('range', 1, 15))
        self.assertEqual(validators.getvalidator(chain)('13.3'), False)        

if __name__ == '__main__':
    unittest.main()
