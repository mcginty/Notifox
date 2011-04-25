<%inherit file="/base/base.mako" />

<%def name="head_tags()">
	<title>Login</title>
</%def>

<%def name="header()">
	<header>Login</header>
</%def>

<ul>
% for user in c.users:
	<li>${user.name} <a href="/admin/users?del=${user.id}">del</a></li>
% endfor
