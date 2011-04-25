# Creeper for Notifox
# @author Jake McGinty <mcginty@illinois.edu>
from datetime import datetime, date, time, timedelta

import threading
import urllib # unquote
import urllib2 # for requests
import lxml # tree parsing
import lxml.html
from lxml.html import tostring

from notifox.model.meta import Session, Base
from notifox.model.page import Page
from notifox.model.user import User

from exceptions import NoXPathException

class Creeper(threading.Thread):
    def __init__(self, page):
        self.page = page
        threading.Thread.__init__(self)

    def run(self):
        if (datetime.utcnow() - self.page.last_crawled) < timedelta(seconds=20):
            sleep(10)
            return
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Notifox/0.1dev')]
            f = opener.open(self.page.url)
            tree = lxml.html.fromstring(f.read())
            chunk = tree.xpath(self.page.xpath, pretty_print=True)
            self.page.content = tostring(chunk[0])
            self.page.last_crawled = datetime.utcnow()
            print "Updated: %s" % self.page.url
            if len(chunk) <= 0:
                raise NoXPathException(self.page.xpath)
        except IOError:
            print "Could not open url: %s" % self.page.url
