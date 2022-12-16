import time

import welcome
from dicc import *

from IC4511 import ic4511
from IC7400 import ic7400
from IC7432 import ic7432

SUPPORTED_IC = {
    "7400" : ic7400,
    "7432" : ic7432,
    "4511" : ic4511,
    }

welcome.welcome_led_blink()
welcome.print_intro()

while True:
    print("\nCurrently we support: ")
    for key in SUPPORTED_IC:
        print(key)
    selected_ic = input("Select Any IC: ")
    print("\n")
    if selected_ic in SUPPORTED_IC:
        try:
            status = SUPPORTED_IC[selected_ic].main()
            if status == RETURN_SUCCESS:
                print("\nVERDICT: IC",selected_ic,"perfetly working.")
                print("-"*(30+len(selected_ic)))
            else:
                print("\nVERDICT: IC",selected_ic,"looks not good, Please cross verify manually.")
                print("-"*(57+len(selected_ic)))
        except Exception as e:
            print("ERROR:", e)
    else:
        print("Sorry!", selected_ic, " is not supported. Try Again.")
    print("\n")
    time.sleep(0.5)