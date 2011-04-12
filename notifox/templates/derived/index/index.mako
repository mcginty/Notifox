<%inherit file="/base/base.mako" />

<%def name="title()">
	Notifox
</%def>

<%def name="head()">
</%def>

<%def name="header()">
	<header class="home">Codename Notifox</header><br>
	<a href="/login">Login</a> <a id="reg" href="#register">Register</a><br>
</%def>

<form name="f" id="f" method="get" action="/add">
	<input type="url" name="q" id="q" placeholder="http://en.wikipedia.org/wiki/Jesus" value="http://" autofocus>
	<input type="submit" id="sub" value="Add Page">
</form>

<div id="reg_p">
	<header>Register</header><a href="javascript:void()" id="x">x</a>
	<form name="form" id="register" action="/register" method="post">
		<fieldset>
			<legend>Your Information</legend>
			<ol>
				<li>
					<label for="username">Username</label>
					<input type="text" name="username" id="username" placeholder="username" required autofocus></li>
				</li>
				<li>
					<label for="password">Password</label>
					<input type="password" name="password" id="password" placeholder="hunter2" required>
				</li>
				<li>
					<label for="email">Email</label>
					<input type="text" name="email" id="email" placeholder="your@email.com" required>
				</li>
			</ol>
		</fieldset>
		<fieldset>
			<legend>Optional Notification Methods</legend>
			<ol>
				<li>
					<label for="tel">Cell Phone</label>
					<input type="text" name="tel" id="tel" placeholder="888-369-4762">
				</li>
			</ol>
		</fieldset>
		<input type="submit" name="submit" id="submit" value="Register">
	</form>
</div>
<script>
	$(document).ready( function() {
		$("#reg_p").fadeOut(0);
	});
	$("#reg").click( function() {
		$("#reg_p").fadeIn(0);
	});
	$("#reg_p").click( function() {
		$("#reg_p").fadeOut(0);
	});
	$("#register").click( function(ev) {
		ev.stopPropagation();
	});
	$("#x").click( function() {
		$("#reg_p").fadeOut(0);
	});
</script>
