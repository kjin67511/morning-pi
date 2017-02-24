import datetime

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


def base_date_time(t):
    base_date = t.strftime('%Y%m%d')
    base_time = t.strftime('%H00')
    return base_date, base_time


def get_basehour_for_forecast(current_hour):
    base_hours_for_forecast = (2, 5, 8, 11, 14, 17, 20, 23)
    base_hour = -1

    if current_hour < 2 or current_hour >= 23:
        base_hour = 23
    else:
        for h in reversed(base_hours_for_forecast):
            if current_hour >= h:
                base_hour = h
                break

    return base_hour


def get_basehour_offset_for_forecast(current_hour):
    """
    0  -> -1 (-> 23)
    1  -> -2 (-> 23)
    2  ->  0 (-> 2 )
    3  -> -1 (-> 2 )
    4  -> -2 (-> 2 )
    5  ->  0 (-> 5 )
    6  -> -1 (-> 5 )
    7  -> -2 (-> 5 )
    8  ->  0 (-> 8 )
    9  -> -1 (-> 8 )
    10 -> -2 (-> 8 )
    11 ->  0 (-> 11)
    12 -> -1 (-> 11)
    13 -> -2 (-> 11)
    14 ->  0 (-> 14)
    15 -> -1 (-> 14)
    16 -> -2 (-> 14)
    17 ->  0 (-> 17)
    18 -> -1 (-> 17)
    19 -> -2 (-> 17)
    20 ->  0 (-> 20)
    21 -> -1 (-> 20)
    22 -> -2 (-> 20)
    23 ->  0 (-> 23)
    :param current_hour:
    :return:
    """

    base_hours_for_forecast = (2, 5, 8, 11, 14, 17, 20, 23)
    offset_hours = 0

    if current_hour < 2:
        offset_hours = -(current_hour + 1)
    else:
        for h in reversed(base_hours_for_forecast):
            if current_hour >= h:
                offset_hours = h - current_hour
                break

    return offset_hours


def create_weather_qs(serviceKey, nx, ny, base_date, base_time):
    qs = dict()
    qs['serviceKey'] = unquote(serviceKey)
    qs['nx'] = nx
    qs['ny'] = ny
    base_date = base_date
    base_time = base_time
    qs['base_date'] = base_date
    qs['base_time'] = base_time
    qs['_type'] = 'json'
    qs['numOfRows'] = 100
    return qs


def create_weather_live_qs(serviceKey, nx, ny, now, basetime_delta):
    base = now + datetime.timedelta(minutes=basetime_delta)
    base_date, base_time = base_date_time(base)
    return create_weather_qs(serviceKey, nx, ny, base_date, base_time)


def create_weather_forecast_qs(serviceKey, nx, ny, now, basetime_delta):
    # delta
    base_hour = now + datetime.timedelta(minutes=basetime_delta)

    offset_hour = get_basehour_offset_for_forecast(base_hour.hour)
    base = base_hour + datetime.timedelta(hours=offset_hour)

    base_date, base_time = base_date_time(base)
    return create_weather_qs(serviceKey, nx, ny, base_date, base_time)
