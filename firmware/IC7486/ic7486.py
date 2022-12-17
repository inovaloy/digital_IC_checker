from machine import Pin
import time
from dicc import *
from IC7486.ic7486_pin import *

'''
        XOR GATE
    In1     In2     Out
    -------------------
      0      0      0
      0      1      1
      1      0      1
      1      1      0
    -------------------
'''

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
    if output.value() != LOW:
        error += 1

    if error == 0:
        print("XOR gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("XOR gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    xor1_out = Pin(PIN_XOR1_OUT, Pin.IN, Pin.PULL_DOWN)
    xor2_out = Pin(PIN_XOR2_OUT, Pin.IN, Pin.PULL_DOWN)
    xor3_out = Pin(PIN_XOR3_OUT, Pin.IN, Pin.PULL_DOWN)
    xor4_out = Pin(PIN_XOR4_OUT, Pin.IN, Pin.PULL_DOWN)

    xor1_in1 = Pin(PIN_XOR1_IN_1, Pin.OUT)
    xor1_in2 = Pin(PIN_XOR1_IN_2, Pin.OUT)
    xor2_in1 = Pin(PIN_XOR2_IN_1, Pin.OUT)
    xor2_in2 = Pin(PIN_XOR2_IN_2, Pin.OUT)
    xor3_in1 = Pin(PIN_XOR3_IN_1, Pin.OUT)
    xor3_in2 = Pin(PIN_XOR3_IN_2, Pin.OUT)
    xor4_in1 = Pin(PIN_XOR4_IN_1, Pin.OUT)
    xor4_in2 = Pin(PIN_XOR4_IN_2, Pin.OUT)


    print("4 XOR IC 7486 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, xor1_in1, xor1_in2, xor1_out)
    time.sleep(0.5)
    exit_val += test_run(2, xor2_in1, xor2_in2, xor2_out)
    time.sleep(0.5)
    exit_val += test_run(3, xor3_in1, xor3_in2, xor3_out)
    time.sleep(0.5)
    exit_val += test_run(4, xor4_in1, xor4_in2, xor4_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR