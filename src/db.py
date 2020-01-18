import mysql.connector

import context
from encryptor import hash_password


def init_db():
	context.db = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='123',
		database='keepyr'
	)


def create_user(name, username, email, password):
	password_hash = hash_password(password, username)
	query = "Insert into User values('%s', '%s', '%s', '%s')" % (
		name, username, email, password_hash
	)
	cursor = context.db.cursor()
	cursor.execute(query)


def check_password(username, password):
	password_hash = hash_password(password, username)
	query = "SELECT EXISTS(" \
	        "SELECT * FROM User WHERE Username = '%s' AND Password = '%s'" \
	        ")" % (
		        username, password_hash
	        )
	cursor = context.db.cursor()
	cursor.execute(query)
	return cursor.fetchone() is not None


def get_username_by_email(email):
	query = "SELECT Username FROM User WHERE Email = '%s'" % email
	cursor = context.db.cursor()
	cursor.execute(query)
	return cursor.fetchone()


def username_exists(username):
	query = "SELECT EXISTS(SELECT * FROM User WHERE Username = '%s')" % username
	cursor = context.db.cursor()
	cursor.execute(query)
	return cursor.fetchone() is not None


def email_exists(email):
	query = "SELECT EXISTS(SELECT * FROM User WHERE Username = '%s')" % email
	cursor = context.db.cursor()
	cursor.execute(query)
	return cursor.fetchone() is not None
