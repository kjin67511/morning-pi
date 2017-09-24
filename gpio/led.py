from config import ConfigSectionMap

led_pin = int(ConfigSectionMap("dust")['led_pin'])

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    led = True
    GPIO.setup(led_pin, GPIO.OUT)
except ImportError:
    led = False


def on():
    if led is True:
        GPIO.output(led_pin, GPIO.HIGH)


def off():
    if led is True:
        GPIO.output(led_pin, GPIO.LOW)
