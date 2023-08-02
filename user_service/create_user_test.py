import requests
import concurrent.futures
num_users = 20
base_url = 'http://172.27.0.3:5002'

def create_user(username, password, first_name, last_name, email):
    data = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }
    try:
        response = requests.post(f'{base_url}/api/users/create', json=data)
        if response.status_code == 201:
            return True
        elif response.status_code == 409:
            print(f'User {username} already exists')
            return False
        else:
            print(f'Failed to create {username}: {response.json()}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Failed to create {username}: {e}')
        return False


def create_user_test():
    successes = 0
    failures = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(create_user, f'user{i}', f'password{i}', f'first_name{i}', f'last_name{i}', f'user{i}@email.com')
                   for i in range(1, num_users + 1)]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                successes += 1
            else:
                failures += 1

    print(f'Successful requests: {successes}')
    print(f'Failed requests: {failures}')


if __name__ == '__main__':
    create_user_test()
