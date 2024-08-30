import requests


def get_annual_weather_data(lat, lon, year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&daily=apparent_temperature_max,precipitation_sum"
    )

    response = requests.get(url)
    data = response.json()

    temperatures = data['daily']['apparent_temperature_max']
    precipitation = data['daily']['precipitation_sum']

    annual_max_temperature = max(temperatures)
    annual_total_precipitation = sum(precipitation)


    return annual_max_temperature, annual_total_precipitation