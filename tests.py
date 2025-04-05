import requests
from jsonschema import validate
import schemas

base_url = 'https://reqres.in/api'

#а каждый из методов GET/POST/PUT/DELETE ручек reqres.in
def test_get_list_users_returns_200():
    response = requests.get(f'{base_url}/users', params={'page':'2'})
    assert response.status_code == 200
    assert 'data' in response.json()

def test_create_user_returns_201():
    response = requests.post(f'{base_url}/users', json={"name": "morpheus", "job": "leader"})
    assert response.status_code == 201
    assert 'id' in response.json()

def test_update_user_returns_200():
    response = requests.put(f'{base_url}/users/2', json={"name": "neo", "job": "chosen one"})
    assert response.status_code == 200

def test_delete_user_returns_204():
    response = requests.delete(f'{base_url}/users/2')
    assert response.status_code == 204
    assert response.text == ''

#Позитивные/Негативные тесты на одну из ручек
def test_get_existing_user_returns_200():
    response = requests.get(f'{base_url}/users/2')
    assert response.status_code == 200

def test_get_nonexistent_user_returns_404():
    response = requests.get(f'{base_url}/users/555')
    assert response.status_code == 404

#Разные статус-коды: 400
def test_status_400_on_register_without_password():
    response = requests.post(f'{base_url}/register', json={"email": "elad@gmail.ru"})
    assert response.status_code == 400

#Тест с пустым телом и телом ответа
def test_delete_has_no_body():
    response = requests.delete(f'{base_url}/users/2')
    assert response.status_code == 204
    assert response.text == ''

#Тесты на схемы
def test_create_user_should_return_201_and_match_schema():
    response = requests.post(f'{base_url}/users', json={"name": "John", "job": "QA"})
    assert response.status_code == 201
    validate(response.json(), schema=schemas.post_users)


def test_get_single_user_should_return_200_and_match_schema():
    response = requests.get(f'{base_url}/users/2')
    assert response.status_code == 200
    validate(response.json(), schema=schemas.get_single_user)


def test_get_user_list_should_return_200_and_match_schema():
    response = requests.get(f'{base_url}/users?page=2')
    assert response.status_code == 200
    validate(response.json(), schema=schemas.get_user_list)


def test_register_success_should_return_200_and_match_schema():
    response = requests.post(f'{base_url}/register', json={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert response.status_code == 200
    validate(response.json(), schema=schemas.register_success)


def test_register_unsuccessful_should_return_400_and_match_schema():
    response = requests.post(f'{base_url}/register', json={"email": "elad@gmail.ru"})
    assert response.status_code == 400
    validate(response.json(), schema=schemas.register_error)


def test_delete_user_should_return_204():
    response = requests.delete(f'{base_url}/users/2')
    assert response.status_code == 204
    assert response.text == ''
