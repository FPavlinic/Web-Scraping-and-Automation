# used libraries
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager


def flight_info():
    """Prints flight info with or without stopovers"""

    print(f"{flight_data.departure_city} to {flight_data.arrival_city}({flight_data.arrival_country}): ${flight_data.price}")

    if flight_data.stop_overs > 0:
        print(f"Flight has {flight_data.stop_overs} stop over, via {flight_data.via_city}")
    print(f"Departure time: {flight_data.departure_time.split('T')[0]} "
          f"at {flight_data.departure_time.split('T')[1]}\n")


def create_notification(stop_over):
    """Creates message to send via email using flight info"""

    basic_info = f"Low price alert! Only ${flight_data.price} " \
                 f"to fly from {flight_data.departure_city}-{flight_data.departure_airport_code} " \
                 f"to {flight_data.arrival_city}-{flight_data.arrival_airport_code}, " \
                 f"from {flight_data.departure_time.split('T')[0]} " \
                 f"to {flight_data.return_time.split('T')[0]}\n"
    stop_over_info = f"Flight has {flight_data.stop_overs} stop over, via {flight_data.via_city}\n"

    # check if there is stopovers --> different notification
    if stop_over:
        notification = basic_info + stop_over_info
    else:
        notification = basic_info
    return notification


data_manager = DataManager()  # create an object to work with table in Sheety
flight_search = FlightSearch(data_manager.sheet_data)  # create an object that finds flight using Tequila API
notification_manager = NotificationManager()  # create an object that sends notification if flight is cheaper than in Sheety table

# find missing IATA codes
for row in data_manager.sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_search.find_iata_code(row["city"])

data_manager.update_sheet_dict()  # updates table in Sheety with missing IATA codes

# find flight by IATA codes in Sheety table
for row in data_manager.sheet_data:
    search_data = flight_search.find_flights(fly_to=row["iataCode"], max_stopovers=0)  # search first direct flights

    if not search_data:  # if direct flights are not found
        search_data = flight_search.find_flights(fly_to=row["iataCode"], max_stopovers=2)  # search flights with stopovers (one each direction)

        if search_data:  # if there is flights with max 2 stopovers
            flight_data = FlightData(search_data, stop_overs=1)  # create an object to hold important flight info
            flight_info()  # print flight info

            # check if flight prices smaller than prices in Sheety table
            if notification_manager.compare_prices(sheet_price=row["lowestPrice"], flight_price=flight_data.price):
                notification_manager.send_sms(create_notification(stop_over=True))  # send sms
                notification_manager.send_mail(create_notification(stop_over=True), flight_data)  # send email

    else:  # if there is direct flights
        flight_data = FlightData(search_data, stop_overs=0)  # create an object to hold important flight info
        flight_info()  # print flight info

        # check if flight prices smaller than prices in Sheety table
        if notification_manager.compare_prices(sheet_price=row["lowestPrice"], flight_price=flight_data.price):
            notification_manager.send_sms(create_notification(stop_over=False))  # send sms
            notification_manager.send_mail(create_notification(stop_over=False), flight_data)  # send email
