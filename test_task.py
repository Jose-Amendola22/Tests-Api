import pytest
from models import Task


#Pruebas a la clase Task
@pytest.fixture
#Se crea un simple task para comprobar que la clase y atributos
def sample_task():
    return Task(
        title='Sample Task',
        description='This is a sample task.',
        completed=False
    )

#Se prueba que se incialize de manera correcta
def test_task_initialization(sample_task):
    assert sample_task.title == 'Sample Task'
    assert sample_task.description == 'This is a sample task.'
    assert not sample_task.completed

#Se prueba que pueda recibir y actualizarse la clase task
def test_task_update(sample_task):
    sample_task.update(
        title='Updated Task',
        description='This task has been updated.',
        completed=True
    )
    assert sample_task.title == 'Updated Task'
    assert sample_task.description == 'This task has been updated.'
    assert sample_task.completed

#Se comprueba que la clase task pueda cambiar SÓLO ciertos datos
def test_task_update_partial(sample_task):
    sample_task.update(
        description='Partial update.'
    )
    assert sample_task.title == 'Sample Task' 
    assert sample_task.description == 'Partial update.'
    assert not sample_task.completed  

if __name__ == '__main__':
    pytest.main()
