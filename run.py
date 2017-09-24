from bus.bus_request import bus_request
from bus.bus_view import arrivals_from_xml, bus_arrival_view
from weather.weather_request import live_weather_request, forecast_weather_request
from weather.weather_view import weather_live_from_json, weather_forecast_from_json, weather_view
from dust.dust_request import dust_request
from dust.dust_view import dust_from_xml, dust_view
import grequests
import datetime
from xml.etree import ElementTree
import lcd


from config import ConfigSectionMap
led_pin = int(ConfigSectionMap("dust")['led_pin'])
pm10_threshold = int(ConfigSectionMap("dust")['pm10_threshold'])
pm25_threshold = int(ConfigSectionMap("dust")['pm25_threshold'])

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    led = True
    GPIO.setup(led_pin, GPIO.OUT)
except ImportError:
    led = False


def run():
    lcd.clear()
    lcd.message("Loading...")

    weather_live_req = live_weather_request()
    weather_forecast_req = forecast_weather_request()
    bus_arrival_req = bus_request()
    dust_req = dust_request()

    grequests.map(
        (weather_live_req, weather_forecast_req, bus_arrival_req, dust_req)
    )

    weathers = list()
    if weather_live_req.response is not None:
        weathers.append(weather_live_from_json(weather_live_req.response.json()))
    else:
        weathers.append(None)

    if weather_forecast_req.response is not None:
        weathers.append(weather_forecast_from_json(weather_forecast_req.response.json(),
                                                   datetime.datetime.now() + datetime.timedelta(hours=12)))
    else:
        weathers.append(None)

    weather_str = weather_view(weathers)

    arrivals = arrivals_from_xml(ElementTree.fromstring(bus_arrival_req.response.content))
    bus_str = bus_arrival_view(arrivals)

    dusts = dust_from_xml(ElementTree.fromstring(dust_req.response.content))
    dust_str = dust_view(dusts)

    lcd_str = bus_str + "\n" + weather_str + " " + dust_str
    lcd.clear()
    lcd.message(lcd_str)

    GPIO.output(led_pin, GPIO.LOW)

    if dusts[0] != '-' and int(dusts[0]) > pm10_threshold:
        GPIO.output(led_pin, GPIO.HIGH)

    if dusts[1] != '-' and int(dusts[1]) > pm25_threshold:
        GPIO.output(led_pin, GPIO.HIGH)

