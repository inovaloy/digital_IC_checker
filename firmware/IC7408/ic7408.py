from machine import Pin
import time
from dicc import *
from IC7408.ic7408_pin import *

'''
          AND GATE
    In1     In2     Out
    -------------------
      0      0      0
      0      1      0
      1      0      0
      1      1      1
    -------------------
'''

def test_run(index, input1, input2, output):
    errand = 0

    input1.value(LOW)
    input2.value(LOW)
    if output.value() != LOW:
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
    if output.value() != HIGH:
        errand += 1

    if errand == 0:
        print("AND gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("AND gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    and1_out = Pin(PIN_AND1_OUT, Pin.IN, Pin.PULL_DOWN)
    and2_out = Pin(PIN_AND2_OUT, Pin.IN, Pin.PULL_DOWN)
    and3_out = Pin(PIN_AND3_OUT, Pin.IN, Pin.PULL_DOWN)
    and4_out = Pin(PIN_AND4_OUT, Pin.IN, Pin.PULL_DOWN)

    and1_in1 = Pin(PIN_AND1_IN_1, Pin.OUT)
    and1_in2 = Pin(PIN_AND1_IN_2, Pin.OUT)
    and2_in1 = Pin(PIN_AND2_IN_1, Pin.OUT)
    and2_in2 = Pin(PIN_AND2_IN_2, Pin.OUT)
    and3_in1 = Pin(PIN_AND3_IN_1, Pin.OUT)
    and3_in2 = Pin(PIN_AND3_IN_2, Pin.OUT)
    and4_in1 = Pin(PIN_AND4_IN_1, Pin.OUT)
    and4_in2 = Pin(PIN_AND4_IN_2, Pin.OUT)


    print("4 AND IC 7408 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, and1_in1, and1_in2, and1_out)
    time.sleep(0.5)
    exit_val += test_run(2, and2_in1, and2_in2, and2_out)
    time.sleep(0.5)
    exit_val += test_run(3, and3_in1, and3_in2, and3_out)
    time.sleep(0.5)
    exit_val += test_run(4, and4_in1, and4_in2, and4_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
