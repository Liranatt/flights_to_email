# In create_html.py

import CONFIG
from datetime import datetime


def _generate_leg_rows_html(legs):
    """Helper function to generate HTML table rows for a set of flight legs."""
    html = ""
    if not legs:
        return "<tr><td colspan='2' data-label='Details'><i>No flight details provided.</i></td></tr>"

    for leg in legs:
        if leg['type'] == 'layover':
            html += f"""
            <tr class="layover-leg">
                <td colspan="2" data-label="Layover">⌛ Layover at {leg['location']} ({leg['duration']} min)</td>
            </tr>"""
        else:  # It's a flight leg
            html += f"""
            <tr class="flight-leg">
                <td data-label="From"><b>{leg['departure_airport']}</b><br><small>{leg['departure_time']}</small></td>
                <td data-label="To"><b>{leg['arrival_airport']}</b><br><small>{leg['arrival_time']}</small></td>
                <td data-label="Details"><small>{leg['airline']}, {leg['duration']} min</small></td>
            </tr>"""
    return html


def generate_html_summary(flight_data_per_destination):
    print("Generating final responsive HTML design...")

    # --- NEW: Modern, Minimal, and Responsive CSS ---
    html_style = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f7f6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2 {
            color: #2c3e50;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
            margin-top: 40px;
        }
        .flight-option {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 25px;
            overflow: hidden; /* Important for border-radius */
        }
        .price-header {
            background-color: #3498db;
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .price-value {
            font-size: 24px;
            font-weight: bold;
        }
        .duration-value {
            font-size: 14px;
            opacity: 0.9;
        }
        .journey-details {
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            text-align: left;
            padding: 15px 20px;
            border-bottom: 1px solid #eef2f5;
        }
        thead {
            background-color: #f9fafb;
            color: #555;
            font-size: 12px;
            text-transform: uppercase;
        }
        .journey-header td {
            background-color: #e9ecef;
            font-weight: bold;
            color: #495057;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .layover-leg td {
            background-color: #fef9e7;
            text-align: center;
            font-style: italic;
            color: #7d6608;
        }

        /* --- RESPONSIVE DESIGN FOR PHONES --- */
        @media (max-width: 768px) {
            body { padding: 10px; }
            h1 { font-size: 24px; }
            h2 { font-size: 20px; }

            thead { display: none; } /* Hide table headers on mobile */

            tr {
                display: block;
                border-bottom: 2px solid #3498db;
                margin-bottom: 15px;
            }
            tr:last-child {
                border-bottom: none;
                margin-bottom: 0;
            }
            .journey-header tr, .layover-leg tr {
                border-bottom: 1px solid #eef2f5;
            }

            td {
                display: block;
                text-align: right !important; /* Force alignment */
                padding: 10px;
                position: relative;
            }
            td:before {
                content: attr(data-label); /* Use data-label for context */
                position: absolute;
                left: 10px;
                font-weight: bold;
                text-align: left;
                white-space: nowrap;
            }
        }
    </style>
    """

    html_body = f"""
    <div class="container">
        <h1>Weekly Flight Deals</h1>
        <p>Report generated on: {datetime.now().strftime('%Y-%m-%d')}</p>
    """

    for destination_code, flight_list in flight_data_per_destination.items():
        html_body += f"<h2>Flights: {CONFIG.DEPARTURE_ID} ➡️ {destination_code}</h2>"

        if not flight_list:
            html_body += "<p>No flights found for this destination.</p>"
            continue

        for flight in flight_list:
            outbound_legs = flight.get('outbound_legs', [])
            return_legs = flight.get('return_legs', [])

            # --- Main Card for each flight option ---
            html_body += f"""
            <div class="flight-option">
                <div class="price-header">
                    <span class="price-value">${flight['price']}</span>
                    <span class="duration-value">Total: {flight['total_duration']} min</span>
                </div>
                <div class="journey-details">
                    <table>
            """

            # --- Outbound Journey ---
            html_body += """
                        <tbody>
                            <tr class="journey-header"><td colspan="3">✈️ Outbound Journey</td></tr>
            """
            html_body += _generate_leg_rows_html(outbound_legs)

            # --- Return Journey (conditional) ---
            if return_legs:
                html_body += """
                            <tr class="journey-header"><td colspan="3">✈️ Return Journey</td></tr>
                """
                html_body += _generate_leg_rows_html(return_legs)

            html_body += "</tbody></table></div></div>"

    html_body += "</div>"  # Close container
    full_html = f"<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Flight Summary</title>{html_style}</head><body>{html_body}</body></html>"
    return full_html
