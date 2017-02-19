from bus.bus_request import bus_request
from bus.bus_view import arrivals_from_xml, bus_arrival_view
from weather.weather_request import live_weather_request, forecast_weather_request
from weather.weather_view import weather_live_from_json, weather_forecast_from_json, weather_view
import grequests
import datetime
from xml.etree import ElementTree
import lcd


def run():
    lcd.clear()
    lcd.message("Loading...")

    weather_live_req = live_weather_request()
    weather_forecast_req = forecast_weather_request()
    bus_arrival_req = bus_request()

    grequests.map(
        (weather_live_req, weather_forecast_req, bus_arrival_req)
    )

    weathers = list()
    weathers.append(weather_live_from_json(weather_live_req.response.json()))
    weathers.append(weather_forecast_from_json(weather_forecast_req.response.json(),
                                               datetime.datetime.now() + datetime.timedelta(hours=12)))

    weather_str = weather_view(weathers)

    arrivals = arrivals_from_xml(ElementTree.fromstring(bus_arrival_req.response.content))
    bus_str = bus_arrival_view(arrivals)
    lcd_str = bus_str + "\n" + weather_str

    lcd.clear()
    lcd.message(lcd_str)
