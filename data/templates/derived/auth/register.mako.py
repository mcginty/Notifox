# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1302361628.3904159
_template_filename='/var/pylons/notifox/notifox/templates/derived/auth/register.mako'
_template_uri='/derived/auth/register.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['header', 'head_tags']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n\n')
        # SOURCE LINE 9
        __M_writer(u'\n\n\t<form name="form" id="register" action="/register" method="post">\n\t\t<fieldset>\n\t\t\t<legend>Your Information</legend>\n\t\t\t<ol>\n\t\t\t\t<li>\n\t\t\t\t\t<label for="username">Username</label>\n\t\t\t\t\t<input type="text" name="username" id="username" placeholder="username" required autofocus></li>\n\t\t\t\t</li>\n\t\t\t\t<li>\n\t\t\t\t\t<label for="password">Password</label>\n\t\t\t\t\t<input type="password" name="password" id="password" placeholder="hunter2" required>\n\t\t\t\t</li>\n\t\t\t\t<li>\n\t\t\t\t\t<label for="email">Email</label>\n\t\t\t\t\t<input type="text" name="email" id="email" placeholder="your@email.com" required>\n\t\t\t\t</li>\n\t\t\t</ol>\n\t\t</fieldset>\n\t\t<fieldset>\n\t\t\t<legend>Optional Notification Methods</legend>\n\t\t\t<ol>\n\t\t\t\t<li>\n\t\t\t\t\t<label for="tel">Cell Phone</label>\n\t\t\t\t\t<input type="text" name="tel" id="tel" placeholder="888-369-4762">\n\t\t\t\t</li>\n\t\t\t</ol>\n\t\t</fieldset>\n\t\t<input type="submit" name="submit" id="submit" value="Register">\n\t</form>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n\t<header>Register</header>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n\t<title>Register</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


