import allure
import pytest
from autotests.basetest import BaseTest
from autotests.services.utils.fake_data import FakeUser


@allure.feature('User API')
class TestUsers(BaseTest):

    @allure.story('Setup Database')
    @pytest.mark.api_positive
    def test_setup_db(self):
        with allure.step('Clear all db'):
            response = self.user.post_setup_db_users()
            assert response.status_code == 200, response.json()

    @allure.story('Create user positive')
    @pytest.mark.api_positive
    def test_post_create_user(self, random_user):
        with allure.step('Try to create random user'):
            response = self.user.post_create_user(**random_user)
            allure.attach(str(response.json()), name="CreateUser Response", attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()
        with allure.step('Validate create user response: '):
            validate_response = self.response_validator.validate_positive_requests(response.json(), 'PostCreateUser')
            allure.attach(str(response.json()), name="Validate create user response",
                          attachment_type=allure.attachment_type.JSON)
            assert validate_response
        with allure.step('Check for created user: '):
            response = self.user.get_user_by_nickname(nickname=random_user['nickname'])
            allure.attach(str(response.json()), name="Check for created user: ", attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, self.response_validator.validate_positive_requests(response.json(),
                                                                                                   'GetUserByNickname')
        with allure.step('Delete user after creation: '):
            response = self.user.delete_user(nickname=random_user['nickname'])
            allure.attach(str(response.json()), name="Delete user after creation: ",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, self.response_validator.validate_positive_requests(response.json(),
                                                                                                   'DeleteUserByNickname')

    invalid_user = FakeUser()

    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data', [
        ("Empty fields", invalid_user.invalid_user_empty_fields()),
        ("Too long fields", invalid_user.invalid_user_too_long()),
        ("Wrong age", invalid_user.invalid_user_wrong_age()),
        ("Wrong types", invalid_user.invalid_user_wrong_types()),
    ])
    def test_post_create_user_negative(self, case, data):
        with allure.step(f'Try to create user with invalid data: {case}'):
            response = self.user.post_create_user(**data)
            allure.attach(str(data), name=f"Invalid user case: {case}",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 400, response.json()
        with allure.step(f'Validate fail response: '):
            with allure.step('Validate create invalid_user response: '):
                print(response.json(), "\n")
                validate_response = self.response_validator.validate_negative_requests(response.json(),
                                                                                       'PostCreateUser')
                allure.attach(str(response.json()), name="Validate create user response",
                              attachment_type=allure.attachment_type.JSON)
                assert validate_response

