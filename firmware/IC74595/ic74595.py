from machine import Pin
import time
from dicc import *
from IC74595.ic74595_pin import *

def test_run(data,
             sipo_data,
             sipo_latch,
             sipo_clock,
             output0,
             output1,
             output2,
             output3,
             output4,
             output5,
             output6,
             output7,
             output7_nt):

    error = 0
    output_arr = [
            output0,
            output1,
            output2,
            output3,
            output4,
            output5,
            output6,
            output7
        ]
    sipo_data.value(LOW)
    sipo_clock.value(LOW)
    sipo_latch.value(HIGH)

    for i in range(8):
        sipo_data.value((data >> i) & 1)

        sipo_clock(HIGH)
        sipo_clock(LOW)

    sipo_latch(LOW)
    sipo_latch(HIGH)

    for i in range(8):
        if output_arr[7 - i].value() != ((data >> i) & 1):
            error += 1


    if error == 0:
        print("SIPO Register OK with value ", data)
        return RETURN_SUCCESS
    else:
        print("SIPO Register NOT OK with value ", data)
        return RETURN_ERROR


def main():
    exit_val = RETURN_SUCCESS
    sipo_out0 = Pin(PIN_SIPO_OUT_Q0, Pin.IN, Pin.PULL_DOWN)
    sipo_out1 = Pin(PIN_SIPO_OUT_Q1, Pin.IN, Pin.PULL_DOWN)
    sipo_out2 = Pin(PIN_SIPO_OUT_Q2, Pin.IN, Pin.PULL_DOWN)
    sipo_out3 = Pin(PIN_SIPO_OUT_Q3, Pin.IN, Pin.PULL_DOWN)
    sipo_out4 = Pin(PIN_SIPO_OUT_Q4, Pin.IN, Pin.PULL_DOWN)
    sipo_out5 = Pin(PIN_SIPO_OUT_Q5, Pin.IN, Pin.PULL_DOWN)
    sipo_out6 = Pin(PIN_SIPO_OUT_Q6, Pin.IN, Pin.PULL_DOWN)
    sipo_out7 = Pin(PIN_SIPO_OUT_Q7, Pin.IN, Pin.PULL_DOWN)
    sipo_out7_nt = Pin(PIN_SIPO_OUT_Q7_NOT, Pin.IN, Pin.PULL_DOWN)

    sipo_data  = Pin(PIN_SIPO_IN_DATA, Pin.OUT)
    sipo_latch = Pin(PIN_SIPO_IN_LATCH, Pin.OUT)
    sipo_clock = Pin(PIN_SIPO_IN_CLOCK, Pin.OUT)

    sipo_output_enable = Pin(PIN_SIPO_IN_OP_ENBL, Pin.OUT)
    sipo_master_reset  = Pin(PIN_SIPO_IN_RESET, Pin.OUT)

    sipo_output_enable.value(LOW)
    sipo_master_reset.value(HIGH)


    print("Serial In to Parallel Out Shift Register IC 74595 test started...")

    time.sleep(0.5)

    for data in range(0, 10):
        exit_val += test_run(data,
                            sipo_data,
                            sipo_latch,
                            sipo_clock,
                            sipo_out0,
                            sipo_out1,
                            sipo_out2,
                            sipo_out3,
                            sipo_out4,
                            sipo_out5,
                            sipo_out6,
                            sipo_out7,
                            sipo_out7_nt)
        time.sleep(0.5)

    print("Test Completed.")

    if exit_val == RETURN_SUCCESS:
        return RETURN_SUCCESS
    else:
        return RETURN_ERROR
