from getpass import getpass

import context
from db import check_master_password, create_user, email_exists, \
	get_password_list, get_username_by_email, retrieve_password, \
	store_password, terminate_connection, username_exists, init_db
from validator import EmailValidator, OptionValidator, ServiceValidator, \
	UsernameValidator


def get_input(prompt, Validator):
	# Helper function for error-safe user input.
	# Accepts a validator class/object to validate the entered data against
	# and repeats the request until valid input is received.
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
		# Using getpass is more secure than taking input manually
		# as getpass hides the inputted text in the command line.
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
	print('\nSign up successful! Please proceed to login...\n')
	login()


def login():
	while True:
		inp = input('Enter your username or email ID: ')

		if '@' in inp:
			# User has entered an email address
			if email_exists(inp):
				username = get_username_by_email(inp)
				break
			print('Email ID has not been registered! Please sign-up instead.\n')

		else:
			# User has entered a username
			if username_exists(inp):
				username = inp
				break
			print('Invalid username!\n')

	# We provide 3 attempts for the password, before prompting the user
	# to confirm whether they would like to login or sign-up,
	# and also request username/email address again.
	# As per convention, since the loop index is not used, we use _
	for _ in range(3):
		password = getpass('Enter your password: ')
		if check_master_password(username, password):
			context.logged_in_user = username
			# We store the user's
			context.user_password = password
			break
		print('Incorrect Password!\n')

	authorize()


def logout():
	context.logged_in_user = None
	print('\nLogged out successfully!\n\n')


def store():
	service = get_input('Enter the name of the service: ', ServiceValidator)
	password = input('Enter password: ')
	store_password(service, password)


def retrieve():
	password_list = get_password_list()
	n_passwords = len(password_list)
	if not n_passwords:
		print('\nThere are no passwords stored currently!')
		return

	print('\nWhich password do you want to retrieve?')
	for i, row in enumerate(password_list):
		print('%s: %s' % (i + 1, row[1]))

	option = get_input('Selected option: ', OptionValidator(n_passwords))
	password = retrieve_password(password_list[int(option) - 1][0])
	print('Your requested password is:', password)


def main():
	# Entry point into the application
	try:
		init_db()
		print('Welcome to Keepyr password manager!\n')
		authorize()

		print('\nLogin successful!')
		while True:
			print('\nPlease select an option:')
			print('1. Store new password')
			print('2. Retrieve passwords')
			print('3. Logout')

			option = get_input('Selected Option: ', OptionValidator(3))
			if option == '1':
				store()
			elif option == '2':
				retrieve()
			else:
				logout()
				main()
	except KeyboardInterrupt:
		# Free resources and gracefully exit
		terminate_connection()


if __name__ == '__main__':
	main()
