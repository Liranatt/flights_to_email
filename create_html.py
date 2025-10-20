# In create_html.py

import CONFIG
from datetime import datetime

def generate_html_summary(flight_data_per_destination):
    """
    Generates a creative HTML summary where connecting flights are broken down
    into detailed legs and layovers.
    """
    print("Generating creative HTML summary...")

    html_style = """
    <style>
        body { font-family: sans-serif; margin: 20px; color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; font-size: 14px; }
        th, td { border: 1px solid #ddd; text-align: left; padding: 12px; }
        thead { background-color: #4CAF50; color: white; }
        h1, h2 { color: #4CAF50; border-bottom: 2px solid #f2f2f2; padding-bottom: 5px;}
        .flight-leg td { background-color: #f9f9f9; }
        .layover-leg td { background-color: #fff8e1; color: #795548; text-align: center; font-style: italic; }
        .merged-cell { vertical-align: middle; text-align: center; font-weight: bold; font-size: 16px; }
    </style>
    """

    html_body = f"<h1>Weekly Flight Deals Summary</h1><p>Report generated on: {datetime.now().strftime('%Y-%m-%d')}</p>"

    for destination_code, flight_list in flight_data_per_destination.items():
        html_body += f"<h2>Flights from {CONFIG.DEPARTURE_ID} to {destination_code}</h2>"
        
        if not flight_list:
            html_body += "<p>No flights found for this destination.</p>"
            continue

        html_body += """
        <table>
            <thead>
                <tr>
                    <th style="width:40%;">Departure & Arrival</th>
                    <th style="width:40%;">Journey Details</th>
                    <th style="width:10%;">Price ($)</th>
                    <th style="width:10%;">Total Duration (m)</th>
                </tr>
            </thead>
            <tbody>
        """
        for flight in flight_list:
            if flight['num_connections'] == 0 and flight['legs']:
                # --- A. SIMPLE ROW FOR DIRECT FLIGHTS ---
                leg = flight['legs'][0]
                html_body += f"""
                <tr class="flight-leg">
                    <td><b>From:</b> {leg['departure_airport']}<br><small>({leg['departure_time']})</small></td>
                    <td><b>To:</b> {leg['arrival_airport']}<br><small>({leg['arrival_time']})</small></td>
                    <td class="merged-cell">{flight['price']}</td>
                    <td class="merged-cell">{flight['total_duration']}</td>
                </tr>"""
            elif flight['legs']:
                # --- B. CREATIVE BLOCK FOR CONNECTING FLIGHTS ---
                rowspan = len(flight['legs'])
                
                # Loop through each leg (flight or layover)
                for i, leg in enumerate(flight['legs']):
                    if i == 0:
                        # --- First leg row: includes the rowspan cells for Price and Duration ---
                        html_body += f"""
                        <tr class="flight-leg">
                            <td><b>From:</b> {leg['departure_airport']}<br><small>({leg['departure_time']})</small></td>
                            <td><b>To:</b> {leg['arrival_airport']}<br><small>({leg['arrival_time']})</small><br><small><i>({leg['airline']}, {leg['duration']} min)</i></small></td>
                            <td class="merged-cell" rowspan="{rowspan}">{flight['price']}</td>
                            <td class="merged-cell" rowspan="{rowspan}">{flight['total_duration']}</td>
                        </tr>"""
                    elif leg['type'] == 'layover':
                        # --- Layover row ---
                        html_body += f"""
                        <tr class="layover-leg">
                            <td colspan="2"><b>Layover at {leg['location']}</b> ({leg['duration']} min)</td>
                        </tr>"""
                    else: # It's a subsequent flight leg
                        # --- Subsequent flight leg row (no Price/Duration cells) ---
                        html_body += f"""
                        <tr class="flight-leg">
                            <td><b>From:</b> {leg['departure_airport']}<br><small>({leg['departure_time']})</small></td>
                            <td><b>To:</b> {leg['arrival_airport']}<br><small>({leg['arrival_time']})</small><br><small><i>({leg['airline']}, {leg['duration']} min)</i></small></td>
                        </tr>"""
        html_body += "</tbody></table>"

    full_html = f"<!DOCTYPE html><html><head>{html_style}</head><body>{html_body}</body></html>"
    return full_html
