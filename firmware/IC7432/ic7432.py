from machine import Pin
import time
from dicc import *
from IC7432.ic7432_pin import *

'''
          OR GATE
    In1     In2     Out
    -------------------
      0      0      0
      0      1      1
      1      0      1
      1      1      1
    -------------------
'''

def metadata():
    ic_pin_count  = IC_14_PIN
    ic_brief_name = "2 input OR Gate IC"

    return ic_pin_count, ic_brief_name


def test_run(index, input1, input2, output):
    error = 0

    input1.value(LOW)
    input2.value(LOW)
    if output.value() != LOW:
        error += 1

    input1.value(LOW)
    input2.value(HIGH)
    if output.value() != HIGH:
        error += 1

    input1.value(HIGH)
    input2.value(LOW)
    if output.value() != HIGH:
        error += 1

    input1.value(HIGH)
    input2.value(HIGH)
    if output.value() != HIGH:
        error += 1

    if error == 0:
        print("OR gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("OR gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    or1_out = Pin(PIN_OR1_OUT, Pin.IN, Pin.PULL_DOWN)
    or2_out = Pin(PIN_OR2_OUT, Pin.IN, Pin.PULL_DOWN)
    or3_out = Pin(PIN_OR3_OUT, Pin.IN, Pin.PULL_DOWN)
    or4_out = Pin(PIN_OR4_OUT, Pin.IN, Pin.PULL_DOWN)

    or1_in1 = Pin(PIN_OR1_IN_1, Pin.OUT)
    or1_in2 = Pin(PIN_OR1_IN_2, Pin.OUT)
    or2_in1 = Pin(PIN_OR2_IN_1, Pin.OUT)
    or2_in2 = Pin(PIN_OR2_IN_2, Pin.OUT)
    or3_in1 = Pin(PIN_OR3_IN_1, Pin.OUT)
    or3_in2 = Pin(PIN_OR3_IN_2, Pin.OUT)
    or4_in1 = Pin(PIN_OR4_IN_1, Pin.OUT)
    or4_in2 = Pin(PIN_OR4_IN_2, Pin.OUT)


    print("4 OR IC 7432 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, or1_in1, or1_in2, or1_out)
    time.sleep(0.5)
    exit_val += test_run(2, or2_in1, or2_in2, or2_out)
    time.sleep(0.5)
    exit_val += test_run(3, or3_in1, or3_in2, or3_out)
    time.sleep(0.5)
    exit_val += test_run(4, or4_in1, or4_in2, or4_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
