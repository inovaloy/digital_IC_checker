import os
import subprocess
import json
import shutil
from datetime import datetime
import sys

path = 'firmware'

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAIL    = 1

TYPE_FILE   = 0
TYPE_FOLDER = 1
TYPE_NONE   = -1

SECRECT_CONFIG_UPDATE = 1
NO_CONFIG_UPDATE = 0

created_folder_list = []

# install cmd "pip3 install adafruit-ampy"
uploader        = "ampy"
port            = "/dev/ttyACM0"
config_bkp_file = "config_bkp.json"
config_file     = "config.json"


def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def get_current_time():
    now = datetime.now()
    ordinal_date = make_ordinal(now.strftime("%d"))
    current_time = now.strftime("%I:%M:%S %p  "+ordinal_date+" %B %Y")
    return current_time


def update_flash_time_to_config():
    shutil.copyfile(os.path.join(path, config_file), os.path.join(path, config_bkp_file))
    with open(os.path.join(path, config_file), 'r') as file:
        json_data = json.loads(file.read())

    json_data["build_time"] = get_current_time()
    config = open(os.path.join(path, config_file), 'w')
    config.write(json.dumps(json_data, indent=4))
    config.close()


def restore_config_file():
    if os.path.exists(os.path.join(path, config_bkp_file)):
        shutil.copyfile(os.path.join(path, config_bkp_file), os.path.join(path, config_file))
        os.remove(os.path.join(path, config_bkp_file))


def run_cmd(base_arg):
    output = []
    process = subprocess.Popen(base_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline().strip().decode('UTF-8')
        if line != "":
            output.append(line)

    process_exit_code = process.wait()
    return process_exit_code, output


def check_folder_exist(folder_path):
    actual_folder_path = os.path.abspath(folder_path).replace(os.path.abspath(path), "")
    exitcode , output = run_cmd([uploader, "--port", port, "ls", actual_folder_path])
    return exitcode


def create_specific_new_folder(folder_path):
    actual_folder_path = os.path.abspath(folder_path).replace(os.path.abspath(path), "")
    list_dir = actual_folder_path.split(os.path.sep)
    folder_length = len(list_dir)

    exit_code = EXIT_CODE_FAIL
    checking_path = actual_folder_path

    while exit_code == EXIT_CODE_FAIL:
        folder_length -= 1
        checking_path = checking_path.replace(list_dir[folder_length], "")[:-1]
        if checking_path == "":
            break
        exit_code = check_folder_exist(checking_path)

    folder_need_to_create = actual_folder_path.replace(checking_path, "")
    list_dir = folder_need_to_create.split(os.path.sep)
    folder_length = len(list_dir)

    for dir in list_dir:
        if dir == "":
            continue
        checking_path = os.path.join(checking_path, dir)
        exitcode , output = run_cmd([uploader, "--port", port, "mkdir", checking_path])
        if exitcode == EXIT_CODE_SUCCESS:
            print("Create Folder : ", checking_path)
            created_folder_list.append(checking_path)
        else:
            print("ERROR: Not albe to Create : ", checking_path)
            return exitcode
    return exitcode


def clean_target(clean_type = TYPE_NONE, dest = None):

    if (clean_type == TYPE_FILE) or (clean_type == TYPE_FOLDER):
        parent_path = os.path.dirname(dest)
        exitcode , output = run_cmd([uploader, "--port", port, "ls", parent_path])
        if exitcode == EXIT_CODE_SUCCESS:
            for item in output:
                if item == dest:
                    if clean_type == TYPE_FILE:
                        exitcode , output = run_cmd([uploader, "--port", port, "rm", dest])
                        if exitcode == EXIT_CODE_SUCCESS:
                            print("Erase file    : ", dest)
                        else:
                            print("ERROR: Not albe to Remove : ", dest)
                    else:
                        exitcode , output = run_cmd([uploader, "--port", port, "rmdir", dest])
                        if exitcode == EXIT_CODE_SUCCESS:
                            print("Erase folder  : ", dest)
                        else:
                            print("ERROR: Not albe to Remove : ", dest)
            return exitcode
        else:
            return EXIT_CODE_SUCCESS


    exitcode , output = run_cmd([uploader, "--port", port, "ls"])
    if exitcode == EXIT_CODE_SUCCESS:
        for item in output:
            if "." in item.split("/")[-1]:
                item = item.strip()
                exitcode , output = run_cmd([uploader, "--port", port, "rm", item])
                if exitcode == EXIT_CODE_SUCCESS:
                    print("Erase file    : ", item)
                else:
                    print("ERROR: Not albe to Remove : ", item)
                    return exitcode
            else:
                exitcode , output = run_cmd([uploader, "--port", port, "rmdir", item])
                if exitcode == EXIT_CODE_SUCCESS:
                    print("Erase folder  : ", item)
                else:
                    print("ERROR: Not albe to Remove : ", item)
                    return exitcode

    return EXIT_CODE_SUCCESS


def create_new_folder(dest_dir):
    global created_folder_list
    abs_dest_path = os.path.abspath(dest_dir)
    abs_home_path = os.path.abspath(path)
    working_path = abs_dest_path.replace(abs_home_path, "")
    dir_list = working_path.split(os.path.sep)
    make_folder = ""
    for d in dir_list:
        make_folder = os.path.join(make_folder, d)
        if d == os.path.sep or d == "":
            continue
        if make_folder not in created_folder_list:
            exitcode , output = run_cmd([uploader, "--port", port, "mkdir", make_folder])
            if exitcode == EXIT_CODE_SUCCESS:
                print("Create Folder : ", make_folder)
                created_folder_list.append(make_folder)
            else:
                print("ERROR: Not albe to Create : ", make_folder)
                return exitcode

    return EXIT_CODE_SUCCESS


def create_new_file(dest_file, config_update = NO_CONFIG_UPDATE):
    actual_file = os.path.abspath(dest_file).replace(os.path.abspath(path), "")
    exitcode , output = run_cmd([uploader, "--port", port, "put", dest_file, actual_file])
    if config_update == SECRECT_CONFIG_UPDATE:
        return exitcode
    if exitcode == EXIT_CODE_SUCCESS:
        print("Send File     : ", actual_file)
    else:
        print("ERROR: Not albe to Send : ", actual_file)
        return exitcode

    return EXIT_CODE_SUCCESS


def upload_firmware(upload_type = TYPE_NONE, dest = None):
    if upload_type == TYPE_FOLDER:
        dest_path = dest
    else:
        dest_path = path
    for root, directories, files in os.walk(dest_path, topdown=False):
        for name in directories:
            exitcode = create_new_folder(os.path.join(root, name))
            if exitcode != EXIT_CODE_SUCCESS:
                return exitcode
    for root, directories, files in os.walk(dest_path, topdown=False):
        for name in files:
            if name == config_bkp_file:
                continue
            exitcode = create_new_file(os.path.join(root, name))
            if exitcode != EXIT_CODE_SUCCESS:
                return exitcode

    return EXIT_CODE_SUCCESS


def noramal_firmware_update():
    print("Removeing old files from Hardware...")
    if clean_target() != EXIT_CODE_SUCCESS:
        exit(0)
    update_flash_time_to_config()
    print("\nUploading new files to Hardware...")
    if upload_firmware() != EXIT_CODE_SUCCESS:
        exit(0)
    restore_config_file()


def partial_firmware_update(file_list):
    config_update = False
    for file in file_list:
        file_destination = os.path.abspath(file).replace(os.path.abspath(path), "")
        if os.path.basename(file) == config_file:
            config_update = True
        if os.path.isfile(file):
            if check_folder_exist(os.path.dirname(file)) == EXIT_CODE_SUCCESS:
                clean_target(TYPE_FILE, file_destination)
                create_new_file(os.path.abspath(file))
            else:
                create_specific_new_folder(os.path.dirname(file))
                create_new_file(os.path.abspath(file))
        else:
            clean_target(TYPE_FOLDER, file_destination)
            upload_firmware(TYPE_FOLDER, os.path.abspath(file))

    if not config_update:
        print("Updating the Metadata...")
        update_flash_time_to_config()
        create_new_file(os.path.join(path, config_file), SECRECT_CONFIG_UPDATE)
        restore_config_file()


if __name__ == "__main__":
    print("\n\t\t:Digital IC Checking:\n\tFirmware Upload will start shortly\n")
    if not os.path.exists(port):
        print("ERROR:", port, "not available")
        exit(0)
    if len(sys.argv) > 1:
        print("Jump to partial fimmware upload mode")

        for file in sys.argv[1:]:
            if not os.path.exists(file):
                print(file, "is not exist")
                exit(0)
            if os.path.abspath(path) not in os.path.abspath(file):
                print(file," upload blocked")
                print("Not able to upload files or folder from unknown location")
                exit(0)

        partial_firmware_update(sys.argv[1:])
    else:
        noramal_firmware_update()

    print("\n\nFirmware Uploaded Succesfully Please restart the hardware once.\n")
