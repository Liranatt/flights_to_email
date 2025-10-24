import CONFIG
import SEND_EMAIL
import create_html
import Searching_Flights
import ranking


# MODIFIED: The job function now also accepts date strings
def job(destinations_list, receiver_emails_list, outbound_date_str, return_date_str):
    flights_data_per_destination = {}

    print("--- Starting flight check ---")
    for destination in destinations_list:
        print(f"Searching flights for destination: {destination}")

        # MODIFIED: Pass the dates to the search_flights constructor
        search_instance = Searching_Flights.search_flights(
            destination,
            outbound_date_str,
            return_date_str
        )

        # ... (rest of the flight search logic is identical) ...
        all_outbound_flights = search_instance.get_outbound_flights()

        if all_outbound_flights:
            print(f"Found {len(all_outbound_flights)} outbound options. Ranking and finding best return flights...")
            top_outbound = ranking.rank_and_filter_flights(all_outbound_flights)

            full_trip_details = []
            for outbound_flight in top_outbound:
                best_return_flight = search_instance.get_best_return_flight(outbound_flight['departure_token'])

                if best_return_flight:
                    final_trip = {
                        'outbound_legs': outbound_flight['outbound_legs'],
                        'return_legs': best_return_flight['return_legs'],
                        'price': best_return_flight['price'],
                        'total_duration': best_return_flight['total_duration'],
                        'num_connections': outbound_flight['num_connections'] + best_return_flight['num_connections']
                    }
                    full_trip_details.append(final_trip)

            print(f"Re-ranking {len(full_trip_details)} complete trip options...")
            final_ranked_trips = ranking.rank_and_filter_flights(full_trip_details)
            flights_data_per_destination[destination] = final_ranked_trips
        else:
            print(f"No flights found for {destination}")
            flights_data_per_destination[destination] = []

    if flights_data_per_destination:
        html_report = create_html.generate_html_summary(flights_data_per_destination)
        SEND_EMAIL.send_html_email(html_report, receiver_emails_list)
    else:
        print("No flight data found for any destination.")

    print("--- Flight check finished ---")
    return True


# MODIFIED: We no longer want this to run automatically
# We will call the job() function from our new app.py file
if __name__ == "__main__":
    # You can keep this for testing, but it's no longer the main entry point
    print("Running in test mode. Use app.py to run the UI.")
    # test_dests = ["ATH", "BCN"]
    # test_emails = ["your_test_email@gmail.com"]
    # job(test_dests, test_emails)
    pass
