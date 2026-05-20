def calculate_profit(distance, demand, ticket_price):
    fuel_cost_per_km = 6
    operational_cost = 20000

    fuel_cost = distance * fuel_cost_per_km
    revenue = demand * ticket_price

    profit = revenue - (fuel_cost + operational_cost)
    return profit