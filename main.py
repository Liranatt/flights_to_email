# In main.py

import CONFIG
import SEND_EMAIL
import create_html
import Searching_Flights
import ranking  # <-- Import the new ranking module
import os 

def job():
    destinations = ["ATH", "BCN", "MUC", "VIE"]
    flights_data_per_destination = {}
    print(f"DEBUG: API Key being used starts with: {os.environ.get('API_KEY', 'KEY_NOT_FOUND')[:5]}")
    print("--- Starting weekly flight check ---")
    for destination in destinations:
        print(f"Searching flights for destination: {destination}")
        search_instance = Searching_Flights.search_flights(destination)

        # Get all flights found for the destination
        all_flights = search_instance.extracting_info()

        if all_flights:
            print(f"Found {len(all_flights)} flights for {destination}. Ranking...")
            # Rank the flights and keep only the top 5
            top_flights = ranking.rank_and_filter_flights(all_flights)
            flights_data_per_destination[destination] = top_flights
        else:
            print(f"No flights found for {destination}")
            flights_data_per_destination[destination] = []

    if flights_data_per_destination:
        html_report = create_html.generate_html_summary(flights_data_per_destination)
        SEND_EMAIL.send_html_email(html_report)
    else:
        print("No flight data found for any destination.")

    print("--- Weekly flight check finished ---")


if __name__ == "__main__":

    job()
