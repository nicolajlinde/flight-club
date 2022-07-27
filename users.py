import os
from dotenv import load_dotenv
import requests

load_dotenv()


class Users:
    def __init__(self):
        self.sheety_token = os.getenv('SHEETY_TOKEN')
        self.sheety_endpoint = os.getenv('SHEETY_USERS_ENDPOINT')

    def create_user_account(self):
        first_name = input("What is your first name?: ")
        last_name = input("What is your lastname name?: ")
        email = input("What is your e-mail?: ")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.sheety_token}"
        }

        params = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            },
        }

        response = requests.post(url=f"{self.sheety_endpoint}", json=params, headers=headers)
        response.raise_for_status()

    def get_user_data(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.sheety_token}"
        }

        response = requests.get(url=self.sheety_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()