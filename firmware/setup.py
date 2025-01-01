from utility import *
from dicc    import *
from main_gui import get_all_wifi, wifi_setup, get_wifi_ip

# Global variables
col_size            = 60
row_size            = 15
menu_page           = None


# Global constants
NO_BACK_OPTION      = 0
BACK_OPTION         = 1

SETUP_MENU          = "SETUP MENU"
EXECUTION_MODE_MENU = "EXECUTION MODE"
INFORMATION_MENU    = "INFORMATION"
WIFI_NAME_MENU      = "WIFI NAME"
WIFI_PASSWORD_MENU  = "WIFI PASSWORD"


OPTION_0            = "0"
OPTION_1            = "1"
OPTION_2            = "2"
OPTION_3            = "3"
OPTION_4            = "4"
OPTION_5            = "5"
OPTION_6            = "6"
OPTION_7            = "7"
OPTION_8            = "8"
OPTION_9            = "9"
OPTION_10           = "10"
OPTION_11           = "11"
OPTION_12           = "12"
OPTION_13           = "13"
OPTION_14           = "14"


def render_menu(heading, menu_option, back_option = 0, status = ""):
    global menu_page

    menu_page = heading

    if back_option:
        back_option = 1

    print("\n\n\n")
    print("#" * col_size)
    print(txt_padding("", col_size, True, 0))
    print(txt_padding(heading.upper(), col_size, True, 0))
    print(txt_padding("", col_size, True, 0))
    print("#" * col_size)

    for menu in menu_option:
        print(txt_padding(menu, col_size, False, 2))

    for _ in range(row_size - len(menu_option) - back_option - 2):
        print(txt_padding("", col_size, False, 2))

    if back_option:
        print(txt_padding("< 0: Back", col_size, False, 2))

    print(txt_padding(status, col_size, False, 1))
    print("#" * col_size)



def render_setup_menu(status = ""):
    render_menu(SETUP_MENU, [
        "> 1:  Execution Mode",
        "> 2:  Set Wifi Credential",
        "> 3:  Information",
        "> 4:  Exit"
    ], NO_BACK_OPTION, status)


def render_execution_mode_menu(status = ""):
    render_menu(EXECUTION_MODE_MENU, [
        "> 1:  Set CLI Mode",
        "> 2:  Set GUI Mode"
    ], BACK_OPTION, status)


def render_information_menu(status = ""):
    config_data = get_config_data()
    version        = config_data["version"]
    flash_time     = config_data["build_time"]

    user_config_data = get_user_config_data()
    execution_mode = user_config_data.get("mode")
    if execution_mode == None:
        execution_mode = "Not Set"
    elif execution_mode == MODE_CLI:
        execution_mode = "CLI"
    elif execution_mode == MODE_GUI:
        execution_mode = "GUI"

    wifi_name = user_config_data.get("wifi")
    if wifi_name == None:
        wifi_name = "Not Set"

    render_menu(INFORMATION_MENU, [
        f"Firmware Version : {version}",
        f"Build Time       : {flash_time}",
        f"Execution Mode   : {execution_mode}",
        f"WiFi             : {wifi_name}",
        f"IP Address       : {get_wifi_ip()}"
    ], BACK_OPTION, status)


def render_wifi_name_menu(status = ""):
    wifi_names = [wifi for wifi in get_all_wifi() if wifi.strip()]

    render_menu(WIFI_NAME_MENU, [
        f"> {i + 1}: {wifi}" for i, wifi in enumerate(wifi_names)
    ], BACK_OPTION, status)

    return wifi_names


def render_wifi_password_menu(status = ""):
    render_menu(WIFI_PASSWORD_MENU, [
        "Enter Password"
    ], NO_BACK_OPTION, status)


def setup(status = ""):
    global menu_page
    input_msg = ""
    wifi_name = ""

    while True:
        if menu_page == SETUP_MENU or menu_page == None:
            render_setup_menu(status)
        if menu_page == EXECUTION_MODE_MENU:
            render_execution_mode_menu(status)
        if menu_page == INFORMATION_MENU:
            render_information_menu(status)
        if menu_page == WIFI_NAME_MENU:
            wifi_names = render_wifi_name_menu(status)
        if menu_page == WIFI_PASSWORD_MENU:
            render_wifi_password_menu(status)

        usr_input = input(f"{input_msg}: ")
        input_msg = ""

        # SETUP MENU CONTROLS
        if menu_page == SETUP_MENU or menu_page == None:
            if usr_input == OPTION_1:
                status = ""
                menu_page = EXECUTION_MODE_MENU
                continue
            elif usr_input == OPTION_2:
                status = ""
                menu_page = WIFI_NAME_MENU
                continue
            elif usr_input == OPTION_3:
                status = ""
                menu_page = INFORMATION_MENU
                continue
            elif usr_input == OPTION_4:
                break
            else:
                print("Invalid option.")
                continue

        # EXECUTION MODE MENU CONTROLS
        if menu_page == EXECUTION_MODE_MENU:
            if usr_input == OPTION_1:
                set_execution_mode(MODE_CLI)
                status = "CLI mode set"
                menu_page = SETUP_MENU
                continue
            elif usr_input == OPTION_2:
                set_execution_mode(MODE_GUI)
                status = "GUI mode set"
                menu_page = SETUP_MENU
                continue
            elif usr_input == OPTION_0:
                status = ""
                menu_page = SETUP_MENU
                continue
            else:
                print("Invalid option.")
                continue

        # INFORMATION MENU CONTROLS
        if menu_page == INFORMATION_MENU:
            if usr_input == OPTION_0:
                status = ""
                menu_page = SETUP_MENU
                continue
            else:
                print("Invalid option.")
                continue

        # WIFI NAME MENU CONTROLS
        if menu_page == WIFI_NAME_MENU:
            if usr_input == OPTION_0:
                status = ""
                menu_page = SETUP_MENU
                continue
            elif usr_input in [str(i + 1) for i in range(len(wifi_names))]:
                status = ""
                menu_page = WIFI_PASSWORD_MENU
                wifi_name = wifi_names[int(usr_input) - 1]
                input_msg = f"Password for '{wifi_name}'"
                continue
            else:
                print("Invalid option.")

        # WIFI PASSWORD MENU CONTROLS
        if menu_page == WIFI_PASSWORD_MENU:
            wifi_status, _ = wifi_setup(wifi_name, usr_input)
            if wifi_status:
                status = "WiFi connected"
                enc_pass = get_encrypted_password(usr_input)
                update_wifi_name(wifi_name)
                update_wifi_password(enc_pass)
                menu_page = SETUP_MENU
            else:
                status = "WiFi connection failed"
                menu_page = WIFI_NAME_MENU
            continue


############ Menu Back Logics ##############
def set_execution_mode(mode):
    config_data = get_user_config_data()
    config_data["mode"] = mode
    update_user_config_data(config_data)


def update_wifi_name(wifi_name):
    config_data = get_user_config_data()
    config_data["wifi"] = wifi_name
    update_user_config_data(config_data)


def update_wifi_password(enc_pass):
    config_data = get_user_config_data()
    config_data["pass"] = enc_pass
    update_user_config_data(config_data)
