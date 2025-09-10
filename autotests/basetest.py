from autotests.services.users.api_users import User
from autotests.services.users.models.user_validation import ResponseValidator
from autotests.services.utils.fake_data import FakeUser

class BaseTest:

    def setup_method(self):

        self.user = User()
        self.random_user = FakeUser()
        self.response_validator = ResponseValidator()