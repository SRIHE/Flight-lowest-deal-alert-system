import requests

Shetty_Api_destination = "https://api.sheety.co/0efa68d1c710f2eae83ec6dfb8397ce7/flightclub/prices"
Shetty_Api_form="https://api.sheety.co/0efa68d1c710f2eae83ec6dfb8397ce7/flightclub/users"
class DataManager:

    def __init__(self):
        self.destination_data={}
        self.email_data={}

    def get_destination_data(self):
        response=requests.get(url=Shetty_Api_destination)
        data=response.json()
        self.destination_data=data['prices']
        return self.destination_data

    def get_user_emails(self):
        response=requests.get(url=Shetty_Api_form)
        data=response.json()
        print(data)
        """self.email_data=data['users']
        return self.email_data"""

    def update_destination_data(self):
        for city in self.destination_data:
            new_data={
                "price":{
                    "iataCode":city["iataCode"]
                }
            }
            response=requests.put(f"{Shetty_Api_destination}/{city["id"]}",json=new_data)
            print(response.text)

datamanager=DataManager()
datamanager.get_user_emails()
