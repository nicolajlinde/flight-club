import requests
from flight_search import FlightSearch
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager(FlightSearch):
    def __init__(self):
        super().__init__()
        self.sheety_endpoint = os.getenv('SHEETY_ENDPOINT')
        self.sheety_token = os.getenv('SHEETY_TOKEN')

    def get_data_from_google_sheets(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.sheety_token}"
        }

        response = requests.get(url=self.sheety_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_aita_codes(self):
        data = self.get_data_from_google_sheets()["prices"]
        for i in range(len(data)):
            city = self.find_missing_aita_codes(data[i]["city"])
            city_name = city["locations"][0]["city"]["name"]
            iata_code = city["locations"][0]["code"]

            if data[i]["city"] == city_name and len(data[i]["iataCode"]) == 0:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.sheety_token}"
                }

                params = {
                    "price": {
                        "iataCode": iata_code,
                    }
                }

                response = requests.put(url=f"{self.sheety_endpoint}/{i + 2}", json=params, headers=headers)
                print(response.text)
                response.raise_for_status()
                i += 1

    def insert_data_to_google_sheets(self):
        i = 2
        self.update_aita_codes()
        sheet_data = self.get_data_from_google_sheets()["prices"]
        for sheet in sheet_data:
            # Flight deals
            deals = self.search_flight_deals(
                {sheet['iataCode']},
                "01/08/2022",
                "01/08/2022")["data"]

            s = slice(0, 1)
            flight_data = deals[s][0]

            if sheet["lowestPrice"] > flight_data["price"]:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.sheety_token}"
                }

                params = {
                    "price": {
                        "lowestPrice": flight_data["price"],
                    }
                }

                response = requests.put(url=f"{self.sheety_endpoint}/{i}", json=params, headers=headers)
                response.raise_for_status()
                i += 1
