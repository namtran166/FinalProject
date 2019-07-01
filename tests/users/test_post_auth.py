import pytest

from tests.actions import authorize_user


@pytest.mark.parametrize(
    "authentication, status_code",
    [
        # Test case: Valid user
        (
                {
                    "username": "brian123",
                    "password": "123456"
                },
                200
        ),
        # Test case: Valid user with space
        (
                {
                    "username": "    brian123  ",
                    "password": "    123456 "
                },
                200
        )
    ]
)
def test_post_auth_valid(client, authentication, status_code):
    response, json_response = authorize_user(client, authentication)

    assert response.status_code == status_code
    assert all(key in json_response for key in ["access_token", "id", "username", "first_name", "last_name"]) is True
    assert any(key in json_response for key in ["password", "hashed_password"]) is False


@pytest.mark.parametrize(
    "authentication, status_code, description",
    [
        # Test case: Username does not exist
        (
                {
                    "username": "brian124",
                    "password": "123456"
                },
                401,
                "Invalid Credentials."
        ),
        # Test case: Wrong password
        (
                {
                    "username": "brian123",
                    "password": "123356"
                },
                401,
                "Invalid Credentials."
        ),
        # Test case: Missing username
        (
                {
                    "password": "123456"
                },
                400,
                "Missing data for required field: username."
        ),
        # Test case: Missing password
        (
                {
                    "username": "brian123"
                },
                400,
                "Missing data for required field: password."
        )
    ]
)
def test_post_auth_invalid(client, authentication, status_code, description):
    response, json_response = authorize_user(client, authentication)

    assert response.status_code == status_code
    assert json_response["description"] == description
