from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace the base URLs with the URLs where your Authentication and User services are running
BASE_URL_AUTH = 'http://127.0.0.1:5000/api/'
BASE_URL_USER = 'http://127.0.0.1:5001/api/'

# Function to get the JWT token from the Authentication Service
def get_token(username, password):
    url = BASE_URL_AUTH + 'login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError("Authentication failed.")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Get the JWT token from the Authentication Service
    try:
        token = get_token(username, password)
        # Now you have the JWT token, you can use it to call the User Service API
        user_url = BASE_URL_USER + 'users/create'
        user_data = {'username': username, 'password': password}
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        user_response = requests.post(user_url, json=user_data, headers=headers)
        
        if user_response.status_code == 201:
            return jsonify({'message': 'User created successfully'}), 201
        elif user_response.status_code == 409:
            return jsonify({'message': 'User already exists'}), 409
        else:
            return jsonify({'message': 'Failed to create user'}), 500
    except ValueError as e:
        return jsonify({'message': 'Authentication failed'}), 401

if __name__ == '__main__':
    app.run(debug=True,port=5003,host='0.0.0.0')


