import time
from datetime import datetime,timedelta
from flight_data import find_cheapest_flight
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

API_KEY="54LnoiZ5pVEIHUy3AhwNcLwgDh47Ytl1"
API_SECRET="A9Gr4lMCHQsNdr3A"

ORGIN_CITY_DATA="LON"

data_manager=DataManager()
sheet_data=data_manager.get_destination_data()
notification=NotificationManager()

flight_search=FlightSearch()

for row in sheet_data:
    if sheet_data[0]['iataCode'] == "":
        row['iataCode']=flight_search.get_destination_code(row['city'])
        time.sleep(2)
print(sheet_data)

data_manager.destination_data=sheet_data
data_manager.update_destination_data()

customer_details=data_manager.get_user_emails()
customer_email_list=[data["enterYourEmailId?"] for data in customer_details]
print(customer_email_list)

tomorrow=datetime.now()+timedelta(days=1)
six_months=datetime.now()+timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}:")
    flights=flight_search.check_flights(ORGIN_CITY_DATA,destination['iataCode'],tomorrow,six_months)
    cheapest_flight=find_cheapest_flight(flights)
    print(f"{destination['city']}:${cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price =="N/A":
        print(f"No direct flights to {destination["city"]}. Looking for flights...")
        stop_over_flights=flight_search.check_flights(
            ORGIN_CITY_DATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months,
            is_direct=False
        )
        cheapest_flight=find_cheapest_flight(stop_over_flights)
        print(f"Cheapest indirect flights price is : ${cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                    f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                    f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                    f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                    f"with {cheapest_flight.stops} stop(s) " \
                    f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        notification.send_sms(message_body=message)

        for email in customer_email_list:
            notification.send_email(receiver_email=email, message=message)