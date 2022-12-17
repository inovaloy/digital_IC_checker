from machine import Pin
import time
from dicc import *
from IC7402.ic7402_pin import *

'''
          NOR GATE
    In1     In2     Out
    -------------------
      0      0      1
      0      1      0
      1      0      0
      1      1      0
    -------------------
'''

def test_run(index, input1, input2, output):
    errand = 0

    input1.value(LOW)
    input2.value(LOW)
    if output.value() != HIGH:
        errand += 1

    input1.value(LOW)
    input2.value(HIGH)
    if output.value() != LOW:
        errand += 1

    input1.value(HIGH)
    input2.value(LOW)
    if output.value() != LOW:
        errand += 1

    input1.value(HIGH)
    input2.value(HIGH)
    if output.value() != LOW:
        errand += 1

    if errand == 0:
        print("NOR gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("NOR gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    nor1_out = Pin(PIN_NOR1_OUT, Pin.IN, Pin.PULL_DOWN)
    nor2_out = Pin(PIN_NOR2_OUT, Pin.IN, Pin.PULL_DOWN)
    nor3_out = Pin(PIN_NOR3_OUT, Pin.IN, Pin.PULL_DOWN)
    nor4_out = Pin(PIN_NOR4_OUT, Pin.IN, Pin.PULL_DOWN)

    nor1_in1 = Pin(PIN_NOR1_IN_1, Pin.OUT)
    nor1_in2 = Pin(PIN_NOR1_IN_2, Pin.OUT)
    nor2_in1 = Pin(PIN_NOR2_IN_1, Pin.OUT)
    nor2_in2 = Pin(PIN_NOR2_IN_2, Pin.OUT)
    nor3_in1 = Pin(PIN_NOR3_IN_1, Pin.OUT)
    nor3_in2 = Pin(PIN_NOR3_IN_2, Pin.OUT)
    nor4_in1 = Pin(PIN_NOR4_IN_1, Pin.OUT)
    nor4_in2 = Pin(PIN_NOR4_IN_2, Pin.OUT)


    print("4 NOR IC 7402 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, nor1_in1, nor1_in2, nor1_out)
    time.sleep(0.5)
    exit_val += test_run(2, nor2_in1, nor2_in2, nor2_out)
    time.sleep(0.5)
    exit_val += test_run(3, nor3_in1, nor3_in2, nor3_out)
    time.sleep(0.5)
    exit_val += test_run(4, nor4_in1, nor4_in2, nor4_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
