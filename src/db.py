import mysql.connector

import context
from encryptor import decrypt_password, encrypt_password, hash_password


def init_db():
	try:
		context.db = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='37ujTpLAp@!WoyL&',
			database='PasswordManager'
		)
	except mysql.connector.errors.ProgrammingError:
		raise EnvironmentError(
			'Unable to connect to MySQL database!\n'
			'Please check credentials and ensure the server is running.'
		)


def terminate_connection():
	context.db.close()


def create_user(name, username, email, password):
	# Instead of storing the password directly, we store only a hash of it
	# in this way, even if someone is able to access the database,
	# they cannot retrieve the user's password.
	password_hash = hash_password(password, username)

	query = "INSERT INTO Users VALUES('%s', '%s', '%s', '%s')" % (
		username, name, email, password_hash
	)

	cursor = context.db.cursor()
	cursor.execute(query)
	context.db.commit()
	cursor.close()


def check_master_password(username, password):
	# Since we store only the hash, we must hash the entered password
	# and compare it to the stored hash.
	password_hash = hash_password(password, username)

	query = "SELECT EXISTS(" \
	        "SELECT * FROM Users WHERE Username = '%s' AND Password = '%s'" \
	        ")" % (
		        username, password_hash
	        )
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchone()
	cursor.close()
	return result[0]


def store_password(service, password):
	encrypted_password = encrypt_password(password)
	query = "INSERT INTO Passwords (Username, Service, Password)" \
	        "VALUES('%s', '%s', '%s')" % (
		        context.logged_in_user, service, encrypted_password
	        )

	cursor = context.db.cursor()
	cursor.execute(query)
	context.db.commit()
	cursor.close()


def get_username_by_email(email):
	# Helper function that allows us to lookup the username
	# when user enters their email address.
	# This is useful as it allows a uniform way of logging in,
	# which is among the most critical components.
	query = "SELECT Username FROM Users WHERE Email = '%s'" % email
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchone()
	cursor.close()
	return result


def get_password_list():
	# Returns a list of the passwords associated with the current account.
	query = "SELECT ID, Service FROM Passwords WHERE Username = '%s'" \
	        % context.logged_in_user
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchall()
	cursor.close()
	return result


def retrieve_password(password_id):
	query = "SELECT Password FROM Passwords WHERE Username = '%s' AND ID=%s" \
	        % (context.logged_in_user, password_id)
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchone()
	cursor.close()
	return decrypt_password(result[0])


def username_exists(username):
	# Helper function that checks if the entered username is present in the db
	query = "SELECT EXISTS(SELECT * FROM Users WHERE Username = '%s')" % \
	        username
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchone()
	cursor.close()
	return result[0]


def email_exists(email):
	# Helper function that checks if the entered email ID is present in the db
	query = "SELECT EXISTS(SELECT * FROM Users WHERE Username = '%s')" % email
	cursor = context.db.cursor()
	cursor.execute(query)

	result = cursor.fetchone()
	cursor.close()
	return result[0]
