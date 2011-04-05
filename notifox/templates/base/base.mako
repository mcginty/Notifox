<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>${self.title()}</title>
		<meta name="description" content="">
		<meta name="author" content="">

		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="/generic.css" type="text/css">
		<link href='http://fonts.googleapis.com/css?family=Neuton|Ubuntu' rel='stylesheet' type='text/css'>
		<link rel="shortcut icon" href="/favicon.ico">
		<link rel="apple-touch-icon" href="/apple-touch.icon.png">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
	</head>

	<body>
	<div id="container">
		${self.header()}
		${self.tabs()}
		${next.body()}
		${self.footer()}
	</div>
	</body>
</html>

<%def name="title()">SimpleSite</%def>
<%def name="head()"></%def>
<%def name="header()"><a name="top"></a></%def>
<%def name="tabs()"></%def>
<%def name="footer()"><div id="footer">Copyleft &copy; 2011 Jake McGinty</div></%def>
