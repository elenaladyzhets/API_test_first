import pytest
import requests
from jsonschema import validate
import schemas

base_url = 'https://reqres.in/api'

test_user = {"name": "archie", "job": "tester"}
@pytest.fixture()
def created_user():
    response = requests.post(f'{base_url}/users', json=test_user)
    assert response.status_code == 201
    return response.json()['id']


#а каждый из методов GET/POST/PUT/DELETE ручек reqres.in
def test_get_list_users_returns_200():
    response = requests.get(f'{base_url}/users', params={'page':'2'})
    assert response.status_code == 200
    validate(response.json(), schema=schemas.get_user_list)

def test_create_user_returns_201():
    response = requests.post(f'{base_url}/users', json={"name": "morpheus", "job": "leader"})
    assert response.status_code == 201
    validate(response.json(), schema=schemas.post_users)

def test_update_user_returns_200(created_user):
    response = requests.put(f'{base_url}/users/{created_user}', json={"name": "neo", "job": "chosen one"})
    assert response.status_code == 200

def test_delete_user_returns_204(created_user):
    response = requests.delete(f'{base_url}/users/{created_user}')
    assert response.status_code == 204
    assert response.text == ''


def test_get_existing_user_returns_200():
    response = requests.get(f'{base_url}/users/2')
    assert response.status_code == 200

def test_get_nonexistent_user_returns_404():
    response = requests.get(f'{base_url}/users/555')
    assert response.status_code == 404

@pytest.mark.parametrize(
    "payload",
    [
        {
            "email": "elad@gmail.ru"
        },
        {
            "password": "secret123"
        },
        {

        }
    ]
)
def test_status_400_on_register(payload):
    response = requests.post(f'{base_url}/register', json=payload)
    assert response.status_code == 400
    validate(response.json(), schema=schemas.register_error)


def test_register_success_should_return_200_and_match_schema():
    response = requests.post(f'{base_url}/register', json={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert response.status_code == 200
    validate(response.json(), schema=schemas.register_success)
