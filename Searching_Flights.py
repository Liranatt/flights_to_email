# In Searching_Flights.py

import CONFIG
import requests

class search_flights:
    def __init__(self, ARRIVAL_ID):
        self.params = {
            "api_key": CONFIG.API_KEY,
            "engine": "google_flights",
            "departure_id": CONFIG.DEPARTURE_ID,
            "arrival_id": ARRIVAL_ID,
            "outbound_date": CONFIG.OUTBOUND_DATE,
            "return_date": CONFIG.RETURN_DATE,
            "currency": "USD",
            "hl": "en"
        }
        self.response = None

    def execute_search(self):
        print("Fetching data from SerpApi...")
        self.response = requests.get("https://serpapi.com/search", params=self.params)

    def extracting_info(self):
        if not self.response:
            self.execute_search()

        extract_flights = []
        if not self.response or self.response.status_code != 200:
             print(f"Failed to get a valid response for {self.params['arrival_id']}")
             return extract_flights

        api_data = self.response.json()
        flight_categories = ["best_flights", "other_flights"]

        for category in flight_categories:
            if category in api_data:
                for item in api_data[category]:
                    flight_legs = item.get("flights", [])
                    flight_info = {
                        "departure_airport": flight_legs[0].get("departure_airport", {}).get("name", "N/A") if flight_legs else "N/A",
                        "departure_time": flight_legs[0].get("departure_airport", {}).get("time", "N/A") if flight_legs else "N/A",
                        "arrival_airport": flight_legs[-1].get("arrival_airport", {}).get("name", "N/A") if flight_legs else "N/A",
                        "arrival_time": flight_legs[-1].get("arrival_airport", {}).get("time", "N/A") if flight_legs else "N/A",
                        "airline": flight_legs[0].get("airline", "N/A") if flight_legs else "N/A",
                        "total_duration": item.get("total_duration"), # Keep as None if missing
                        "price": item.get("price"), # Keep as None if missing
                        "type": item.get("type", "N/A"),
                        # --- ADDED FOR RANKING ---
                        "num_connections": len(flight_legs) - 1 if flight_legs else 0
                    }
                    extract_flights.append(flight_info)

        return extract_flights