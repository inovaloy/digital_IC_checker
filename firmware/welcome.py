from machine import Pin
import json
import time

from dicc import *
import dicc_pin

def print_intro():
    with open("config.json", 'r') as file:
        json_data = json.loads(file.read())

    version = json_data["version"]
    print("\n\n\n")
    print("#"*47)
    print("\tDigital IC Checker v"+version)
    print("#"*47)



def welcome_led_blink():
    led_list = []
    led_list.append(Pin(dicc_pin.LED1, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED2, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED3, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED4, Pin.OUT))

    for led in led_list:
        led.value(HIGH)
    time.sleep(2)

    for _ in range(5):
        led_list[0].value(HIGH)
        led_list[1].value(LOW)
        led_list[2].value(LOW)
        led_list[3].value(LOW)
        time.sleep(0.1)

        led_list[0].value(LOW)
        led_list[1].value(HIGH)
        led_list[2].value(LOW)
        led_list[3].value(LOW)
        time.sleep(0.1)

        led_list[0].value(LOW)
        led_list[1].value(LOW)
        led_list[2].value(HIGH)
        led_list[3].value(LOW)
        time.sleep(0.1)

        led_list[0].value(LOW)
        led_list[1].value(LOW)
        led_list[2].value(LOW)
        led_list[3].value(HIGH)
        time.sleep(0.1)

    for led in led_list:
        led.value(LOW)


def blink_status_led(status):
    green_status_led = Pin(dicc_pin.DUAL_LED_GREEN, Pin.OUT)
    red_status_led = Pin(dicc_pin.DUAL_LED_RED, Pin.OUT)

    green_status_led.value(LOW)
    red_status_led.value(LOW)

    if status == RETURN_SUCCESS:
        for _ in range(5):
            green_status_led.value(HIGH)
            time.sleep(0.2)
            green_status_led.value(LOW)
            time.sleep(0.2)

    if status == RETURN_ERROR:
        for _ in range(5):
            red_status_led.value(HIGH)
            time.sleep(0.2)
            red_status_led.value(LOW)
            time.sleep(0.2)
