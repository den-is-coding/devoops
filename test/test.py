from main import app


# passed
def test_empty_db():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'data not found' in response.data


# passed
def test_create_record():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.put('/', json={
            "name": "Bob",
            "email": "Bob_email",
            "role": "Bob_role",
            "unique_facial_id": "Bob_unique_facial_id",
        })
        assert response.status_code == 200
        assert response.get_json()["role"] == "Bob_role"


# passed
def test_get_all_users():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.post('/all_users', json={
            "email": "Bob_email"
        })
        assert response.status_code == 200
        assert b'no access, bad role' in response.data


# passed
def test_update_record():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.post('/', json={
            "name": "Bob",
            "email": "Bob_email",
            "role": "admin",
            "unique_facial_id": "Bob_unique_facial_id",
        })
        assert response.status_code == 200
        assert response.get_json()["role"] == "admin"


# passed
def test_get_all_users_admin():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.post('/all_users', json={
            "email": "Bob_email"
        })
        assert response.status_code == 200
        assert len(response.get_json()) > 1


def test_delete_record():
    flask_app = app
    with flask_app.test_client() as test_client:
        response = test_client.delete('/', json={
            "email": "Bob_email"
        })
        assert response.status_code == 200
        assert len(response.get_json()) >= 1
