from src.data_loader import load_data
from src.route_optimizer import build_profit_function
from src.genetic_algorithm import run_ga

def main():
    airports, flights, revenue, weather, aircraft = load_data()

    # pick sample airports
    nodes = airports['iata_code'].dropna().unique().tolist()[:6]

    profit_func = build_profit_function(airports)

    best_route = run_ga(nodes, profit_func)

    print("\n🔥 BEST ROUTE FOUND:")
    print(" -> ".join(best_route))
    print("💰 Profit:", profit_func(best_route))


if __name__ == "__main__":
    main()