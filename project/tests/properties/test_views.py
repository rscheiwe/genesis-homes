def test_read_unauthorized_url(client):

    response = client.get('/genesis-properties/properties-internal')
    assert response.status_code == 401
    assert response.json()["detail"] == f"Not authenticated"


def test_read_second_unauthorized_url(client):
    user_id = 1
    response = client.get(f'/genesis-properties/user-properties-internal')
    assert response.status_code == 404
