import pytest
from autotests.services.users.api_users import User

@pytest.fixture()
def user():
    return User()