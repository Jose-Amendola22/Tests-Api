import requests
import pytest
import os

BASE_URL = os.getenv('BASE_URL', 'http://backend:8888')  # Use environment variable or default to http://backend:8888

sample_task = {
    'title': 'Sample Task',
    'description': 'This is a sample task.',
    'completed': False
}

@pytest.fixture
def cleanup_tasks():
    # Setup: Delete all tasks before tests and teardown after tests
    requests.delete(f'{BASE_URL}/tasks')
    yield
    requests.delete(f'{BASE_URL}/tasks')

def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    response = requests.post(f'{BASE_URL}/tasks', json=sample_task)
    assert response.status_code == 201
    assert 'id' in response.json()

def test_create_task_invalid_json():
    invalid_task = {
        'invalid_key': 'Invalid Task'  # Missing required fields
    }
    response = requests.post(f'{BASE_URL}/tasks', json=invalid_task)
    assert response.status_code == 400  # Expecting BadRequest

def test_create_task_missing_field():
    incomplete_task = {
        'title': 'Incomplete Task'  # Missing 'description' and 'completed'
    }
    response = requests.post(f'{BASE_URL}/tasks', json=incomplete_task)
    assert response.status_code == 400  # Expecting BadRequest

def test_update_task():
    task_id = create_task()
    updated_task = {
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=updated_task)
    assert response.status_code == 200

def test_update_task_not_found():
    task_id = 'non_existent_id'
    updated_task = {
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=updated_task)
    assert response.status_code == 404  # Expecting NotFound

def test_delete_task():
    task_id = create_task()
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200

def test_delete_task_not_found():
    task_id = 'non_existent_id'
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404  # Expecting NotFound

def create_task():
    response = requests.post(f'{BASE_URL}/tasks', json=sample_task)
    assert response.status_code == 201
    return response.json()['id']
