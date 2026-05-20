from flask import Flask, render_template, request, jsonify
from src.data_loader import load_data
from src.route_optimizer import build_profit_function
from src.genetic_algorithm import run_ga
from src.haversine import haversine
from src.profit_calculator import calculate_profit

app = Flask(__name__)

airports, *_ = load_data()

@app.route('/')
def home():
    codes = airports['iata_code'].dropna().unique().tolist()
    airport_data = airports[['iata_code', 'latitude_deg', 'longitude_deg', 'name']].dropna().to_dict('records')
    # Create a list of airport options with name and code
    airport_options = []
    for _, row in airports[['iata_code', 'name']].dropna().drop_duplicates(subset=['iata_code']).iterrows():
        airport_options.append({
            'code': row['iata_code'],
            'name': row['name']
        })
    return render_template("index.html", codes=codes, airport_data=airport_data, airport_options=airport_options)

@app.route('/api/airports', methods=['GET'])
def get_airports():
    airport_data = airports[['iata_code', 'latitude_deg', 'longitude_deg', 'name']].dropna().to_dict('records')
    return jsonify(airport_data)

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    data = request.get_json()
    selected = data.get('airports', [])
    optimization = data.get('optimization', 'profit')
    
    if len(selected) < 2:
        return jsonify({'error': 'Select at least 2 airports'}), 400
    
    if optimization == 'profit':
        profit_func = build_profit_function(airports)
        best_route = run_ga(selected, profit_func)
    else:
        best_route = selected
    
    segments = []
    total_distance = 0
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    total_fuel = 0
    total_time = 0
    
    # Data for visualizations
    revenue_by_segment = {}
    fuel_by_segment = {}
    time_by_segment = {}
    demand_by_airport = {}
    
    for airport_code in best_route:
        demand_by_airport[airport_code] = 120
    
    for i in range(len(best_route) - 1):
        src_code = best_route[i]
        dst_code = best_route[i + 1]
        
        src = airports[airports['iata_code'] == src_code].iloc[0]
        dst = airports[airports['iata_code'] == dst_code].iloc[0]
        
        distance = haversine(src['latitude_deg'], src['longitude_deg'], 
                           dst['latitude_deg'], dst['longitude_deg'])
        
        demand = 120
        ticket_price = 5000
        revenue = demand * ticket_price
        fuel_cost = distance * 6
        operational_cost = 20000
        cost = fuel_cost + operational_cost
        profit = calculate_profit(distance, demand, ticket_price)
        
        # Calculate travel time (assuming avg speed 900 km/h for commercial aircraft)
        travel_time = round(distance / 900 * 60, 2)  # in minutes
        
        total_distance += distance
        total_revenue += revenue
        total_cost += cost
        total_profit += profit
        total_fuel += fuel_cost
        total_time += travel_time
        
        segment_name = f"{src_code} → {dst_code}"
        revenue_by_segment[segment_name] = round(revenue, 2)
        fuel_by_segment[segment_name] = round(fuel_cost, 2)
        time_by_segment[segment_name] = round(travel_time, 2)
        
        segments.append({
            'from': src_code,
            'to': dst_code,
            'distance': round(distance, 2),
            'passengers': demand,
            'revenue': round(revenue, 2),
            'cost': round(cost, 2),
            'profit': round(profit, 2),
            'fuel': round(fuel_cost, 2),
            'time': round(travel_time, 2)
        })
    
    return jsonify({
        'route': best_route,
        'segments': segments,
        'totals': {
            'distance': round(total_distance, 2),
            'passengers': len(best_route) * 120,
            'revenue': round(total_revenue, 2),
            'cost': round(total_cost, 2),
            'profit': round(total_profit, 2),
            'fuel': round(total_fuel, 2),
            'time': round(total_time, 2)
        },
        'charts': {
            'revenue_by_segment': revenue_by_segment,
            'fuel_by_segment': fuel_by_segment,
            'time_by_segment': time_by_segment,
            'demand_by_airport': demand_by_airport
        }
    })

if __name__ == "__main__":
    app.run(debug=True)