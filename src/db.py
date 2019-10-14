from encryptor import hash_password


def create_user(name, username, email_id, password):
	hashed_password = hash_password(password)
	pass


def check_password(username, password):
	pass


def get_username_by_email(email_id):
	pass


def username_exists(username):
	pass


def email_id_exists(email_id):
	pass
