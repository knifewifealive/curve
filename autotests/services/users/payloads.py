class UserPayLoad:
    @staticmethod
    def post_user_payload(nickname: str, first_name: str, last_name: str, age: int, job: str):

        data = {
            "nickname": nickname,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "job": job
        }
        return data

    @staticmethod
    def put_user_payload(age: int, job: str):

        data = {
            'age': age,
            'job': job
        }
        return data

    @staticmethod
    def post_user_info_payload(information: str, explanation: str):
        
        data = {
            "information": information,
            "explanation": explanation
        }
        return data
    
    