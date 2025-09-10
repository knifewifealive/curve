url = 'http://127.0.0.1:8000/'


class UserEndpoints:

    @staticmethod
    def setup_database():
        return f'{url}/setup_database'

    @staticmethod
    def get_users():
        return f'{url}/users'

    @staticmethod
    def get_user_by_nickname(nickname: str) -> str:
        return f'{url}/users/{nickname}'

    @staticmethod
    def put_user(nickname: str) -> str:
        return f'{url}/users/{nickname}'

    @staticmethod
    def delete_user(nickname: str) -> str:
        return f'{url}/users/{nickname}'

    # User information
    @staticmethod
    def get_user_info(nickname: str) -> str:
        return f'{url}/users/{nickname}/information'

    @staticmethod
    def post_user_info(nickname: str) -> str:
        return f'{url}/users/{nickname}/information'

    @staticmethod
    def delete_user_info(nickname: str, information_id: int) -> str:
        return f'{url}/{nickname}/information/{information_id}'
