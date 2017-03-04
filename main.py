from run import run
import datetime
from utils.timer import int_time, timer_list
import time
import lcd
from config import ConfigSectionMap

interval = int(ConfigSectionMap("run")['interval'])
duration = int(ConfigSectionMap("run")['duration'])
schedule_time = ConfigSectionMap("schedule")['time']

timers = []
start_time = int_time()
elapsed_time = 0
schedule_toggle = False


def check_schedule(time_str):
    global schedule_toggle

    if schedule_toggle is True:
        return False

    scheduled_time = time.strptime(time_str, "%H:%M")
    current_time = datetime.datetime.now()

    if scheduled_time.tm_hour == current_time.hour and scheduled_time.tm_min == current_time.minute:
        return True
    else:
        return False


def start_timer():
    """
    initialize time variables and timer_list to run within the main loop
    """
    global start_time
    global elapsed_time
    global timers
    timers = timer_list(duration, interval)
    start_time = int_time()
    elapsed_time = 0


if __name__ == "__main__":
    print("start")

    start_timer()

    if lcd.lcd is not None:
        try:
            while True:
                elapsed_time = int_time() - start_time

                if lcd.GPIO_input() or check_schedule(schedule_time):
                    schedule_toggle = True
                    start_timer()

                if len(timers) > 0 and int(elapsed_time) == timers[0]:
                    timers.pop(0)

                    if len(timers) == 0:  # end of timer
                        schedule_toggle = False
                        lcd.clear()
                    else:
                        run()

                time.sleep(0.01)
        except KeyboardInterrupt:
            lcd.clear()
    else:  # test purpose in non-rpi
        run()
