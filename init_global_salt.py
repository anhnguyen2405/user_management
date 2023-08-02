import bcrypt

# Generate a global salt for password hashing
global_salt = bcrypt.gensalt()

# Save the global_salt to a file
with open("global_salt.txt", "wb") as file:
    file.write(global_salt)
