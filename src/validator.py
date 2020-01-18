import re

from db import email_exists, username_exists


class UsernameValidator:
	@staticmethod
	def validate(username):
		if not UsernameValidator.is_username_valid(username):
			print('Invalid username!')
			print('Please choose a username which consists of 4 - 32')
			print('alphanumeric characters and underscores.')
			return False
		if username_exists(username):
			print('This username is already in use!')
			return False
		return True

	@staticmethod
	def is_username_valid(username):
		return (4 <= len(username) <= 32) \
		       and (re.match('^[a-zA-Z0-9_]+$', username) is not None)


class EmailValidator:
	@staticmethod
	def validate(email: str):
		if not EmailValidator.is_email_valid(email):
			print('Invalid email address! Please enter a valid one.')
			return False
		if email_exists(email):
			print('This email address has already been registered!')
			print('Please log in or use another email address to sign up.')
		return True

	@staticmethod
	def is_email_valid(email):
		return re.match('^[\w-.+]+@([\w-]+\.)+[\w-]+$', email) is not None


class OptionValidator:
	def __init__(self, limit):
		self.limit = limit

	def validate(self, option):
		if not self.is_option_valid(option):
			print('Invalid option selected! Please enter a valid one.')
			return False
		return True

	def is_option_valid(self, option):
		return option in range(self.limit)
