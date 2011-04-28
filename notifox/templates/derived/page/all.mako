<%inherit file="/base/base.mako" />

<%def name="head_tags()">
	<title>My Pages</title>
</%def>

<%def name="header()">
	<header>My Pages</header>
</%def>

<ul>
% for page in c.pages:
	<li>${page.name} - ${page.last_crawled}<a href="/page/del?id=${page.id}">del</a></li>
% endfor
