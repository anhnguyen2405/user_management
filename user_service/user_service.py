from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mysqldb import MySQL
import os
from concurrent.futures import ProcessPoolExecutor
import bcrypt

with open("global_salt.txt", "rb") as file:
    global_salt = file.read()

app = Flask(__name__)

app.config['SECRET_KEY'] = '9464990e38a96935477deca11607e07f51ec9f29535964f7412e54a82a2e80ec'
jwt = JWTManager(app)

# MySQL configurations (update with your MySQL credentials)
app.config['MYSQL_HOST']    = 'mysql_db'
app.config['MYSQL_USER']    = 'root'
app.config['MYSQL_PASSWORD']= '000000x@X'
app.config['MYSQL_DB']      = 'user_management'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def hash_password(password):
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), global_salt)
    return hashed_password

def check_password(password, hashed_password):
    # Check if the given password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def execute_query(query, values=None):
    cur = mysql.connection.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    mysql.connection.commit()
    cur.close()

# Function to create a new user (used in multi-processing)
def create_new_user(username, password, first_name, last_name, email):
    # Check if the user already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users where username = %s", (username,))
    user = cur.fetchone()
    if user:
        cur.close()
        return False
    
    # Hash the password before storing it in the database
    hashed_password = hash_password(password)
    
    cur.execute("INSERT INTO users(username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)", (username, hashed_password, first_name, last_name, email))
    mysql.connection.commit()
    cur.close()
    return True

# Functionn to update user information(used in multi-procrssing)
def update_user_info(username, new_first_name, new_last_name, new_email):
    try:
        cur = mysql.connection.cursor()
        query = "UPDATE users SET "
        fields = []
        values = []
        if new_first_name:
            fields.append("first_name = %s")
            values.append(new_first_name)
        if new_last_name:
            fields.append("last_name = %s")
            values.append(new_last_name)
        if new_email:
            fields.append("email = %s")
            values.append(new_email)

        if not fields:
            return

        query += ", ".join(fields) + " WHERE username = %s"
        values.append(username)
        print(query)
        cur.execute(query, tuple(values))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Failed to update user {username}: {e}")

# Function to delete user (used in multi-processing)
def delete_user_existed(username):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    mysql.connection.commit()
    cur.close()

# Endpoint to get users list
@app.route('/api/users', methods = ['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users")
    users = [user[0] for user in cur.fetchall()]
    cur.close()
    return jsonify({'users' : users}), 200

# Endpoint to get detail information of a specific user
@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username , first_name, last_name, email FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({'username': user[0],
                       'first_name' : user[1],
                       'last_name' : user[2],
                       'email' : user[3]}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
# Endpoint to create a new user
@app.route('/api/users/create', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')


    if not username or not password:
        return jsonify({'message': 'Invalid credentials'}), 400

    # Use ProcessPollExecutor to excute create_new_user function concurrently
    with ProcessPoolExecutor() as executor:
        result = executor.submit(create_new_user, username, password, first_name, last_name, email ).result()

    if result:
        return jsonify({'message' : 'User created successfully'}), 201
    else:
        return jsonify({'nessage': 'User already exists'}), 409
    
#Endpoint to update user information
@app.route('/api/<username>/update', methods = ['PUT'])
@jwt_required()
def update_user(username):
    data = request.get_json()
    new_password = data.get('password')
    new_first_name = data.get('first_name')
    new_last_name = data.get('last_name')
    new_email = data.get('email')
    
    if not username :
        return jsonify({'message' : 'The username field is required'}), 400
    
    if new_password :
        return jsonify({'message' : 'Cannot update password'}), 400

    if username and not new_first_name and not new_last_name and not new_email:
        return jsonify({'message' : 'There is no filed to update'}), 400

    with ProcessPoolExecutor() as executor :
        executor.submit(update_user_info, username, new_first_name, new_last_name, new_email )

    return jsonify({'message' : 'User updated successfully'}), 200

# Endpount to delete user
@app.route('/api/<username>/delete', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    if not username:
        return jsonify({'message': 'User is not existed'}), 404

    # Check if the user exists before attempting to delete
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    with ProcessPoolExecutor() as executor:
        executor.submit(delete_user_existed, username)

    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        first_name VARCHAR(255),
                        last_name VARCHAR(255),
                        email VARCHAR(255)
                    )
                    """)                
        mysql.connection.commit()
        cur.close()

    app.run(debug=True,port=5002,host='0.0.0.0')



