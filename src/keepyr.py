from db import username_exists, email_id_exists, get_encrypted_password
from validator import is_username_valid
from getpass import getpass
FLAG_SIGNUP, FLAG_LOGIN = 0, 1


def get_selected_choice():
	while True:
		x = input('Create new account or login to an existing one? (1 / 2): ')
		if x == '1':
			return FLAG_SIGNUP
		elif x == '2':
			return FLAG_LOGIN
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
		pass1 = getpass()
		pass2 = getpass('Repeat password: ')

		if pass1 == pass2:
			break
		print('The passwords don\'t match!')

	if not lookup_user(username):
		print('Username not found!')

	password = getpass()


def login():
	pass


# success = validate_user(username, password)
# if not success:
# 	print('Error')


def main():
	print('Welcome to keepyr password manager!')
	choice = get_selected_choice()
	if choice == FLAG_SIGNUP:
		signup()
	else:
		login()


if __name__ == '__main__':
	main()
