from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from concurrent.futures import ThreadPoolExecutor
from flask_mysqldb import MySQL
import time
import bcrypt

with open("global_salt.txt", "rb") as file:
    global_salt = file.read()

app = Flask(__name__)

# Set up JWT configurations
app.config['JWT_SECRET_KEY'] = '9464990e38a96935477deca11607e07f51ec9f29535964f7412e54a82a2e80ec'  # Change this to a secure random string in production
jwt = JWTManager(app)

# MySQL configurations (update with your MySQL credentials)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '000000x@X'
app.config['MYSQL_DB'] = 'user_management'

mysql = MySQL(app)

def hash_password(password):
    # Generate a salt and hash the password    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), global_salt)
    return hashed_password

def check_password(password, hashed_password):
    # Check if the given password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

executor = ThreadPoolExecutor()

def perform_login(username, password):
    try:
        # Use app.app_context() to establish the application context
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()

            if not user or  not check_password(password, user[1].encode('utf-8')):
                return False

            return True
    except Exception as e:
        print(e)
        return False

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Invalid credentials'}), 401

    def perform_login_task():
        return perform_login(username, password)

    future = executor.submit(perform_login_task)
    login_result = future.result()

    if login_result:
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected_resource():
    return jsonify({'message': 'Protected resource accessed successfully'}), 200

if __name__ == '__main__':
    print(global_salt)
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0')
