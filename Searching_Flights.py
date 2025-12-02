# In Searching_Flights.py

import CONFIG
import requests
from datetime import datetime
import ranking  

def _process_legs(flight_legs_data):
    structured_legs = []
    if not flight_legs_data: return structured_legs
    for i, leg_data in enumerate(flight_legs_data):
        structured_legs.append({
            "type": "flight", "departure_airport": leg_data.get("departure_airport", {}).get("name", "N/A"),
            "departure_time": leg_data.get("departure_airport", {}).get("time", "N/A"),
            "arrival_airport": leg_data.get("arrival_airport", {}).get("name", "N/A"),
            "arrival_time": leg_data.get("arrival_airport", {}).get("time", "N/A"),
            "duration": leg_data.get("duration", 0), "airline": leg_data.get("airline", "N/A")
        })
        if i < len(flight_legs_data) - 1:
            try:
                arrival_time = datetime.fromisoformat(leg_data["arrival_airport"]["time"])
                next_departure_time = datetime.fromisoformat(flight_legs_data[i + 1]["departure_airport"]["time"])
                layover_duration = (next_departure_time - arrival_time).total_seconds() / 60
                structured_legs.append({
                    "type": "layover", "location": leg_data.get("arrival_airport", {}).get("name", "N/A"),
                    "duration": int(layover_duration)
                })
            except (KeyError, ValueError):
                structured_legs.append({"type": "layover", "location": "N/A", "duration": "N/A"})
    return structured_legs


class search_flights:
    def __init__(self, ARRIVAL_ID, outbound_date, return_date):
        self.base_params = {
            "api_key": CONFIG.API_KEY,
            "engine": "google_flights",
            "departure_id": CONFIG.DEPARTURE_ID,
            "arrival_id": ARRIVAL_ID,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD",
            "hl": "en"
        }

    def _execute_api_call(self, params):
        print("Fetching data from SerpApi...")
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_outbound_flights(self):
        api_data = self._execute_api_call(self.base_params)
        if not api_data: return []
        extracted_flights = []
        for category in ["best_flights", "other_flights"]:
            for item in api_data.get(category, []):
                outbound_legs_data = item.get("flights", [])
                flight_info = {
                    "price": item.get("price"), "total_duration": item.get("total_duration"),
                    "num_connections": len(outbound_legs_data) - 1 if outbound_legs_data else 0,
                    "outbound_legs": _process_legs(outbound_legs_data),
                    "departure_token": item.get("departure_token")
                }
                extracted_flights.append(flight_info)
        return extracted_flights

    def get_best_return_flight(self, departure_token):
        if not departure_token: return None

        params = self.base_params.copy()
        params["departure_token"] = departure_token
        api_data = self._execute_api_call(params)
        if not api_data: return None

        all_return_options = []
        for category in ["best_flights", "other_flights"]:
            for item in api_data.get(category, []):
                return_legs_data = item.get("flights", [])
                option = {
                    "price": item.get("price"),
                    "total_duration": item.get("total_duration"),
                    "num_connections": len(return_legs_data) - 1 if return_legs_data else 0,
                    "return_legs": _process_legs(return_legs_data)
                }
                all_return_options.append(option)

        if not all_return_options: return None
        ranked_return_options = ranking.rank_and_filter_flights(all_return_options)
        return ranked_return_options[0] if ranked_return_options else None

