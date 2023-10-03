import pytest
import requests

# Define the base URL for your API
BASE_URL = 'http://127.0.0.1:3000/'

# Define sample data for testing (you may need to adjust this)
sample_user_data = {
    'username': 'bodakesa@gmail.com',
    'email': 'bodakesa@gmail.com',
    'password': 'admin',
}

sample_group_data = {
  "name": "test Group",
  "group_members": [1]  
}
@pytest.fixture
def auth_token():
    # Authenticate a user and get an access token for testing
    response = requests.post(BASE_URL + 'login/', data={
    "username": "bodake@gmail.com",
    "password": "admin"
})
    assert response.status_code == 200
    return response.json()['Token']

def test_user_registration(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(BASE_URL + 'register_user/', headers=headers, json=sample_user_data)
    assert response.status_code == 201

def test_create_group(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(BASE_URL + 'groups/create/', headers=headers, json=sample_group_data)
    assert response.status_code == 201

def test_add_member_to_group(auth_token):
    # Create a new user for testing (assuming the user registration test passed)
    headers = {'Authorization': f'Bearer {auth_token}'}
    user_data = {
        'username': 'newu@example.com',
        'email': 'newu@example.com',
        'password': 'newpassword123',
    }
    response = requests.post(BASE_URL + 'register_user/', headers=headers, json=user_data)
    assert response.status_code == 201

    # # Authenticate the new user and get an access token
    # response = requests.post(BASE_URL + 'login/', data={
    #     'username': 'newu@example.com',
    #     'password': 'newpassword123',
    # })
    # assert response.status_code == 200
    # new_auth_token = response.json()['Token']

    # Create a new group (assuming the group creation test passed)
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(BASE_URL + 'groups/create/', headers=headers, json=sample_group_data)
    assert response.status_code == 201
    group_id = response.json()['id']

    # Add the new user to the group
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.post(BASE_URL + f'groups/{group_id}/add_member/', headers=headers, json={'user_id': 2})  # Replace 2 with the actual user ID
    assert response.status_code == 201


def test_send_message_to_group(auth_token):
    group_id = 1 

    # Send a message to the group
    headers = {'Authorization': f'Bearer {auth_token}'}
    message_data = {'text': 'Hello, group!'}
    response = requests.post(BASE_URL + f'groups/{group_id}/send_message/', headers=headers, json=message_data)
    assert response.status_code == 201

if __name__ == '__main__':
    pytest.main()
