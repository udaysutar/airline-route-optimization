from src.haversine import haversine
from src.profit_calculator import calculate_profit

def build_profit_function(airports_df):

    def profit(route):
        total_profit = 0

        for i in range(len(route)-1):
            src = airports_df[airports_df['iata_code'] == route[i]].iloc[0]
            dst = airports_df[airports_df['iata_code'] == route[i+1]].iloc[0]

            distance = haversine(
                src['latitude_deg'], src['longitude_deg'],
                dst['latitude_deg'], dst['longitude_deg']
            )

            demand = 120
            ticket_price = 5000

            total_profit += calculate_profit(distance, demand, ticket_price)

        return total_profit

    return profit