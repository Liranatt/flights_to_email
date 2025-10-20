# In create_html.py

import CONFIG
from datetime import datetime


def generate_html_summary(flight_data_per_destination):
    """
    Generates a single HTML string containing formatted tables for all flight data.
    """
    print("Generating HTML summary...")

    # CSS for styling the table to make it look professional
    html_style = """
    <style>
        body { font-family: sans-serif; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }
        thead { background-color: #f2f2f2; }
        h1, h2 { color: #333333; }
    </style>
    """

    html_body = f"<h1>Weekly Multi-Destination Flight Summary</h1>"
    html_body += f"<p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>"

    for destination_code, flight_list in flight_data_per_destination.items():
        html_body += f"<h2>Flights from {CONFIG.DEPARTURE_ID} to {destination_code}</h2>"

        if not flight_list:
            html_body += "<p>No flights found for this destination.</p>"
            continue

        html_body += """
        <table>
            <thead>
                <tr>
                    <th>Departure</th>
                    <th>Arrival</th>
                    <th>Airline</th>
                    <th>Price ($)</th>
                    <th>Duration (m)</th>
                </tr>
            </thead>
            <tbody>
        """
        for flight in flight_list:
            html_body += f"""
                <tr>
                    <td>{flight['departure_airport']}<br>({flight['departure_time']})</td>
                    <td>{flight['arrival_airport']}<br>({flight['arrival_time']})</td>
                    <td>{flight['airline']}</td>
                    <td>{flight['price']}</td>
                    <td>{flight['total_duration']}</td>
                </tr>
            """
        html_body += "</tbody></table>"

    # Combine style and body into a full HTML document
    full_html = f"<!DOCTYPE html><html><head>{html_style}</head><body>{html_body}</body></html>"
    return full_html