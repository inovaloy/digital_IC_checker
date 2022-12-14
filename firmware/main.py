import time
from collections import OrderedDict

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


SUPPORTED_IC = {
    "7400"  : [ic7400,  "2 input NAND Gate IC"],
    "7402"  : [ic7402,  "2 input NOR Gate IC"],
    "7404"  : [ic7404,  "NOT Gate IC"],
    "7408"  : [ic7408,  "2 input AND Gate IC"],
    "7432"  : [ic7432,  "2 input OR Gate IC"],
    "7486"  : [ic7486,  "2 input XOR Gate IC"],
    "74595" : [ic74595, "Serial In to Parallel Out Shift Register IC"],
    # "4511"  : [ic4511,  "BCD to 7 Segment Decoder IC"],
    }

welcome.welcome_led_static()
time.sleep(1)
welcome.print_intro()
welcome.welcome_led_blink()

SUPPORTED_IC = OrderedDict(sorted(SUPPORTED_IC.items()))

while True:
    print("\nCurrently we support: ")
    for key in SUPPORTED_IC:
        colon = " "*(5-len(key))+":"
        print(" ", key, colon, SUPPORTED_IC[key][1])
    selected_ic = input("\nSelect Any IC: ")
    print("\n")
    if selected_ic in SUPPORTED_IC:
        try:
            status = SUPPORTED_IC[selected_ic][0].main()
            if status == RETURN_SUCCESS:
                print("\nVERDICT: IC",selected_ic,"perfetly working.")
                print("-"*(30+len(selected_ic)))
            else:
                print("\nVERDICT: IC",selected_ic,"looks not good, Please cross verify manually.")
                print("-"*(57+len(selected_ic)))
            welcome.blink_status_led(status)
        except Exception as e:
            print("ERROR:", e)
    else:
        print("Sorry!", selected_ic, " is not supported. Try Again.")
    print("\n")
    time.sleep(0.5)
