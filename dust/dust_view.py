# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import xml.etree.ElementTree
from config import ConfigSectionMap

def dust_from_xml(root):
    """
    get arrivals from xml which contains arrival items (n different routes) for specified bus station
    :param root: root node of xml response
    :return: arrival list (this, next)
    """

    try:
        # find matching route
        pm25 = None
        pm10 = None
        body = root[1] # <body>
        if int(body.find('totalCount').text) > 0:
            item = body.find('items')[0]
            pm10 = item.find('pm10Value').text
            pm25 = item.find('pm25Value').text

    except xml.etree.ElementTree.ParseError as e:
        print("XML error", str(e))
        print(xml.etree.ElementTree.tostring(root))

    return (pm10, pm25)


def dust_view(dusts):
    """
    create bus arrival view from arrivals

    :param arrivals: (arrival, arrival, arrival...)
    :return: string "arrival_str/arrival_str/arrival_str..."
    """

    view = ""

    for index, element in enumerate(dusts):
        if index != 0:
            view += '/'

        view += str(element)

    return view
