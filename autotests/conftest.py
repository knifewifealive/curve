import pytest
# from autotests.services.users.api_users import User
# from autotests.services.users.models.user_validation import ResponseValidator
from autotests.services.utils.fake_data import FakeUser
#
# @pytest.fixture()
# def user():
#     return User()
#
# @pytest.fixture()
# def validate_response():
#     return ResponseValidator
#
@pytest.fixture()
def random_user():
    generator = FakeUser()
    return generator.valid_user()

@pytest.fixture()
def random_invalid_user():
    generator = FakeUser()
    return generator.random_invalid_user()