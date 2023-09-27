import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_playlists(client):
    response = client.get('/playlists')
    assert response.status_code == 200 or response.status_code == 302

def test_followed_artists(client):
    response = client.get('/followed-artists')
    assert response.status_code == 200 or response.status_code == 302

def test_top_tracks(client):
    response = client.get('/top-tracks')
    assert response.status_code == 200 or response.status_code == 302
