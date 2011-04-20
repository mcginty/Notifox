<%inherit file="/base/base.mako" />

<%def name="head_tags()">
	<title>Login</title>
</%def>

<%def name="header()">
	<header>Login</header>
</%def>

	<form name="form" id="login" class="auth" action="/login" method="post">
		<fieldset>
			<legend>Credentials</legend>
			<ol>
				<li>
					<label for="username">Username</label>
					<input type="text" name="username" id="username" placeholder="bozarking" required autofocus></li>
				</li>
				<li>
					<label for="password">Password</label>
					<input type="password" name="password" id="password" placeholder="hunter2" required>
				</li>
			</ol>
		</fieldset>
		<input type="submit" name="submit" id="submit" value="Login">
	</form>
</html>
