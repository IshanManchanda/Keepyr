from getpass import getpass

import context
from db import check_password, create_user, email_exists, \
	get_username_by_email, username_exists
from validator import EmailValidator, OptionValidator, UsernameValidator


def get_input(prompt, Validator):
	while True:
		inp = input(prompt)
		if Validator.validate(inp):
			return inp


def authorize():
	if context.logged_in_user:
		return True

	prompt = 'Create new account or login to an existing one? (1 / 2): '
	if get_input(prompt, OptionValidator(2)) == '1':
		signup()
	else:
		login()

	return True


def signup():
	name = input('Enter your name: ')
	username = get_input('Pick a username: ', UsernameValidator)
	email_id = get_input('Enter your email address: ', EmailValidator)

	while True:
		password1 = getpass('Choose a password: ')
		password2 = getpass('Repeat password: ')

		if password1 != password2:
			print('The passwords don\'t match!')
			continue

		if len(password1) < 8:
			print('Please use a password that is 8 characters or longer.')
			continue

		break

	create_user(name, username, email_id, password1)
	login()


def login():
	while True:
		inp = input('Enter your username or email ID: ')

		# User has entered an email address
		if '@' in inp:
			if email_exists(inp):
				username = get_username_by_email(inp)
				break
			print('Email ID has not been registered! Please sign-up instead.')

		# User has entered a username
		else:
			if username_exists(inp):
				username = inp
				break
			print('Invalid username!')

	for _ in range(3):
		password = getpass('Enter your password: ')
		if check_password(username, password):
			context.logged_in_user = username
			break
		print('Incorrect Password!')

	authorize()


def logout():
	context.logged_in_user = None
	print('\nLogged out successfully!\n\n')


def store_password():
	pass


def retrieve_passwords():
	pass


def main():
	print('Welcome to Keepyr password manager!\n')
	authorize()

	print('Thank you for logging in.')
	while True:
		print('\nPlease select an option:')
		print('1. Store new password')
		print('2. Retrieve passwords')
		print('3. Logout')

		option = get_input('Selected Option (1 / 2 / 3): ', OptionValidator(3))
		if option == '1':
			store_password()
		elif option == '2':
			retrieve_passwords()
		else:
			logout()
			main()


if __name__ == '__main__':
	main()
