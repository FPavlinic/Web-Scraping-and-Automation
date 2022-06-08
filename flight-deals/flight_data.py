class FlightData:
    """Models flight info storage"""

    def __init__(self, flight_data, stop_overs):
        self.airline = flight_data["airlines"]
        self.departure_country = flight_data["countryFrom"]["name"]
        self.departure_city = flight_data["cityFrom"]
        self.departure_airport_code = flight_data["flyFrom"]
        self.departure_time = flight_data["route"][0]["local_departure"].split('.')[0]
        self.arrival_country = flight_data["countryTo"]["name"]
        self.arrival_city = flight_data["cityTo"]
        self.arrival_airport_code = flight_data["flyTo"]
        self.return_time = flight_data["route"][2]["local_departure"].split('.')[0]
        self.price = flight_data["price"]
        self.available_seats = flight_data["availability"]["seats"]
        self.stop_overs = stop_overs
        if self.stop_overs:
            self.via_city = flight_data["route"][0]['cityTo']
