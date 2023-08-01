import pytest
from starlette.testclient import TestClient
from api.fast_api import app


# @pytest.fixture(scope="module")
# def test_app():
#     client = TestClient(app)
#     yield client  # testing happens here

client = TestClient(app)


def test_login_for_access_token(test_app):
    # response = test_app.post("/token")
    # assert response.status_code == 200

    response = test_app.post(
        "/token/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_read_users_me(test_app):
    response = test_app.get("/users/me")
    assert response.status_code == 200


