import hashlib
import bcrypt

# Declaring Password
password = 'GeeksPassword'
# Adding the salt to password
salt = bcrypt.gensalt()

# Adding salt at the last of the password
dataBase_password = password + str(salt)
# Encoding the password
hashed = hashlib.md5(dataBase_password.encode())

# converting hash type to string

ddd = hashed.hexdigest()
# Printing the Hash
print(ddd)
print(type(ddd))
