# Creeper for Notifox
# @author Jake McGinty <mcginty@illinois.edu>

import threading
import urllib # unquote
import urllib2 # for requests
import lxml # tree parsing

from notifox.model.meta import Session, Base
from notifox.model.page import Page
from notifox.model.user import User

from creeper.exceptions import NoXPathException

Errors = enum('NoSuchXPath')

class Creeper(threading.Thread):
    def __init__(self, page):
        self.page = page
        self.result = None
        threading.Thread.__init__(self)

        def get_result(self):
            return self.result
        
        def run(self):
            try:
                opener = urllib2.build_opener()
                opener.addheaders[('User-agent', 'Notifox/0.1dev')]
                f = opener.open(self.page.url)
                tree = lxml.html.fromstring(f.read())
                chunk = tree.xpath(self.page.xpath, pretty_print=True)
                if len(chunk) <= 0:
                    raise NoXPathException(self.page.xpath)
            except IOError:
                print "Could not open url: %s" % self.page.url
