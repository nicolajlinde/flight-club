#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import flight_data
from flight_search import FlightSearch
import data_manager

# Google sheet data
google = data_manager.DataManager()
google.insert_data_to_google_sheets("01/08/2022", "01/08/2022")

