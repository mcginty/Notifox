<%inherit file="/base/base.mako" />

<%def name="head_tags()">
	<title>Login</title>
</%def>

<%def name="header()">
	<header>Login</header>
</%def>

<ul>
% for page in c.pages:
	<li>${page.name} - ${page.last_crawled}<a href="/admin/users?del=${page.id}">del</a></li>
% endfor
