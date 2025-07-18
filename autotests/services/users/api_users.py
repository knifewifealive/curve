from autotests.services.users.endpoints import UserEndpoints
from autotests.services.users.payloads import UserPayLoad
from requests import Response
import requests
import allure

class User:
    
    def __init__(self):
        self.payload = UserPayLoad
        self.endpoint = UserEndpoints
    
    @allure.step('Post request to setup and clear db')
    def post_clear_db_users(self) -> Response:
        response = requests.post(
            url=self.endpoint.setup_database()
        )
        return response
        
    @allure.step('Get request for all users')
    def get_all_users(self) -> Response:
        response = requests.get(
            url=self.endpoint.get_users()
        )
        return response
    
    @allure.step('Post request to create user')
    def post_create_user(self, **kwargs) -> Response:
        response = requests.post(
            url=self.endpoint.get_users(),
            json=self.payload.post_user_payload(**kwargs)
        )
        return response
    
    @allure.step('Get request for user by nickname')
    def get_user_by_nickname(self, nickname: str) -> Response:
        response = requests.get(
            url=self.endpoint.get_user_by_nickname(nickname)
        )
        return response

    @allure.step('Put request to update user age and job')
    def put_user_age_and_job(self, nickname: str, age: int, job: str) -> Response:
        response = requests.put(
            url = self.endpoint.put_user(nickname),
            json = self.payload.put_user_payload(age,job)
        )
        return response

    @allure.step('Delete request to Delete user')
    def delete_user(self, nickname: str) -> Response:
        response = requests.delete(
            url = self.endpoint.delete_user(nickname)
        )
        return response

    @allure.step('Post request to create user information')
    def post_create_user_info(self, nickname: str, information, explanation) -> Response:
        response = requests.post(
            url=self.endpoint.post_user_info(nickname),
            json=self.payload.post_user_info_payload(information, explanation)
        )
        return response

    @allure.step('Get request to get user info by nickname')
    def get_user_info(self, nickname: str) -> Response:
        response = requests.get(
            url=self.endpoint.get_user_info(nickname)
        )
        return response

    @allure.step('Delete request to delete user info')
    def delete_user_info(self, nickname: str, indormation_id: int) -> Response:
        response = requests.delete(
            url=self.endpoint.delete_user_info(nickname, indormation_id)
        )
        return response


