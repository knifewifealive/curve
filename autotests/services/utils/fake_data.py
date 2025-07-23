from faker import Faker
import random


class FakeUser:
    def __init__(self):
        self.fake = Faker()

    def valid_user(self) -> dict:
        """Генерация валидного пользователя"""
        return {
            "nickname": self.fake.user_name()[:20],
            "first_name": self.fake.first_name()[:20],
            "last_name": self.fake.last_name()[:20],
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.job()[:100],
        }

    # Invalid tests inputs cases
    def invalid_user_empty_fields(self) -> dict:
        """Пустые строки (нарушение min_length)"""
        return {
            "nickname": "",
            "first_name": "",
            "last_name": "",
            "age": 25,
            "job": ""
        }

    def invalid_user_too_long(self) -> dict:
        """Значения, превышающие max_length"""
        return {
            "nickname": self.fake.pystr(min_chars=21, max_chars=30),
            "first_name": self.fake.pystr(min_chars=21, max_chars=30),
            "last_name": self.fake.pystr(min_chars=21, max_chars=30),
            "age": 25,
            "job": self.fake.pystr(min_chars=101, max_chars=120)
        }

    def invalid_user_too_long_nickname(self) -> dict:
        """Значения, превышающие max_length"""
        return {
            "nickname": self.fake.pystr(min_chars=21, max_chars=30),
            "first_name": self.fake.first_name()[:20],
            "last_name": self.fake.last_name()[:20],
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.job()[:100],
        }

    def invalid_user_nickname_type(self) -> dict:
        return {
            "nickname": self.fake.random_int(min=1, max=99),
            "first_name": self.fake.first_name()[:20],
            "last_name": self.fake.last_name()[:20],
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.job()[:100],
        }

    def invalid_user_nickname_is_empty(self) -> dict:
        return {
            "nickname": "",
            "first_name": self.fake.first_name()[:20],
            "last_name": self.fake.last_name()[:20],
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.job()[:100],
        }

    def invalid_user_wrong_age(self) -> dict:
        """Возраст вне диапазона (ge=1, le=99)"""
        return {
            "nickname": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "age": random.choice([0, -5, 150]),
            "job": self.fake.job()
        }

    def invalid_user_wrong_types(self) -> dict:
        """Неверные типы данных (например, int вместо str)"""
        return {
            "nickname": 12345,  # должно быть str
            "first_name": 5678,  # должно быть str
            "last_name": None,  # должно быть str
            "age": "twenty",  # должно быть int
            "job": 98765  # должно быть str
        }

    # PUT
    def put_user_valid(self) -> dict:
        return {
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.job()[:100],
        }

    def put_user_invalid_type_age_and_job(self) -> dict:
        return {
            "age": self.fake.name(),
            "job": self.fake.random_int(min=1, max=2)
        }

    def put_user_invalid_type_age(self) -> dict:
        return {
            "age": self.fake.name(),
            "job": self.fake.job()[:100]
        }

    def put_user_invalid_type_job(self) -> dict:
        return {
            "age": self.fake.random_int(min=1, max=99),
            "job": self.fake.random_int(min=1, max=99)
        }

    # User_Info



