from hashlib import sha256

SECRET_KEY = '71=sc=vtf$$!hyy&6^+sk43d56kvr1a$cemmd$@-(qr*g+++pk'

CHARACTERS = 'abcdefghijklmnopqrstuvwxyz'
CHARACTERS += CHARACTERS.upper()
CHARACTERS += '0123456789!@#$%^&*()-_ '


def get_hexdigest(salt, plaintext):
	return sha256(salt + plaintext).hexdigest()


def get_raw_digest(plaintext, username):
	salt = get_hexdigest(SECRET_KEY, username)[:20]
	hsh = get_hexdigest(salt, plaintext)
	return ''.join((salt, hsh))


def hash_password(password, username, length=32, alphabet=CHARACTERS):
	raw_hexdigest = get_raw_digest(password, username)

	# Convert the hexdigest into decimal
	num = int(raw_hexdigest, 16)

	# Base for the characters
	num_chars = len(alphabet)

	# Build up the new password one character at a time,
	# up to a certain length
	chars = []
	for i in range(length):
		num, idx = divmod(num, num_chars)
		chars.append(alphabet[idx])

	return ''.join(chars)
