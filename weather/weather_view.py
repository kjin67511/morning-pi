# -*- coding: utf-8 -*-
import datetime


def python_unichr(chr_code):
    """
    compatible function for chr(python 3.x) and unichr(python 2.x)
    """
    try:
        from builtins import chr
    except ImportError:
        return unichr(chr_code)  # python 2.x
    else:
        return chr(chr_code)  # python 3.x


def convert_sky_code(sky_code):
    """
    Convert sky code into the following code, handling only sunny and cloudy

    SKY Code: refer to weather station API document
        1: sunny,
        2: partly cloudy,
        3: mostly cloudy
        4: cloudy

    2,3,4 mapped to 2

    Weather Code: Own implementation
        1: sunny
        2: rainy (not handled by this function)
        3: cloudy
        4: snowy (not handled by this function)

    :param sky_code: SKY code from open API
    :return: weather code
    """

    weather_code = 0

    if sky_code == 1:
        weather_code = 1
    elif sky_code == 2 or sky_code == 3 or sky_code == 4:
        weather_code = 3

    return weather_code


def convert_rain_code(rain_code):
    """
    Convert rain code into the following code

    SKY Code: refer to weather station API document
        0: No rain
        1: Rainy
        2: Rainy and Snowy
        3: Snowy

    Weather Code: Own implementation
        1: sunny (not handled by this function)
        2: rainy
        3: cloudy (not handled by this function)
        4: snowy

    :param rain_code: PTY(rain) code from open API
    :return: weather code
    """

    weather_code = 0  # error

    if rain_code == 1 or rain_code == 2:
        weather_code = 2
    elif rain_code == 3:
        weather_code = 4

    return weather_code


def translate_weather_code(weather_code):
    """
    translate weather code into a character
    """
    if weather_code == 1:
        return 'S'  # Sunny
    elif weather_code == 2:
        return 'R'  # Rainy
    elif weather_code == 3:
        return 'L'  # Cloudy
    elif weather_code == 4:
        return 'W'  # Snowy
    else:
        return '-'  # error


def weather_forecast_from_json(json, time):
    """
    parse forecast response(json) to return weather object

    :param json: json object in response
    :param time: forecast 'time' later (hour)
    :return: list(
                temperature,  # rounded celsius in integer
                weather_code, # S/R/L/W/-
                probability,  # of snow or rain in integer xx
             )
    """
    temperature = 0
    rain_code = 0
    sky_code = 0
    probability = 0

    lowest_delta_sec = datetime.timedelta(days=1).total_seconds()
    nearest_fcstTime_str = None

    try:

        # Of forecast list elements, find the item with nearest time to "time" argument
        #
        # Given forecast list consists of (9 am, 12 am, 3 pm, 5 pm, 9 pm) and
        # if "time" argument is 12 (hours) and current time is 8 am
        # 9pm forecast will be acquired (nearest item from 8am + 12hours)
        for item in json['response']['body']['items']['item']:
            time_str = str(item['fcstDate']) + str(item['fcstTime'])
            t = datetime.datetime.strptime(time_str, '%Y%m%d%H%M')
            delta_sec = abs((time - t).total_seconds())

            if delta_sec < lowest_delta_sec:
                lowest_delta_sec = delta_sec
                nearest_fcstTime_str = time_str

        # parse forecast item
        for item in json['response']['body']['items']['item']:
            time_str = str(item['fcstDate']) + str(item['fcstTime'])

            if time_str == nearest_fcstTime_str:
                if item['category'] == 'T3H':
                    temperature = item['fcstValue']
                elif item['category'] == 'PTY' and item['fcstValue'] != 0:
                    rain_code = item['fcstValue']
                elif item['category'] == 'POP' and item['fcstValue'] != 0:
                    probability = item['fcstValue']
                elif item['category'] == 'SKY':
                    sky_code = item['fcstValue']

        if rain_code != 0:  # rainy or snowy?
            weather_code = convert_rain_code(rain_code)
        else:  # sunny or cloudy
            weather_code = convert_sky_code(sky_code)

    except KeyError as e:
        weather_code = 0
        print("Key error", str(e))
    except TypeError as e:
        weather_code = 0
        print("Key error", str(e))
        
    return temperature, weather_code, probability,


def weather_live_from_json(json):
    """
    parse live weather response(json) to return weather object

    :param json: json object in response
    :return: list(
                temperature,  # rounded celsius in integer
                weather_code, # S/R/L/W/-
                probability,  # of snow or rain in integer xx
             )

    """

    temperature = 0
    rain_code = 0
    sky_code = 0
    probability = 0

    try:
        for item in json['response']['body']['items']['item']:
            if item['category'] == 'T1H':
                temperature = item['obsrValue']
            elif item['category'] == 'PTY' and item['obsrValue'] != 0:
                rain_code = item['obsrValue']
            elif item['category'] == 'SKY':
                sky_code = item['obsrValue']

        if rain_code != 0:  # rainy or snowy?
            weather_code = convert_rain_code(rain_code)
            probability = 99  # no probability for live weather, set 99%
        else:  # sunny or cloudy
            weather_code= convert_sky_code(sky_code)
    except KeyError as e:
        weather_code = 0
        print("Key error", str(e))
    except TypeError as e:
        weather_code = 0
        print("Key error", str(e))

    return temperature, weather_code, probability,


def weather_to_str(weather):
    """
    convert weather object into string

    :param weather: list(temperature,  # rounded celsius in integer
                         weather_code, # S/R/L/W/-
                         probability,  # of snow or rain in integer xx)
    :return: string "temp{Status}Probability|--" or "ERR"
    """

    if weather is None:
        return 'ERR'

    temperature = int(round(weather[0], 1))
    status = translate_weather_code(weather[1])

    if status == "R" or status == "W":
        probability = weather[2]
    else:
        probability = ""

    celsius_code = 223
    degree_sign = u'\N{DEGREE SIGN}'

    return u'{}{}{}{}'.format(temperature, python_unichr(celsius_code), status, probability)


def weather_view(weathers):
    """
    create weather view from weathers

    :param weathers: (weather, weather, weather...)
    :return: string "weather_str/weather_str/weather_str..."
    """

    view = ""

    for index, element in enumerate(weathers):
        if index != 0:
            view += '/'

        view += weather_to_str(element)

    return view
