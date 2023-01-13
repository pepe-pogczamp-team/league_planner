from rest_framework import status
from rest_framework.response import Response

from league_planner import settings

from datetime import datetime, timedelta

import requests


class WeatherAPIClient:
    weather_api_base_url = "https://api.weatherapi.com/v1/"
    weather_api_secret_key = settings.WEATHER_API_SECRET_KEY

    def check_if_weather_good(self, city: str, date: "datetime") -> bool:
        current_datetime = datetime.now()
        if current_datetime >= date:
            return True
        elif current_datetime + timedelta(days=14) <= date:
            response = self.check_future(city, date)
        else:
            delta = date - current_datetime
            response = self.check_forecast(city, delta.days)

        return self.check_response(response)

    def check_future(self, city: str, date: "datetime") -> "Response":
        return requests.get(
            f"{self.weather_api_base_url}future.json",
            params={
                "key": self.weather_api_secret_key,
                "q": city,
                "dt": date.strftime(settings.WEATHER_API_DATE_FORMAT)
            },
        )

    def check_forecast(self, city: str, delta_days: int) -> "Response":
        return requests.get(
            f"{self.weather_api_base_url}forecast.json",
            params={
                "key": self.weather_api_secret_key,
                "q": city,
                "days": delta_days,
            },
        )

    @staticmethod
    def check_response(response: "Response") -> bool:
        if response.status_code != status.HTTP_200_OK:
            return True
        data_json = response.json()
        return not bool(data_json["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"])
