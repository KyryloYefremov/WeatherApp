import requests


class WeatherApi:
    """
    Class to interact with the weatherapi.com API.
    """
    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__url = 'https://api.weatherapi.com/'
        self.__sunny_codes = {
            "Sunny": 1000
        }
        self.__rain_codes = {
            "Patchy rain possible": 1063, "Thundery outbreaks possible": 1087, "Blizzard": 1117,
            "Patchy light drizzle": 1150, "Light drizzle": 1153, "Freezing drizzle": 1168,
            "Heavy freezing drizzle": 1171, "Patchy light rain": 1180, "Light rain": 1183,
            "Moderate rain at times": 1186, "Moderate rain": 1189, "Heavy rain at times": 1192,
            "Heavy rain": 1195, "Light freezing rain": 1198, "Moderate or heavy freezing rain": 1201,
            "Light rain shower": 1240, "Moderate or heavy rain shower": 1243, "Torrential rain shower": 1246,
            "Light sleet showers": 1249, "Moderate or heavy sleet showers": 1252, "Light showers of ice pellets": 1261,
            "Moderate or heavy showers of ice pellets": 1264, "Patchy light rain with thunder": 1273,
            "Moderate or heavy rain with thunder": 1276
        }
        self.__cloudy_codes = {
            "Cloudy": 1006, "Overcast": 1009, "Mist": 1030, "Fog": 1135, "Freezing fog": 1147,
        }
        self.__partly_cloudy_codes = {
            "Partly cloudy": 1003,
        }
        self.__snowy_codes = {
            "Patchy snow possible": 1066, "Patchy sleet possible": 1069, "Patchy freezing drizzle possible": 1072,
            "Blowing snow": 1114, "Light sleet": 1204, "Moderate or heavy sleet": 1207, "Patchy light snow": 1210,
            "Light snow": 1213, "Patchy moderate snow": 1216, "Moderate snow": 1219, "Patchy heavy snow": 1222,
            "Heavy snow": 1225, "Ice pellets": 1237, "Light snow showers": 1255, "Moderate or heavy snow showers": 1258,
            "Moderate or heavy snow with thunder": 1282,  "Patchy light snow with thunder": 1279
        }


    def get_today_forecast(self, city: str) -> dict:
        """
        Get today's forecast for the specified city.
        :param city: City name.
        :return: Dictionary with forecast data.
        """

        url = f'{self.__url}v1/forecast.json?key={self.__api_key}&q={city}&days=1&aqi=no&alerts=no'
        response = requests.get(url)
        data = response.json()

        # Convert api data to {time: degrees} view.
        hourly_forecast = []
        for hour in data['forecast']['forecastday'][0]['hour']:
            hourly_forecast.append({hour['time'][-5:]: round(hour['temp_c'])})

        img_src = "images/"
        forecast_code = data['forecast']['forecastday'][0]['day']['condition']['code']
        if forecast_code in self.__sunny_codes.values():
            img_src += "icon-sun.png"
        elif forecast_code in self.__partly_cloudy_codes.values():
            img_src += "icon-clouds-sun.png"
        elif forecast_code in self.__cloudy_codes.values():
            img_src += "icon-clouds.png"
        elif forecast_code in self.__snowy_codes.values():
            img_src += "icon-snow.png"
        elif forecast_code in self.__rain_codes.values():
            img_src += "icon-rain.png"
        else:
            img_src += "default.png"

        result = {
            'date': data['forecast']['forecastday'][0]['date'],
            'condition': data['forecast']['forecastday'][0]['day']['condition']['text'],
            'icon_src': img_src,
            'maxtemp': data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'mintemp': data['forecast']['forecastday'][0]['day']['mintemp_c'],
            'daily_chance_of_rain': data['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
            'hourly': hourly_forecast
        }
        return result
