import re


def is_username_valid(username):
	return re.match('^[a-zA-Z0-9_]+$', username) is not None
