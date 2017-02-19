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
    h1 = now + datetime.timedelta(minutes=basetime_delta)

    # base hour
    base = h1.replace(hour=get_basehour_for_forecast(h1.hour))
    base_date, base_time = base_date_time(base)
    return create_weather_qs(serviceKey, nx, ny, base_date, base_time)
