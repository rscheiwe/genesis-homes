from project.users.models import User
from project.users import users_router


def test_pytest_setup(client):
    # test view
    response = client.get(users_router.url_path_for('/genesis-users/users'))
    assert response.status_code == 404