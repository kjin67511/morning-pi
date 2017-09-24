from config import ConfigSectionMap
input_pin = int(ConfigSectionMap("gpio")['input_pin'])

rs = int(ConfigSectionMap("lcd")['rs'])
en = int(ConfigSectionMap("lcd")['en'])
d4 = int(ConfigSectionMap("lcd")['d4'])
d5 = int(ConfigSectionMap("lcd")['d5'])
d6 = int(ConfigSectionMap("lcd")['d6'])
d7 = int(ConfigSectionMap("lcd")['d7'])

try:
    import Adafruit_CharLCD as LCD
    import RPi.GPIO as GPIO
except ImportError:
    lcd = None
else:
    lcd = LCD.Adafruit_CharLCD(rs, en, d4, d5, d6, d7, 16, 2)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def GPIO_input():
    if lcd is not None:
        return GPIO.input(input_pin)
    else:
        return False


def message(msg):
    if lcd is not None:
        lcd.message(msg)
    else:
        print(msg)


def clear():
    if lcd is not None:
        lcd.clear()
