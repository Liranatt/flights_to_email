# In a new file named ranking.py

def rank_and_filter_flights(flights, max_results=5):
    """
    Ranks flights based on a weighted score of price, duration, and connections,
    and returns the top results.
    """
    if not flights:
        return []

    # Use a large number to sort flights with 'N/A' price/duration to the end
    inf_value = float('inf')

    # Sort a copy of the list by price to get price ranks
    flights_sorted_by_price = sorted(
        flights,
        key=lambda f: f.get('price') if isinstance(f.get('price'), int) else inf_value
    )

    # Sort a copy of the list by duration to get duration ranks
    flights_sorted_by_duration = sorted(
        flights,
        key=lambda f: f.get('total_duration') if isinstance(f.get('total_duration'), int) else inf_value
    )

    # Calculate a final score for each flight
    for flight in flights:
        # Get price rank (index + 1 in the sorted list)
        price_rank = flights_sorted_by_price.index(flight) + 1

        # Get duration rank
        duration_rank = flights_sorted_by_duration.index(flight) + 1

        # Calculate the connection multiplier (lower is better)
        num_connections = flight.get('num_connections', 0)
        connection_multiplier = 0.95
        if num_connections > 0:
            connection_multiplier = 0.95 + (0.05 * num_connections)

        # Calculate final score (lower is better)
        flight['score'] = (price_rank + duration_rank) * connection_multiplier

    # Sort all flights by their new final score
    ranked_flights = sorted(flights, key=lambda f: f['score'])

    # Return the top 5 (or fewer)
    return ranked_flights[:max_results]