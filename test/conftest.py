import pytest
from server import app
from selenium import webdriver

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def competitions():
    return [
        {'name': 'competition1',"date": "2020-03-27 10:00:00", 'numberOfPlaces': '10'},
        {'name': 'competition2',"date": "2020-03-27 10:00:00", 'numberOfPlaces': '20'},
    ]

@pytest.fixture
def clubs():
    return [
        {'name': 'club1', 'email':'club1@hotmail.fr', 'points': '15'},
        {'name': 'club2','email':'club2@hotmail.fr', 'points': '5'},
    ]

@pytest.fixture
def reservations():
    return [
        {'competition': 'competition1', 'club': 'club1', 'places': '5'},
        {'competition': 'competition1', 'club': 'club2', 'places': '5'},
    ]

@pytest.fixture
def client_1_with_session(client):
    with client.session_transaction() as session:
        session['email'] = 'club1@hotmail.fr'
    return client

@pytest.fixture
def client_2_with_session(client):
    with client.session_transaction() as session:
        session['email'] = 'club2@hotmail.fr'
    return client

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.close()