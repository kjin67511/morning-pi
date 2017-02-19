from utils.url import make_url
from config import ConfigSectionMap
from weather.weather_query import create_weather_live_qs, create_weather_forecast_qs
import grequests
import datetime

forecast_api_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
live_api_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'

nx = int(ConfigSectionMap("weather")['nx'])
ny = int(ConfigSectionMap("weather")['ny'])

live_basetime_delta = int(ConfigSectionMap("weather_basetime_delta")['live'])
forecast_basetime_delta = int(ConfigSectionMap("weather_basetime_delta")['forecast'])

key = ConfigSectionMap("api_key")['weather']
now = datetime.datetime.now()


def live_weather_request():
    qs = create_weather_live_qs(key, nx, ny, now, live_basetime_delta)
    return grequests.get(make_url(live_api_url, qs))


def forecast_weather_request():
    qs = create_weather_forecast_qs(key, nx, ny, now, forecast_basetime_delta)
    return grequests.get(make_url(forecast_api_url, qs))
