import requests
import json
import concurrent.futures

num_users = 10

BASE_URL_AUTH = 'http://127.0.0.1:5000/api/'
BASE_URL_USER = 'http://127.0.0.1:5005/api/'

def get_token(username, password):
    url = BASE_URL_AUTH + 'login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError("Authentication failed.")

def delete_user(username, password):
    try:
        token = get_token(username=password)
        print("Authentication successful. Obtained JWT token")
    except ValueError as e:
        print("Authentication failed: ", e)
        return

    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.delete(f'{BASE_URL_USER}/api/{username}/delete')
    except requests.exceptions.RequestException as e:
        print(f'Failed to delete {username}: {e}')
        return False


def delete_user_test():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(delete_user, f'user{i}', f'password{i}') for i in range(1, num_users+1)]

        concurrent.futures.wait(futures)

if __name__ == '__main__':
    delete_user_test()
