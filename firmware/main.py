import time
from collections import OrderedDict
import _thread

import welcome
from dicc import *


from IC4511 import ic4511
from IC7400 import ic7400
from IC7402 import ic7402
from IC7404 import ic7404
from IC7408 import ic7408
from IC7432 import ic7432
from IC7486 import ic7486
from IC74595 import ic74595
from IC24LC512 import ic24lc512
from IC24LC256 import ic24lc256

SUPPORTED_IC = {
    "7400"  : [
        ic7400,
        IC_14_PIN,
        "2 input NAND Gate IC"
        ],

    "7402"  : [
        ic7402,
        IC_14_PIN,
        "2 input NOR Gate IC"
        ],

    "7404"  : [
        ic7404,
        IC_14_PIN,
        "NOT Gate IC"
        ],

    "7408"  : [
        ic7408,
        IC_14_PIN,
        "2 input AND Gate IC"
        ],

    "7432"  : [
        ic7432,
        IC_14_PIN,
        "2 input OR Gate IC"
        ],

    "7486"  : [
        ic7486,
        IC_14_PIN,
        "2 input XOR Gate IC"
        ],

    "74595" : [
        ic74595,
        IC_16_PIN,
        "Serial In to Parallel Out Shift Register IC"
        ],

    "24LC512" : [
        ic24lc512,
        IC_8_PIN,
        "512Kbits EEPROM IC"
        ],

    "24LC256" : [
        ic24lc256,
        IC_8_PIN,
        "256Kbits EEPROM IC"
        ],

    "4511"  : [
        ic4511,
        IC_16_PIN,
        "BCD to 7 Segment Decoder IC"
        ],
    }

welcome.welcome_led_static()
time.sleep(1)
welcome.print_intro()
welcome.welcome_led_blink()

SUPPORTED_IC = OrderedDict(sorted(SUPPORTED_IC.items()))

while True:
    print("\nCurrently we support: ")
    for key in SUPPORTED_IC:
        colon = " "*(8-len(key))+":"
        print(" ", key, colon, SUPPORTED_IC[key][2])
    selected_ic = input("\nSelect Any IC: ")
    selected_ic = selected_ic.upper()
    print("\n")
    if not welcome.check_external_power():
        continue
    if selected_ic in SUPPORTED_IC:
        welcome.select_ic_base_led(SUPPORTED_IC[selected_ic][1])
        ans = input("Do you install the ic into selected slot (y/n) :")
        if ans.upper() == "Y" or ans == "":
            try:
                thread_handeler = [ON]
                flash_thread = _thread.start_new_thread(welcome.flash_code_running_led, (thread_handeler,))
                status = SUPPORTED_IC[selected_ic][0].main()
                thread_handeler[0] = OFF
                if status == RETURN_SUCCESS:
                    print("\nVERDICT: IC",selected_ic,"perfetly working.")
                    print("-"*(30+len(selected_ic)))
                elif status != RETURN_NA:
                    print("\nVERDICT: IC",selected_ic,"looks not good, Please cross verify manually.")
                    print("-"*(57+len(selected_ic)))
                welcome.blink_status_led(status)
            except Exception as e:
                thread_handeler[0] = OFF
                print("\nERROR:", e)
        welcome.select_ic_base_led(IC_NO_PIN)
    else:
        print("Sorry!", selected_ic, " is not supported. Try Again.")
    print("\n")
    time.sleep(0.5)
