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
    resp = client.post('/registry', json={'username': 'testuser', 'password': 'secret123'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data

    # Login
    resp = client.post('/login', json={'username': 'testuser', 'password': 'secret123'})
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
*** End Patch