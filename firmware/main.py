import os
import json
from dicc import *
from utility import *
from setup import *

def get_execution_mode():
    mode = None
    try:
        json_data = get_config_data()
        if json_data == None:
            print("Error: configuration file not found.")
            exit(-1)

        mode = json_data["mode"]
    except:
        mode = MODE_UNKNOWN

        if MACHINE_RPI_PICO_W not in get_machine_name():
            mode = MODE_CLI

    return mode


def get_wifi_credential():
    wifi_name = None
    wifi_pass = None
    try:
        json_data = get_config_data()
        if json_data == None:
            print("Error: configuration file not found.")
            exit(-1)

        wifi_name = json_data.get("wifi")
        wifi_pass = json_data.get("pass")
    except:
        pass

    return wifi_name, wifi_pass


def connect_wifi():
    wifi_name, wifi_pass = get_wifi_credential()
    if wifi_name == None or wifi_pass == None:
        print("Error: WiFi credentials not found.")
        return False

    wifi_pass = get_decrypted_password(wifi_pass)
    status, _ = wifi_setup(wifi_name, wifi_pass)
    return status


def main_func():
    jump_to_setup = False
    mode = get_execution_mode()
    if mode == MODE_UNKNOWN:
        print("RT mode not set; Jump to setup mode.")
        message = "Select execution mode"
        jump_to_setup = True

    if not connect_wifi() and mode == MODE_GUI:
        print("WiFi connection failed.")
        message = "Select wifi connection"
        jump_to_setup = True

    if jump_to_setup:
        setup(message)
        main_func()

    if mode == MODE_CLI:
        print("CLI mode")
        import main_cli as main
    elif mode == MODE_GUI:
        print("GUI mode")
        import main_gui as main
    else:
        print("Unknown mode")
        main_func()

    main.main()


main_func()