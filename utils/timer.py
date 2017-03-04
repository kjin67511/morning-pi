import time


def int_time():
    return int(time.time())


def timer_list(duration, interval):
    """
    reset timer list
    main loop will check timer list and pop the head item to consume
    :return: list consists of second (0, 30, 60, ... 1800)
    """
    count = int(duration / interval)

    l = []
    for c in range(count + 1):
        l.append(c * interval)

    return l
