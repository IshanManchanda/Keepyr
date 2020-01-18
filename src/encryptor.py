from hashlib import sha256

import onetimepad

import context

SECRET_KEY = '71=sc=vtf$$!hyy&6^+sk43d56kvr1a$cemmd$@-(qr*g+++pk'

CHARACTERS = 'abcdefghijklmnopqrstuvwxyz'
CHARACTERS += CHARACTERS.upper()
CHARACTERS += '0123456789!@#$%^&*()-_ '


def get_hexdigest(salt, plaintext):
	return sha256((salt + plaintext).encode('utf-8')).hexdigest()


def get_raw_digest(plaintext, username):
	salt = get_hexdigest(SECRET_KEY, username)[:20]

	# The variable is named hsh since hash is a function provided by Python.
	hsh = get_hexdigest(salt, plaintext)
	return ''.join((salt, hsh))


def hash_password(password, username, length=32, alphabet=CHARACTERS):
	raw_hexdigest = get_raw_digest(password, username)

	# Convert the hexdigest into decimal
	num = int(raw_hexdigest, 16)

	# Base for the characters
	num_chars = len(alphabet)

	# Build up the new password one character at a time,
	# up to the specified length.
	chars = []
	for i in range(length):
		# Successive division - Standard algorithm to convert to arbitrary base
		# At each step, idx represents the next character added to the hash.
		num, idx = divmod(num, num_chars)
		chars.append(alphabet[idx])

	return ''.join(chars)


def encrypt_password(password):
	# We use the one time pad cipher with key as the user's master password
	# to encrypt the passwords stored in the database.
	# This cipher allows us to conveniently encrypt and decrypt,
	# as well as ensure that no one can gain access to the password
	# without the master password.
	return onetimepad.encrypt(password, context.user_password)


def decrypt_password(encrypted_password):
	return onetimepad.decrypt(encrypted_password, context.user_password)
