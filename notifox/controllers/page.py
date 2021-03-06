import logging

# HTML/XTree parsing libraries
import urllib, urllib2
import re
import lxml.html
from lxml import etree
from lxml.html.soupparser import fromstring
from lxml.html import tostring

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from notifox.lib.base import Session, BaseController, render
from notifox.model.user import User
from notifox.model.page import Page

"""
'   Dataflows:
'       * GET[link] -> add() -> selected() -> list()
'       * list()
"""

log = logging.getLogger(__name__)
absolute_url = "http://localhost:5000"

def add_base_href(root, link):
    """
    Locate the <head> tag, and insert our base tag.
    <base> tells the browser to use that path for relative links over the current URI.
    """
    try:
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
    return

def add_js(root, link):
    """
    Insert JavaScript for our node selector at the end of the body.
    """
    try:
        settings = etree.Element("script")
        settings.text = ' \n \
            nodeselector = {}; \n \
            nodeselector.ns = {}; \n \
            nodeselector.ns.doneURL = "'+absolute_url+'/selected/"; \n \
            nodeselector.ns.initURL = "'+link+'";\n'

        nsjs = etree.Element("script", src=absolute_url+'/ns.js')
        root.append(settings)
        root.append(nsjs)
    except Exception as detail:
        raise Exception(detail)
    return

def add_helpbar(root):
    """
    Insert JavaScript for our node selector at the end of the body.
    """
    try:
        helpbar = etree.Element("div",
                id="notifox_help_bar",
                style="position:fixed; bottom: 0px; left: 0px; width: 100%; border: 1px solid black; background: black; color: white; z-index: 999; padding: 25px; font-size: 150%; font-family: Georgia, Tahoma, Arial, sans-serif; background-image: -webkit-linear-gradient(top, #020202, #111111); box-shadow: 0px -5px 20px rgba(0, 0, 0, 1.0); text-align: center; opacity: 0.9;")
        helpbar.attrib['class'] = 'no_highlight'

        descspan = etree.Element("div")
        descspan.text = 'Select an element on the page for Notifox to track.'
        hintspan = etree.Element("div", style="font-size: 60%")
        hintspan.text = 'Hint: hit the Control button on your keyboard to select the element underneath your current one.'
        descspan.attrib['class'] = 'no_highlight'
        hintspan.attrib['class'] = 'no_highlight'
        upboat = etree.Element("img", src=absolute_url + "/upboat.png", style="position:absolute; left: 200px; vertical-align: center;")
        upboat.attrib['class'] = 'no_highlight'
        helpbar.append(upboat)
        helpbar.append(descspan)
        helpbar.append(hintspan)

        root.append(helpbar)
    except Exception as detail:
        raise Exception(detail)
    return

class PageController(BaseController):

    def __before__(self):
        """ Called before any function does anything. """
        c.errors = []
        if 'username' in session:
            c.me = Session.query(User).filter_by(name='username'

    def index(self):
        # Return a rendered template
        return render('/derived/page/page.mako')

    def show(self):
        if 'username' in session:
            me = Session.query(Page).filter_by(user_id=session['id']).first()
            c.pages = me.pages
            render render('/derived/page/all.mako')

    def add(self):
        """
        Linked is passed all pretty-like into this function, which slips in our helper code in the requested website.
        All the rest of the work is done client-side with our ns.js (nodeSelector library), which returns XPath.

        next in line: selected()
        """
        link = request.params['q']
        content = urllib2.urlopen(link).read()
        try:
            root = lxml.html.fromstring(content)
            # find the <head> tag and insert our <base href=%url%> to make sure imgs/etc work still
            add_base_href(root, link)
            # insert our javascript at the end of the body
            add_js(root, link)
            add_helpbar(root)
            content = tostring(root)
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
            if 'username' in session:
                me = Session.query(User).filter_by(name=session['username']).first()
                # Make sure this *exact* combination isn't in the database already.
                if len(Session.query(Page).filter_by(user_id=me.id, url=request.params['referer'], xpath=request.params['xpath']).all()) == 0:
                    page = Page(request.params['referer'], request.params['referer'], request.params['xpath'], me.id)
                    Session.add(page)
                    Session.commit()
                else:
                    c.errors.append("You're already watching this path, sillybutt!")
                    return c.errors
        else:
            chunk = "[no text]"
        redirect(url(controller='auth', action='pages'))
