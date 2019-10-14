from db import username_exists, email_id_exists, create_user, check_password, get_username_by_email
from validator import is_username_valid
from getpass import getpass

LOGGED_IN_USER = None


def authorize():
	while True:
		x = input('Create new account or login to an existing one? (1 / 2): ')
		if x == '1':
			signup()
			return
		elif x == '2':
			login()
			return
		else:
			print('Invalid option selected! Please enter a valid one.')


def signup():
	name = input('Enter your name: ')

	while True:
		username = input('Pick a username: ')
		if not is_username_valid(username):
			print('Invalid username!')
			print('Please choose a username which consists of 4 - 32')
			print('alphanumeric characters and underscores.')
		if not username_exists(username):
			break
		print('Username has been taken!')

	while True:
		email_id = input('Email ID: ')
		if not email_id_exists(email_id):
			break
		print('Email ID has already been registered!')

	while True:
		password1 = getpass()
		password2 = getpass('Repeat password: ')

		if password1 == password2:
			break
		print('The passwords don\'t match!')

	create_user(name, username, email_id, password1)


def login():
	while True:
		inp = input('Enter your username or email ID: ')
		if '@' in inp:
			if email_id_exists(inp):
				username = get_username_by_email(inp)
				break
			print('Email ID has not been registered!')
		else:
			if username_exists(inp):
				username = inp
				break
			print('Invalid username!')

	for _ in range(3):
		password = input('Enter your password: ')
		if check_password(username, password):
			LOGGED_IN_USER = username
			break
		print('Incorrect Password!')

	authorize()


def logout():
	LOGGED_IN_USER = None


def main():
	print('Welcome to Keepyr password manager!')
	authorize()


if __name__ == '__main__':
	main()
