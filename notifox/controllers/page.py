import logging

# HTML/XTree parsing libraries
import urllib, urllib2
import re
import lxml.html
from lxml import etree
from lxml.html.soupparser import fromstring
#from lxml.etree import tostring
from lxml.html import tostring

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import BaseController, render

"""
'   Dataflows:
'       * GET[link] -> add() -> selected() -> list()
'       * list()
"""

log = logging.getLogger(__name__)
absolute_url = "http://localhost:5000"

def add_base_href(content, link):
    """
    Locate the <head> tag, and insert our base tag.
    <base> tells the browser to use that path for relative links over the current URI.
    """
    try:
        root = lxml.html.fromstring(content)
        if root.find('html') != None:
            head = root.find('html').find('head')
        else:
            head = root.find('head')
        base = etree.Element("base")
        base.set("href", link)
        base.text = "a"
        head.insert(0, base)
    except Exception as detail:
        raise Exception(detail)
    return tostring(root)

def add_js(content, link):
    """
    Insert JavaScript for our node selector at the end of the body.
    """
    try:
        root = lxml.html.fromstring(content)
        settings = etree.Element("script")
        settings.text = ' \n \
            nodeselector = {}; \n \
            nodeselector.ns = {}; \n \
            nodeselector.ns.doneURL = "'+absolute_url+'/selected/"; \n \
            nodeselector.ns.initURL = "'+urllib.quote_plus(link)+'";\n'

        nsjs = etree.Element("script", src=absolute_url+'/ns.js')
        root.append(settings)
        root.append(nsjs)
    except Exception as detail:
        raise Exception(detail)
    return tostring(root)

class PageController(BaseController):

    def index(self):
        # Return a rendered template
        return render('/derived/page/page.mako')

    def add(self):
        """
        Linked is passed all pretty-like into this function, which slips in our helper code in the requested website.
        All the rest of the work is done client-side with our ns.js (nodeSelector library), which returns XPath.

        next in line: selected()
        """
        link = request.params['q']
        content = urllib2.urlopen(link).read();
        try:
            # find the <head> tag and insert our <base href=%url%> to make sure imgs/etc work still
            content = add_base_href(content, link)
            # insert our javascript at the end of the body
            content = add_js(content, link)
        except Exception as detail:
            c.details = detail
            return "error. details: %s, url: %s" % (detail, request.params['q'])

        return content

    def selected(self):
        """
        After the user has selected the DOM element, it passes through here.
        """
        tree = lxml.html.fromstring( urllib2.urlopen(urllib.unquote(request.params['referer'])).read() )
        chunk = tree.xpath(request.params['xpath'], pretty_print=True)
        if len(chunk) > 0:
            chunk = tostring(chunk[0])
        else:
            chunk = "[no text]"
        return "xpath: %s<br>from url: %s<br>chunk: %s" % (request.params['xpath'], request.params['referer'], chunk)
