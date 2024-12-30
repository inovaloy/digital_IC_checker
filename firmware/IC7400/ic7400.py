from machine import Pin
import time
from dicc import *
from IC7400.ic7400_pin import *

'''
        NAND GATE
    In1     In2     Out
    -------------------
      0      0      1
      0      1      1
      1      0      1
      1      1      0
    -------------------
'''

def metadata():
    ic_pin_count  = IC_14_PIN
    ic_brief_name = "2 input NAND Gate IC"

    return ic_pin_count, ic_brief_name


def test_run(index, input1, input2, output):
    error = 0

    input1.value(LOW)
    input2.value(LOW)
    if output.value() != HIGH:
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
        print("NAND gate", index, "OK")
        return RETURN_SUCCESS
    else:
        print("NAND gate", index, "Not OK")
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    nand1_out = Pin(PIN_NAND1_OUT, Pin.IN, Pin.PULL_DOWN)
    nand2_out = Pin(PIN_NAND2_OUT, Pin.IN, Pin.PULL_DOWN)
    nand3_out = Pin(PIN_NAND3_OUT, Pin.IN, Pin.PULL_DOWN)
    nand4_out = Pin(PIN_NAND4_OUT, Pin.IN, Pin.PULL_DOWN)

    nand1_in1 = Pin(PIN_NAND1_IN_1, Pin.OUT)
    nand1_in2 = Pin(PIN_NAND1_IN_2, Pin.OUT)
    nand2_in1 = Pin(PIN_NAND2_IN_1, Pin.OUT)
    nand2_in2 = Pin(PIN_NAND2_IN_2, Pin.OUT)
    nand3_in1 = Pin(PIN_NAND3_IN_1, Pin.OUT)
    nand3_in2 = Pin(PIN_NAND3_IN_2, Pin.OUT)
    nand4_in1 = Pin(PIN_NAND4_IN_1, Pin.OUT)
    nand4_in2 = Pin(PIN_NAND4_IN_2, Pin.OUT)


    print("4 NAND IC 7400 test started...")

    time.sleep(0.5)
    exit_val += test_run(1, nand1_in1, nand1_in2, nand1_out)
    time.sleep(0.5)
    exit_val += test_run(2, nand2_in1, nand2_in2, nand2_out)
    time.sleep(0.5)
    exit_val += test_run(3, nand3_in1, nand3_in2, nand3_out)
    time.sleep(0.5)
    exit_val += test_run(4, nand4_in1, nand4_in2, nand4_out)
    time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
