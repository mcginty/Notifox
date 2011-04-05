<%inherit file="/base/base.mako" />

<%def name="head_tags()">
	<title>Register</title>
</%def>

	<form name="form" action="/register" method="post">
		<fieldset>
			<legend>Your Information</legend>
			<ol>
				<li>
					<label for="username">Username</label>
					<input type="text" name="username" id="username" placeholder="bozarking" required autofocus></li>
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
</html>
