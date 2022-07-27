#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from users import Users
import users

# Users
user = Users()
user.create_user_account()
data = user.get_user_data()["users"]

emails = []
for x in data:
    emails.append(x['email'])

# Google sheet data
google = DataManager()
google.insert_data_to_google_sheets("01/08/2022", "27/08/2022", emails)

