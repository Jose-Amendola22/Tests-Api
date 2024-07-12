import requests
import pytest
import os

# Esto se usa para poder usarse en docker, normalmente sólo la url normal basta
BASE_URL = os.getenv('BASE_URL', 'http://backend:8888')  

#Task que usaremos como prueba!
sample_task = {
    'title': 'Sample Task',
    'description': 'This is a sample task.',
    'completed': False
}

@pytest.fixture
def cleanup_tasks():
    #Se borran los tasks para empezar de manera limpia
    requests.delete(f'{BASE_URL}/tasks')
    yield
    requests.delete(f'{BASE_URL}/tasks')

def test_get_tasks():
    #Prueba sencilla donde se llama con un get a la api, si devuelve 200 entonces la prueba pasa
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    #Prueba sencilla donde se crea un objeto en la api, si devuelve 201 entonces se creo el objeto de manera correcta
    response = requests.post(f'{BASE_URL}/tasks', json=sample_task)
    assert response.status_code == 201
    assert 'id' in response.json()

def test_create_task_invalid_json():
    #Se comprueba que no se pueda enviar datos que no existan
    invalid_task = {
        'invalid_key': 'Invalid Task'  
    }
    response = requests.post(f'{BASE_URL}/tasks', json=invalid_task)
    #Si devuelve 400 la api significa que paso la prueba por que tiene el error handler correcto
    assert response.status_code == 400 

def test_create_task_missing_field():
    #Prueba donde se comprueba que la api no permita recibir tasks con fields faltantes
    incomplete_task = {
        'title': 'Incomplete Task'  
    }
    response = requests.post(f'{BASE_URL}/tasks', json=incomplete_task)
    #Si devuelve 400 la api significa que paso la prueba por que tiene el error handler correcto
    assert response.status_code == 400 

def test_update_task():
    #Prueba sencilla que comprueba que el api pueda actualizar tasks con el id proporcionado
    task_id = create_task()
    updated_task = {
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=updated_task)
    assert response.status_code == 200

def test_update_task_not_found():
    #Prueba que valida que si no esta el id, el api no devuelva error 500
    task_id = 'non_existent_id'
    updated_task = {
        'title': 'Updated Task',
        'description': 'This task has been updated.',
        'completed': True
    }
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=updated_task)
    #Si devuelve 404 significa que la api no encontro el id
    assert response.status_code == 404  

def test_delete_task():
    #Prueba que valida que se pueda borrar un registro correctamente
    task_id = create_task()
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    #Si devuelle 200 significa que se borro el task de manera correcta
    assert response.status_code == 200

def test_delete_task_not_found():
    #Prueba que valida que el task a borrar si no existe no devuelva error 500
    task_id = 'non_existent_id'
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    #Si devuelve error 404 sigfinifica que paso la prueba
    assert response.status_code == 404  

def create_task():
    #Prueba donde se comprueba que se pueda insertar tasks a la api
    response = requests.post(f'{BASE_URL}/tasks', json=sample_task)
    assert response.status_code == 201
    return response.json()['id']
