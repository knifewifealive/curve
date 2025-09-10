from autotests.services.users.models.users_models import InformationGetSchema, InformationPostSchema, StatusSchema, UserGetSchema, UserPostSchema, UserPutSchema, UserValidationError, HTTPValidationError
from pydantic import ValidationError

class ResponseValidator:
    def __init__(self):
        self.APIRequestsSuccess = {
            'PostCreateUser': lambda response_json: StatusSchema(**response_json),
            'GetUserByNickname': lambda response_json: UserGetSchema(**response_json),
            'PutUserByNickname': lambda response_json: StatusSchema(**response_json),
            'DeleteUserByNickname': lambda response_json: UserGetSchema(**response_json),
            'PostCreateUserInfo': lambda response_json: StatusSchema(**response_json),
            'GetUserInfo': lambda response_json: StatusSchema(**response_json),
            'DeleteUserInfo': lambda response_json: StatusSchema(**response_json),
        }

        self.APIRequestsFailure = {
            'PostCreateUser': lambda response_json: HTTPValidationError(**response_json),
            'DeleteUserByNickname': lambda response_json: HTTPValidationError(**response_json),
            'PostCreateUserInfo': lambda response_json: HTTPValidationError(**response_json)
        }

    def validate_user(self, create_and_delete_user):
        return UserGetSchema(**create_and_delete_user)

    def validate_positive_requests(self, response_json, request_type):


        try:
            validator = self.APIRequestsSuccess.get(request_type)
            return validator(response_json)
        except ValidationError as e:
            print(f'Validation error: {e}')
        except KeyError as e:
            print(f'{e} .No test for the request: {request_type}')

    def validate_negative_requests(self, response_json, request_type):


        try:
            validator = self.APIRequestsFailure.get(request_type)
            return validator(response_json)
        except ValidationError as e:
            print(f'Validation error: {e}')
        except KeyError as e:
            print(f'{e} .No test for the request: {request_type}')