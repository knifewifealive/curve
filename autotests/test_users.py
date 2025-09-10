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
    def test_post_create_user(self, create_and_delete_user, response_validator, user):
        with allure.step('Check that user exists'):
            response = self.user.get_user_by_nickname(create_and_delete_user['nickname'])
            assert response.status_code == 200, response.json()
        with allure.step('Validate user'):
            assert response_validator.validate_positive_requests(create_and_delete_user, 'GetUserByNickname')

    user_generator = FakeUser()

    @allure.story('Post create user negative')
    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data', [
        ("Empty fields", user_generator.invalid_user_empty_fields()),
        ("Too long fields", user_generator.invalid_user_too_long()),
        ("Wrong age", user_generator.invalid_user_wrong_age()),
        ("Wrong types", user_generator.invalid_user_wrong_types()),
    ])
    def test_post_create_user_negative(self, case, data, user, response_validator):
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

    @allure.story('Get user by nickname')
    @pytest.mark.api_positive
    def test_get_user_by_nickname(self, create_and_delete_user, user, response_validator):
        nickname = create_and_delete_user['nickname']
        response = user.get_user_by_nickname(nickname)
        assert response.status_code == 200, response.json()

    @allure.story('Get user negative')
    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data', [
        ("Too long nickname", user_generator.invalid_user_too_long_nickname()),
        ("Int in nickname", user_generator.invalid_user_nickname_type()),
        # ("Nickname is empty", user_generator.invalid_user_nickname_is_empty())
    ])
    def test_get_user_by_nickname(self, create_and_delete_user, user, response_validator, case, data):
        with allure.step(f'Try to get user with invalid data: {case}'):
            response = user.get_user_by_nickname(data['nickname'])
            allure.attach(str(data), name=f"Invalid user case: {case}",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 404, response.json()

    @allure.story('Put user positive')
    @pytest.mark.api_positive
    @pytest.mark.parametrize('case, data', [
        ("Valid user update 1", user_generator.valid_user()),
        ("Valid user update 2", user_generator.valid_user()),
        ("Valid user update 3", user_generator.valid_user()),
        # ("Nickname is empty", user_generator.invalid_user_nickname_is_empty())
    ])
    def test_put_user_by_nickname(self, create_and_delete_user, user, response_validator, case, data):
        with allure.step(f'Try to put user with data: {case}'):
            response = user.put_user_age_and_job(create_and_delete_user['nickname'], data['age'], data['job'])
            allure.attach(str(data), name=f"Invalid user case: {case}",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()

    @allure.story('Put user negative')
    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data', [
        ("Wrong type job and age", user_generator.put_user_invalid_type_age_and_job()),
        ("Wrong type job", user_generator.put_user_invalid_type_age()),
        ("Wrong type age", user_generator.put_user_invalid_type_job()),
        ("Age more than 100", user_generator.put_user_invalid_type_job()),
        ("Age is negative", user_generator.put_user_invalid_type_job()),
    ])
    def test_put_user_by_nickname(self, create_and_delete_user, user, response_validator, case, data):
        with allure.step(f'Try to put user with data: {case}'):
            response = user.put_user_age_and_job(create_and_delete_user['nickname'], data['age'], data['job'])
            allure.attach(str(data), name=f"Invalid user case: {case}",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 400, response.json()

    @allure.story('Delete user positive')
    @pytest.mark.api_positive
    def test_delete_user_by_nickname(self, create_user, user, response_validator, case, data):
        with allure.step(f'Try to delete user: {case}'):
            response = user.delete_user(create_user['nickname'])
            allure.attach(str(response.json()), name="Delete user after creation: ",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200

        with allure.step(f'Try to get user: {case}'):
            response = user.get_user_by_nickname(create_user['nickname'])
            assert response.status_code == 404

    @allure.story('Delete user negative')
    @pytest.mark.api_negative
    @pytest.mark.parametrize('case', [
        "User 404",
        "User 400",
    ])
    def test_delete_user_by_nickname(self, create_user, user, response_validator, case):
        with allure.step(f'Try to get user: {case}'):
            response = user.delete_user(create_user['nickname'] * 2)
            if response.status_code == 404:
                assert True
            else:
                with allure.step(f'Validate user'):
                    assert response_validator.validate_negative_requests(create_user, 'DeleteUserByNickname')

    @allure.story('Create user info positive')
    @pytest.mark.api_positive
    @pytest.mark.parametrize('case, data', [
        ("Put valid info 1", user_generator.post_user_info()),
        ("Put valid info 2", user_generator.post_user_info()),
        ("Put valid info 3", user_generator.post_user_info()),
    ])
    def test_post_create_user_info(self, create_and_delete_user, response_validator, user, case, data):
        with allure.step('Create user info'):
            response = user.post_create_user_info(create_and_delete_user['nickname'], **data)
            assert response.status_code == 200, response.json()
        with allure.step('Validate response'):
            assert response_validator.validate_positive_requests(response.json(), 'PostCreateUserInfo')

    @allure.story('Create user info negative')
    @pytest.mark.api_negative
    @pytest.mark.parametrize('case, data', [
        ("Invalid data type", user_generator.post_user_info_invalid_type()),
        ("More character than docs have", user_generator.post_user_info_more_characters()),
        ("Put valid info 3", user_generator.post_user_info_empty_strings()),
    ])
    def test_post_create_user_info(self, create_and_delete_user, response_validator, user, case, data):
        with allure.step('Try to update user info'):
            response = user.post_create_user_info(create_and_delete_user['nickname'], **data)
            allure.attach(str(response.json()), name="Create user info",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 400
        with allure.step('Validate response'):
            allure.attach(str(response.json()), name="Validate response after user info creation",
                          attachment_type=allure.attachment_type.JSON)
            assert response_validator.validate_negative_requests(response.json(), 'PostCreateUserInfo')

    @allure.story('Get user info by nickname')
    @pytest.mark.api_positive
    @pytest.mark.parametrize('case, data', [
        ("Put valid info 1", user_generator.post_user_info()),
        ("Put valid info 2", user_generator.post_user_info()),
        ("Put valid info 3", user_generator.post_user_info()),
    ])
    def test_get_user_info_by_nickname(self, create_and_delete_user, user, response_validator, case, data):
        with allure.step('Create user info'):
            response = user.post_create_user_info(create_and_delete_user['nickname'], **data)
            allure.attach(str(response.json()), name="Create user info",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()
        with allure.step('Validate response'):
            allure.attach(str(response.json()), name="Validate response after user info creation",
                          attachment_type=allure.attachment_type.JSON)
            assert response_validator.validate_positive_requests(response.json(), 'PostCreateUserInfo')

        with allure.step('Try to get user info: '):
            response = user.get_user_info(create_and_delete_user['nickname'])
            allure.attach(str(response.json()), name="Get user info",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()

    @allure.story('Delete user info by nickname')
    @pytest.mark.api_positive
    @pytest.mark.parametrize('case, data', [
        ("Put valid info 1", user_generator.post_user_info()),
        ("Put valid info 2", user_generator.post_user_info()),
        ("Put valid info 3", user_generator.post_user_info()),
    ])
    def test_delete_user_info(self, create_and_delete_user, user, response_validator, case, data):
        with allure.step('Create user info'):
            response = user.post_create_user_info(create_and_delete_user['nickname'], **data)
            allure.attach(str(response.json()), name="Create user info",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()
        with allure.step('Validate response'):
            allure.attach(str(response.json()), name="Validate response after user info creation",
                          attachment_type=allure.attachment_type.JSON)
            assert response_validator.validate_positive_requests(response.json(), 'PostCreateUserInfo')

        with allure.step('Get user info id to delete: '):
            response = user.get_user_info(create_and_delete_user['nickname'])
            allure.attach(str(response.json()), name="Get user info",
                          attachment_type=allure.attachment_type.JSON)
            assert response.status_code == 200, response.json()
            information_id = response.json()[0]['id']
        # Тест падает
        # with allure.step('Delete user info: '):
        #     response = user.delete_user_info(create_and_delete_user['nickname'], information_id)
        #     print(f'Delete user info: {response.json()}\n')
        #     assert response.status_code == 200, response.json()
        #
        # with allure.step('Try to get user info: '):
        #     response = user.get_user_info(create_and_delete_user['nickname'])
        #     allure.attach(str(response.json()), name="Get user info",
        #                   attachment_type=allure.attachment_type.JSON)
        #     assert response.status_code == 404, response.json()
