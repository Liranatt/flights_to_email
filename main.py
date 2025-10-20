# In main.py

import CONFIG
import SEND_EMAIL
import create_html
import Searching_Flights
import ranking


def job():
    destinations = ["ATH", "BCN", "MUC", "VIE"]
    flights_data_per_destination = {}

    print("--- Starting weekly flight check ---")
    for destination in destinations:
        print(f"Searching flights for destination: {destination}")
        search_instance = Searching_Flights.search_flights(destination)

        # STEP 1: Get all available outbound flights
        all_outbound_flights = search_instance.get_outbound_flights()

        if all_outbound_flights:
            print(f"Found {len(all_outbound_flights)} outbound options. Ranking and finding best return flights...")
            top_outbound = ranking.rank_and_filter_flights(all_outbound_flights)

            full_trip_details = []
            for outbound_flight in top_outbound:
                # STEP 2: Get the BEST return flight for this specific outbound option
                best_return_flight = search_instance.get_best_return_flight(outbound_flight['departure_token'])

                if best_return_flight:
                    # Combine the outbound flight with its best return flight
                    final_trip = {
                        'outbound_legs': outbound_flight['outbound_legs'],
                        'return_legs': best_return_flight['return_legs'],
                        # Use the FINAL price and duration from the return flight call
                        'price': best_return_flight['price'],
                        'total_duration': best_return_flight['total_duration'],
                        # The ranking function needs num_connections, so we calculate it here
                        'num_connections': outbound_flight['num_connections'] + best_return_flight['num_connections']
                    }
                    full_trip_details.append(final_trip)

            # STEP 3: Re-rank the final list of complete trips based on their final price/duration
            print(f"Re-ranking {len(full_trip_details)} complete trip options...")
            final_ranked_trips = ranking.rank_and_filter_flights(full_trip_details)
            flights_data_per_destination[destination] = final_ranked_trips
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
