import pytest
from app_factory import create_app
from config.database import Base, engine
from config.database import SessionLocal
import json


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        # reset db
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield client


def test_register_and_login_and_refresh(client):
    # Register
    resp = client.post('/registry', json={'email': 'testuser@example.com', 'username': 'testuser', 'password': 'secret123'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data

    # Login
    resp = client.post('/login', json={'email': 'testuser@example.com', 'password': 'secret123'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'access_token' in data and 'refresh_token' in data

    refresh_token = data['refresh_token']

    # Use refresh endpoint
    headers = {'Authorization': f'Bearer {refresh_token}'}
    resp = client.post('/refresh', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'access_token' in data


def test_protected_and_logout(client):
    # Register and login
    resp = client.post('/registry', json={'email': 'sec@example.com', 'username': 'sec', 'password': 'secret123'})
    assert resp.status_code == 201
    resp = client.post('/login', json={'email': 'sec@example.com', 'password': 'secret123'})
    assert resp.status_code == 200
    tokens = resp.get_json()
    access = tokens['access_token']
    refresh = tokens['refresh_token']

    # Protected without token should be 401
    resp = client.get('/users')
    assert resp.status_code == 401

    # With access token should succeed
    resp = client.get('/users', headers={'Authorization': f'Bearer {access}'})
    assert resp.status_code == 200

    # Logout (revoke refresh)
    resp = client.post('/logout', headers={'Authorization': f'Bearer {refresh}'})
    assert resp.status_code == 200

    # After logout, refresh should fail (token is revoked)
    resp = client.post('/refresh', headers={'Authorization': f'Bearer {refresh}'})
    assert resp.status_code == 401 or resp.status_code == 422
*** End Patch