def weather_factor(weather_row):
    factor = 1.0

    if 'Storm' in str(weather_row).lower():
        factor += 0.3
    elif 'Rain' in str(weather_row).lower():
        factor += 0.15

    return factor