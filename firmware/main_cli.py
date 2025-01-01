import time
from collections import OrderedDict
import _thread
import os

import welcome
import utility
from dicc import *


SUPPORTED_IC = dict()

# Importing all the IC library automatically
for path in os.listdir():
    if utility.isFolder(path):
        if path[:2] == "IC":
            library_str = path.lower()
            try:
                exec("from " + path + " import " + library_str)

                ic_key = library_str[2:].upper()
                ic_pin_count  = None
                ic_brief_name = None
                library       = None
                exec("ic_pin_count, ic_brief_name = " + library_str + ".metadata()")
                exec("library =" + library_str)

                if ic_pin_count != None and ic_brief_name != None and library != None:
                    SUPPORTED_IC[ic_key] = [
                        library,
                        ic_pin_count,
                        ic_brief_name
                    ]

            except Exception as e:
                print(e)

# Sorting the dictionary to print in a beautiful format
SUPPORTED_IC = OrderedDict(sorted(SUPPORTED_IC.items()))

#  Main while loop
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
                    print("\nVERDICT: IC", selected_ic, "perfetly working.")
                    print("-"*(30+len(selected_ic)))
                elif status != RETURN_NA:
                    print("\nVERDICT: IC", selected_ic, "not looks good, Please cross verify manually.")
                    print("-"*(57+len(selected_ic)))
                welcome.blink_status_led(status)
            except Exception as e:
                thread_handeler[0] = OFF
                print("\nERROR:", e)
        welcome.select_ic_base_led(IC_NO_PIN)
    else:
        if selected_ic:
            print("Sorry!", selected_ic, " is not supported. Try Again.")

    time.sleep(0.5)
    print("\n")
    welcome.print_intro()
