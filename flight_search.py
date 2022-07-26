import requests
import os
from dotenv import load_dotenv
load_dotenv()


class FlightSearch:
    def __init__(self):
        self.flight_endpoint = os.getenv('FLIGHT_ENDPOINT')
        self.flight_api = os.getenv('FLIGHT_API')
        self.flight_id = os.getenv('FLIGHT_ID')

    def search_flight_deals(self, fly_to: [], date_from: str, date_to: str):
        headers = {
            "Content-Type": "application/json",
            "apikey": self.flight_api
        }

        flight_params = {
            "fly_from": "BLL, AAL, CPH",
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to
        }

        response = requests.get(url=self.flight_endpoint, params=flight_params, headers=headers)
        response.raise_for_status()
        return response.json()

    def find_missing_aita_codes(self, city):
        endpoint = "https://tequila-api.kiwi.com/locations/query"

        headers = {
            "Content-Type": "application/json",
            "apikey": self.flight_api
        }

        params = {
            "term": city,
            "local": "en-US",
            "location_types": "airport"
        }

        response = requests.get(url=endpoint, headers=headers, params=params)
        return response.json()