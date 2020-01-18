# This file acts as a context manager that stores the state of the program.
# That is, is manages the variables that need to be shared between the files.
# We opt for this design pattern because it avoids the issue of cyclic imports
# and is based on the principles of loose coupling of components.

logged_in_user = None
user_password = None
db = None
