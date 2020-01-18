import re

from db import email_exists, username_exists


# This file contains the validator classes for the various possible inputs.
# All of them implement a function called validate,
# which checks the validity of the entered data
# and is responsible for printing feedback for the user.

class UsernameValidator:
	@staticmethod
	def validate(username):
		if not UsernameValidator.is_username_valid(username):
			print('Invalid username!')
			print('Please choose a username which consists of 4 - 32')
			print('alphanumeric characters and underscores.\n')
			return False

		if username_exists(username):
			print('This username is already in use!\n')
			return False
		return True

	@staticmethod
	def is_username_valid(username):
		# Checks length and characters in the username
		return (4 <= len(username) <= 32) \
		       and (re.match('^[a-zA-Z0-9_]+$', username) is not None)


class EmailValidator:
	@staticmethod
	def validate(email):
		if not EmailValidator.is_email_valid(email):
			print('Invalid email address! Please enter a valid one.\n')
			return False

		if email_exists(email):
			print('This email address has already been registered!')
			print('Please log in or use another email address to sign up.\n')
			return False
		return True

	@staticmethod
	def is_email_valid(email):
		# Tests for the general format of all email addresses:
		# identifier@domain.extension
		return re.match('^[\w\-.+]+@([\w\-]+\.)+[\w\-]+$', email) is not None


class OptionValidator:
	def __init__(self, limit):
		self.limit = limit

	def validate(self, option):
		if not self.is_option_valid(option):
			print('Invalid option selected! Please enter a valid one.\n')
			return False
		return True

	def is_option_valid(self, option):
		try:
			return int(option) in range(1, self.limit + 1)
		except ValueError:
			return False


class ServiceValidator:
	@staticmethod
	def validate(service):
		if not (0 < len(service) <= 64):
			print('Service name must be between 0 and 64 characters\n')
			return False
		return True
