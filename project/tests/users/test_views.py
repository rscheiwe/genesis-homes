from project.users.models import User
from project.users import users_router


def test_read_unauthorized_url(client):

    response = client.get('/genesis-users/users')
    assert response.status_code == 401


def test_read_second_unauthorized_url(client):
    user_id = 1
    response = client.get(f'/genesis-users/users/{user_id}')
    assert response.status_code == 401
    assert response.json()["detail"] == f"Not authenticated"

