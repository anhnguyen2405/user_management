import requests
import concurrent.futures

num_users = 3
BASE_URL_AUTH = 'http://127.0.0.1:5000'
BASE_URL_USER = 'http://127.0.0.1:5005'

def get_token(username, password):
    url = BASE_URL_AUTH + '/api/login'
    data = {'username' : username, 'password' : password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError("Authentication failed.")
    

def update_user(username, password, first_name, last_name, email):
    data = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

    try:
        token = get_token(username, password)
        print("Authentication successful. Obtained JWT token")
    except ValueError as e:
        print("Authentication failed: ",e)
        return
    
    headers = {'Authorization' : f'Bearer {token}'}


    try:
        response = requests.put(f'{BASE_URL_USER}/api/{username}/update', headers= headers ,json=data)
        print(f'{BASE_URL_USER}/api/{username}/update')
        if response.status_code == 200:
            return True
        elif response.status_code == 409:
            print(f'User {username} already exists')
            return False
        else:
            print(f'Failed to update {username}: {response.json()}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Failed to update {username}: {e}')
        return False


def update_user_test():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(update_user, f'user{i}', f'password{i}', f'first_name{i}x', f'last_name{i}x', f'user{i}x@email.com')
                   for i in range(1, num_users + 1)]

        concurrent.futures.wait(futures)

if __name__ == '__main__':
    update_user_test()
