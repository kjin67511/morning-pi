from run import run
import time
import lcd
from config import ConfigSectionMap

interval = int(ConfigSectionMap("run")['interval'])
duration = int(ConfigSectionMap("run")['duration'])

timers = []
start_time = time.time()
elapsed_time = 0


def timer_list():
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


def start_timer():
    """
    initialize time variables and timer_list to run within the main loop
    """
    global start_time
    global elapsed_time
    global timers
    timers = timer_list()
    start_time = time.time()
    elapsed_time = 0


if __name__ == "__main__":
    print("start")

    run()

    if lcd.lcd is not None:
        try:
            while True:
                elapsed_time = time.time() - start_time

                if lcd.GPIO_input():
                    start_timer()

                if len(timers) > 0 and int(elapsed_time) == timers[0]:
                    timers.pop(0)

                    if len(timers) == 0:
                        lcd.clear()
                    else:
                        run()

                time.sleep(0.01)
        except KeyboardInterrupt:
            lcd.clear()

