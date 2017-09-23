try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


def create_dust_qs(serviceKey, station_name):
    qs = dict()
    qs['serviceKey'] = unquote(serviceKey)
    qs['stationName'] = station_name
    qs['dataTerm'] = 'DAILY'
    qs['ver']='1.3'
    return qs
