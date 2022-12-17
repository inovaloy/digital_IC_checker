import os
import subprocess
import json
import shutil
from datetime import datetime

path = 'firmware'

EXIT_CODE_SUCCESS = 0
created_folder = []

# install cmd "pip3 install adafruit-ampy"
uploader = "ampy"
port = "/dev/ttyACM0"
config_bkp_file = "config_bkp.json"


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
    print("\nFlash Time =", current_time)
    return current_time


def update_flash_time_to_config():
    shutil.copyfile(os.path.join(path, "config.json"), os.path.join(path, config_bkp_file))
    with open(os.path.join(path, "config.json"), 'r') as file:
        json_data = json.loads(file.read())

    json_data["build_time"] = get_current_time()
    config = open(os.path.join(path, "config.json"), 'w')
    config.write(json.dumps(json_data, indent=4))
    config.close()


def restore_config_file():
    if os.path.exists(os.path.join(path, config_bkp_file)):
        shutil.copyfile(os.path.join(path, config_bkp_file), os.path.join(path, "config.json"))
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


def clean_target():
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
    global created_folder
    dir_list = dest_dir.split("/")
    current_dir = "/"
    for d in dir_list:
        current_dir = os.path.join(current_dir, d)
        if current_dir.replace(path, "") == "/":
            # skipping the base path
            continue
        if current_dir not in created_folder:
            actual_dir = current_dir.replace("/"+path, "").strip()
            exitcode , output = run_cmd([uploader, "--port", port, "mkdir", actual_dir])
            if exitcode == EXIT_CODE_SUCCESS:
                print("Create Folder : ", actual_dir)
                created_folder.append(current_dir)
            else:
                print("ERROR: Not albe to Create : ", actual_dir)
                return exitcode

    return EXIT_CODE_SUCCESS


def create_new_file(dest_file):
    actual_file = dest_file.replace(path, "").strip()
    exitcode , output = run_cmd([uploader, "--port", port, "put", dest_file, actual_file])
    if exitcode == EXIT_CODE_SUCCESS:
        print("Send File     : ", actual_file)
    else:
        print("ERROR: Not albe to Send : ", actual_file)
        return exitcode

    return EXIT_CODE_SUCCESS


def upload_firmware():
    for root, directories, files in os.walk(path, topdown=False):
        for name in directories:
            exitcode = create_new_folder(os.path.join(root, name))
            if exitcode != EXIT_CODE_SUCCESS:
                return exitcode
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            if name == config_bkp_file:
                continue
            exitcode = create_new_file(os.path.join(root, name))
            if exitcode != EXIT_CODE_SUCCESS:
                return exitcode

    return EXIT_CODE_SUCCESS



if __name__ == "__main__":
    print("\n\t\t:Digital IC Checking:\n\tFirmware Upload will start shortly\n")
    if not os.path.exists(port):
        print("ERROR:", port, "not available")
        exit(0)
    print("Removeing old files from Hardware...")
    if clean_target() != EXIT_CODE_SUCCESS:
        exit(0)
    update_flash_time_to_config()
    print("\nUploading new files to Hardware...")
    if upload_firmware() != EXIT_CODE_SUCCESS:
        exit(0)
    restore_config_file()
    print("\n\nFirmware Uploaded Succesfully Please restart the hardware once.\n")
