import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import requests
from flight_search import FlightSearch
import os
from dotenv import load_dotenv
from pprint import pprint
from users import Users

load_dotenv()

USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


class DataManager(FlightSearch):
    def __init__(self):
        super().__init__()
        self.sheety_endpoint = os.getenv('SHEETY_ENDPOINT')
        self.sheety_token = os.getenv('SHEETY_TOKEN')

    def get_data_from_google_sheets_price(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.sheety_token}"
        }

        response = requests.get(url=self.sheety_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_aita_codes(self):
        data = self.get_data_from_google_sheets_price()["prices"]
        for i in range(len(data)):
            city = self.find_missing_aita_codes(data[i]["city"])
            iata_code = city["locations"][0]["code"]

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

    def insert_data_to_google_sheets(self, date_from, date_to, recipients):
        self.update_aita_codes()
        sheet_data = self.get_data_from_google_sheets_price()["prices"]
        for i in range(len(sheet_data)):
            # Flight deals
            deals = self.search_flight_deals(
                {sheet_data[i]['iataCode']},
                date_from,
                date_to,
                0)["data"]

            s = slice(0, 1)

            try:
                flight_data = deals[s][0]
                print("Success")
            except IndexError:
                flight_data = None
                print("No available flights")
                continue

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.sheety_token}"
            }

            params = {
                "price": {
                    "lowestPrice": flight_data['price'],
                },
            }

            response = requests.put(url=f"{self.sheety_endpoint}/{i + 2}", json=params, headers=headers)
            response.raise_for_status()

            if flight_data["price"] < sheet_data[i]["lowestPrice"]:
                # TODO: add link to emails
                self.send_mail(
                    f"Low price alert! Only £{flight_data['price']} to fly from CPH to {sheet_data[i]['iataCode']} ({sheet_data[i]['city']}) from {date_from} to {date_to}",
                    "Big Sales on Travels Right Meow!",
                    recipients
                )
            elif not sheet_data[i]["lowestPrice"]:
                self.send_mail(
                    f"Low price alert! Only £{flight_data['price']} to fly from CPH to {sheet_data[i]['iataCode']} ({sheet_data[i]['city']}) from {date_from} to {date_to}\n\n"
                    f"Flight has {flight_data['stop_over']} stop over via {flight_data['via_city']}",
                    "Big Sales on Travels Right Meow!",
                    recipients
                )
            else:
                print("No email were sent")

    def send_mail(self, description, header, recipients: list):
        message = MIMEMultipart()
        message["From"] = f"{USERNAME}"
        message["To"] = "; ".join(recipients)
        message["Subject"] = Header(s=f"{header}", charset="utf-8")

        # Add the text message
        msg_text = MIMEText(_text=f"{description}", _subtype="plain", _charset="utf-8")
        message.attach(msg_text)

        with smtplib.SMTP("smtp.gmail.com", 587) as conn:
            conn.starttls()
            conn.login(user=USERNAME, password=PASSWORD)
            conn.sendmail(
                from_addr=USERNAME,
                to_addrs="nicolajlpedersen@gmail.com",
                msg=f"{message.as_string()}"
            )
