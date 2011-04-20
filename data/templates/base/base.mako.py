# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1302777371.9356689
_template_filename=u'/var/pylons/notifox/notifox/templates/base/base.mako'
_template_uri=u'/base/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['tabs', 'header', 'head', 'footer', 'title']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        session = context.get('session', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!doctype html>\n<html>\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n\t\t<title>')
        # SOURCE LINE 6
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n\t\t<meta name="description" content="">\n\t\t<meta name="author" content="">\n\n\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t\t<link rel="stylesheet" href="/generic.css" type="text/css">\n\t\t<link href=\'http://fonts.googleapis.com/css?family=Neuton|Ubuntu\' rel=\'stylesheet\' type=\'text/css\'>\n\t\t<link rel="shortcut icon" href="/favicon.ico">\n\t\t<link rel="apple-touch-icon" href="/apple-touch.icon.png">\n\t\t<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>\n\t\t')
        # SOURCE LINE 16
        __M_writer(escape(self.head()))
        __M_writer(u'\n\t</head>\n\n\t<body>\n\t<div id="container">\n\t\t')
        # SOURCE LINE 21
        __M_writer(escape(self.header()))
        __M_writer(u'\n')
        # SOURCE LINE 22
        if 'error' in session:
            # SOURCE LINE 23
            __M_writer(u'\t\t<div class="error_msg">')
            __M_writer(escape(session['error']))
            __M_writer(u'</div>\n')
            pass
        # SOURCE LINE 25
        __M_writer(u'\t\t')
        __M_writer(escape(self.tabs()))
        __M_writer(u'\n\t\t')
        # SOURCE LINE 26
        __M_writer(escape(next.body()))
        __M_writer(u'\n\t\t')
        # SOURCE LINE 27
        __M_writer(escape(self.footer()))
        __M_writer(u'\n\t</div>\n\t</body>\n</html>\n\n')
        # SOURCE LINE 32
        __M_writer(u'\n')
        # SOURCE LINE 33
        __M_writer(u'\n')
        # SOURCE LINE 34
        __M_writer(u'\n')
        # SOURCE LINE 35
        __M_writer(u'\n')
        # SOURCE LINE 36
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tabs(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 34
        __M_writer(u'<a name="top"></a>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 36
        __M_writer(u'<div id="footer">Copyleft &copy; 2011 Jake McGinty</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 32
        __M_writer(u'SimpleSite')
        return ''
    finally:
        context.caller_stack._pop_frame()


