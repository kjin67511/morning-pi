from dust.dust_query import create_dust_qs
from utils.url import make_url

import grequests
from config import ConfigSectionMap

dust_api_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
key = ConfigSectionMap("api_key")['dust']
station_name = ConfigSectionMap("dust")['station_name']


def dust_grequests(url, key, station_id):
    dust_qs = create_dust_qs(key, station_id)
    return grequests.get(make_url(url, dust_qs))

 
def dust_request():
    return dust_grequests(dust_api_url, key, station_name)
