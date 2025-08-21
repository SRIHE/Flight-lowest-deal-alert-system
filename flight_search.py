import requests
from datetime import datetime

FLIGHT_API_KEY="API KEY"
FLIGHT_SECRET_KEY="API PASSWORD"


class FlightSearch:

    def __init__(self):
        self.api_key=FLIGHT_API_KEY
        self.secret_key=FLIGHT_SECRET_KEY
        self.token=self._get_new_token()

    def _get_new_token(self):

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        body={
            'grant_type':'client_credentials',
            'client_id':self.api_key,
            'client_secret':self.secret_key,
        }

        response1=requests.post("https://test.api.amadeus.com/v1/security/oauth2/token",headers=headers,data=body)
        print(f"Your Token is {response1.json()['access_token']}")
        print(f"Your Token expires in {response1.json()['expires_in']} seconds")
        return response1.json()['access_token']

    def get_destination_code(self,city_name):

        print(f"Using this token to get destination {self.token}")
        headers={
            "Authorization":f"Bearer {self.token}"
        }

        query={
            "keyboard":city_name,
            "max":"2",
            "include":"AIRPORTS"
        }

        response=requests.get(url="https://test.api.amadeus.com/v1/reference-data/locations/cities",headers=headers,params=query)
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code=response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError:No airport code found for {city_name}.")
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not found"

        print(response.text)

    def check_flights(self,origin_code,destination_code,from_time,to_time,is_direct=True):

        headers={"Authorization":f"Bearer {self.token}"}
        query={
            "originLocationCode":origin_code,
            "destinationLocationCode":destination_code,
            "departureDate":from_time.strftime("%Y-%m-%d"),
            "returnDate":to_time.strftime("%Y-%m-%d"),
            "adults":1,
            "nonStop":"true" if is_direct else "false",
            "currencyCode":"INR",
            "max":"10"
        }

        response=requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers",headers=headers,params=query)

        if response.status_code!=200:
            print(f"check flights() response code:{response.status_code}")
            print("There was a problem with the flight search")
            print(response.text)
            return None

        return response.json()
