try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


def create_bus_qs(serviceKey, station_id):
    qs = dict()
    qs['serviceKey'] = unquote(serviceKey)
    qs['arsId'] = station_id
    return qs
