from machine import Pin
import time
from dicc import *
from IC7404.ic7404_pin import *

'''
      NOT GATE
     In     Out
    -----------
      0     1
      1     0
    -----------
'''

def metadata():
    ic_pin_count  = IC_14_PIN
    ic_brief_name = "NOT Gate IC"

    return ic_pin_count, ic_brief_name


def test_run(index, input, output):
    errand = 0

    input.value(LOW)
    if output.value() != HIGH:
        errand += 1

    input.value(HIGH)
    if output.value() != LOW:
        errand += 1

    if errand == 0:
        print("NOT gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("NOT gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    not1_out = Pin(PIN_NOT1_OUT, Pin.IN, Pin.PULL_DOWN)
    not2_out = Pin(PIN_NOT2_OUT, Pin.IN, Pin.PULL_DOWN)
    not3_out = Pin(PIN_NOT3_OUT, Pin.IN, Pin.PULL_DOWN)
    not4_out = Pin(PIN_NOT4_OUT, Pin.IN, Pin.PULL_DOWN)
    not5_out = Pin(PIN_NOT5_OUT, Pin.IN, Pin.PULL_DOWN)
    not6_out = Pin(PIN_NOT6_OUT, Pin.IN, Pin.PULL_DOWN)

    not1_in = Pin(PIN_NOT1_IN, Pin.OUT)
    not2_in = Pin(PIN_NOT2_IN, Pin.OUT)
    not3_in = Pin(PIN_NOT3_IN, Pin.OUT)
    not4_in = Pin(PIN_NOT4_IN, Pin.OUT)
    not5_in = Pin(PIN_NOT5_IN, Pin.OUT)
    not6_in = Pin(PIN_NOT6_IN, Pin.OUT)


    print("4 NOT IC 7404 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, not1_in, not1_out)
    time.sleep(0.5)
    exit_val += test_run(2, not2_in, not2_out)
    time.sleep(0.5)
    exit_val += test_run(3, not3_in, not3_out)
    time.sleep(0.5)
    exit_val += test_run(4, not4_in, not4_out)
    time.sleep(0.5)
    exit_val += test_run(5, not5_in, not5_out)
    time.sleep(0.5)
    exit_val += test_run(6, not6_in, not6_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
