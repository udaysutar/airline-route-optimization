import pandas as pd

def load_data():
    airports = pd.read_csv("data/India_Airports_dataset (1).csv")
    flights = None  # Flight Data.xlsx file not available
    revenue = pd.read_csv("data/revenue_dataset (1).csv")
    weather = pd.read_csv("data/weather_dataset (1).csv")
    aircraft = pd.read_csv("data/aircraft_types.csv")

    return airports, flights, revenue, weather, aircraft