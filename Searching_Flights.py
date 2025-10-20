# In Searching_Flights.py

import CONFIG
import requests
from datetime import datetime

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
        if not self.response or self.response.status_code != 200:
             print(f"Failed to get a valid response for {self.params['arrival_id']}")
             return []

        api_data = self.response.json()
        flight_categories = ["best_flights", "other_flights"]
        extracted_flights = []

        for category in flight_categories:
            if category in api_data:
                for item in api_data.get(category, []):
                    flight_legs_data = item.get("flights", [])
                    
                    structured_legs = []
                    # Process each flight leg and the layover that follows it
                    for i, leg_data in enumerate(flight_legs_data):
                        # Add the flight leg
                        structured_legs.append({
                            "type": "flight",
                            "departure_airport": leg_data.get("departure_airport", {}).get("name", "N/A"),
                            "departure_time": leg_data.get("departure_airport", {}).get("time", "N/A"),
                            "arrival_airport": leg_data.get("arrival_airport", {}).get("name", "N/A"),
                            "arrival_time": leg_data.get("arrival_airport", {}).get("time", "N/A"),
                            "duration": leg_data.get("duration", 0),
                            "airline": leg_data.get("airline", "N/A")
                        })

                        # If this isn't the last leg, calculate the layover
                        if i < len(flight_legs_data) - 1:
                            try:
                                arrival_time = datetime.fromisoformat(leg_data["arrival_airport"]["time"])
                                next_departure_time = datetime.fromisoformat(flight_legs_data[i+1]["departure_airport"]["time"])
                                layover_duration = (next_departure_time - arrival_time).total_seconds() / 60
                                
                                structured_legs.append({
                                    "type": "layover",
                                    "location": leg_data.get("arrival_airport", {}).get("name", "N/A"),
                                    "duration": int(layover_duration)
                                })
                            except (KeyError, ValueError):
                                # Handle cases where time parsing might fail
                                structured_legs.append({"type": "layover", "location": "N/A", "duration": "N/A"})
                    
                    flight_info = {
                        "price": item.get("price"),
                        "total_duration": item.get("total_duration"),
                        "num_connections": len(flight_legs_data) - 1 if flight_legs_data else 0,
                        "legs": structured_legs # The new detailed structure
                    }
                    extracted_flights.append(flight_info)

        return extracted_flights
