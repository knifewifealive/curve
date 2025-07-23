import allure
import pytest
from autotests.services.users.api_users import User
from autotests.services.users.models.user_validation import ResponseValidator
from autotests.services.utils.fake_data import FakeUser



@pytest.fixture()
def user():
    return User()


@pytest.fixture()
def response_validator():
    return ResponseValidator()


@pytest.fixture()
def random_user():
    generator = FakeUser()
    return generator.valid_user()

@pytest.fixture()
def create_and_delete_user(user, response_validator, random_user):
    with allure.step('Try to create random user: '):
        response = user.post_create_user(**random_user)
        allure.attach(str(response.json()), name='CreateUser Response', attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, response.json()
    with allure.step('Validate user creation: '):
        validate_response = response_validator.validate_positive_requests(response.json(), 'PostCreateUser')
        allure.attach(str(response.json()), name="Validate create user response",
                      attachment_type=allure.attachment_type.JSON)
        assert validate_response


    with allure.step('Check for created user: '):
        response = user.get_user_by_nickname(nickname=random_user['nickname'])
        allure.attach(str(response.json()), name="Check for created user: ",
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, response_validator.validate_positive_requests(response.json(),
                                                                                          'GetUserByNickname')
    yield response.json()
    with allure.step('Delete user after creation: '):
        response = user.delete_user(nickname=random_user['nickname'])
        allure.attach(str(response.json()), name="Delete user after creation: ",
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, response_validator.validate_positive_requests(response.json(),
                                                                                          'DeleteUserByNickname')


@pytest.fixture()
def create_user(user, response_validator, random_user):
    with allure.step('Try to create random user: '):
        response = user.post_create_user(**random_user)
        allure.attach(str(response.json()), name='CreateUser Response', attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, response.json()
    with allure.step('Validate user creation: '):
        validate_response = response_validator.validate_positive_requests(response.json(), 'PostCreateUser')
        allure.attach(str(response.json()), name="Validate create user response",
                      attachment_type=allure.attachment_type.JSON)
        assert validate_response


    with allure.step('Check for created user: '):
        response = user.get_user_by_nickname(nickname=random_user['nickname'])
        allure.attach(str(response.json()), name="Check for created user: ",
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, response_validator.validate_positive_requests(response.json(),
                                                                                          'GetUserByNickname')
    return response.json()