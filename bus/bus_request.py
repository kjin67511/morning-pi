from bus.bus_query import create_bus_qs
from utils.url import make_url
import grequests
from config import ConfigSectionMap

arrival_api_url = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid'
key = ConfigSectionMap("api_key")['bus']
station_id = ConfigSectionMap("bus")['station_id']


def bus_grequests(url, key, station_id):
    bus_qs = create_bus_qs(key, station_id)
    return grequests.get(make_url(url, bus_qs))


def bus_request():
    return bus_grequests(arrival_api_url, key, station_id)
