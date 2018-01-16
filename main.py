import datetime
import time

from config import ConfigSectionMap
from run import run, reset, button_pushed, lcd_ready
from utils.timer import int_time, timer_list

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

    if lcd_ready():
        try:
            while True:
                elapsed_time = int_time() - start_time

                if button_pushed() or check_schedule(schedule_time):
                    schedule_toggle = True
                    start_timer()

                if len(timers) > 0 and int(elapsed_time) == timers[0]:
                    timers.pop(0)

                    if len(timers) == 0:  # end of timer
                        schedule_toggle = False
                        reset()
                    else:
                        run()

                time.sleep(0.01)
        except KeyboardInterrupt:
            reset()
    else:  # test purpose in non-rpi
        run()
