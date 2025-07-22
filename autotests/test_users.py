import allure
import pytest
from autotests.basetest import BaseTest
from autotests.services.utils.fake_data import FakeUser


@allure.feature('User API')
class TestUsers(BaseTest):

    @allure.story('Setup Database')
    @pytest.mark.api_positive
    def test_setup_db(self, user):
        with allure.step('Clear all db'):
            response = user.post_setup_db_users()
            assert response.status_code == 200, response.json()

    @allure.story('Create user positive')
    @pytest.mark.api_positive
    def test_post_create_user(self, create_and_delete_user, response_validator):
        assert response_validator.validate_positive_requests(create_and_delete_user,'PostCreateUser')


invalid_user = FakeUser()


@pytest.mark.api_negative
@pytest.mark.parametrize('case, data', [
    ("Empty fields", invalid_user.invalid_user_empty_fields()),
    ("Too long fields", invalid_user.invalid_user_too_long()),
    ("Wrong age", invalid_user.invalid_user_wrong_age()),
    ("Wrong types", invalid_user.invalid_user_wrong_types()),
])
def test_post_create_user_negative(case, data, user, response_validator):
    with allure.step(f'Try to create user with invalid data: {case}'):
        response = user.post_create_user(**data)
        allure.attach(str(data), name=f"Invalid user case: {case}",
                      attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 400, response.json()

    with allure.step('Validate create invalid_user response: '):
        validate_response = response_validator.validate_negative_requests(response.json(),
                                                                          'PostCreateUser')
        allure.attach(str(response.json()), name="Validate create user response",
                      attachment_type=allure.attachment_type.JSON)
        assert validate_response
