<%inherit file="/base/base.mako" />

<%def name="title()">
	Notifox
</%def>

<%def name="header()">
	<header>Codename Notifox</header>
</%def>

<form name="f" id="f" method="get" action="/add">
	<input type="url" name="q" id="q" placeholder="http://en.wikipedia.org/wiki/Jesus" value="http://" autofocus>
	<input type="submit" id="sub" value="Add Page">
</form>
