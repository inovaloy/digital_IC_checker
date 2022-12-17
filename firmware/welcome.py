from machine import Pin
import json
import time

from dicc import *
import dicc_pin

led_list = []

def txt_padding(txt, center, l_offset):
    txt_len = len(str(txt))
    space = 60 - txt_len - 4
    if center:
        l_space = space//2
        r_space = space - l_space
        return "##" + " "*l_space + str(txt) + " "*r_space + "##"
    else:
        r_space = space - l_offset
        return "##" + " "*l_offset + str(txt) + " "*r_space + "##"


def print_intro():
    with open("config.json", 'r') as file:
        json_data = json.loads(file.read())

    version = json_data["version"]
    flash_time = json_data["build_time"]
    print("\n\n\n")
    print("#"*60)
    print(txt_padding("Digital IC Checker v"+version, True, 0))
    print(txt_padding("A project by team Inovaloy", True, 0))
    print(txt_padding("Last update time: "+flash_time, True, 0))
    print("#"*60)



def red_led_initialte():
    global led_list
    led_list.append(Pin(dicc_pin.LED1, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED2, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED3, Pin.OUT))
    led_list.append(Pin(dicc_pin.LED4, Pin.OUT))


def welcome_led_static():
    global led_list

    if led_list == []:
        red_led_initialte()

    for led in led_list:
        led.value(HIGH)
    time.sleep(0.1)


def welcome_led_blink():
    global led_list

    if led_list == []:
        red_led_initialte()

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
