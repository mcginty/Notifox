<%inherit file="/base.mako" />

	<form name="form" action="/login" method="post">
		<fieldset>
			<legend>Hive Info</legend>
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
