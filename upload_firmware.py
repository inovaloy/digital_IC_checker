import os
import subprocess

path = 'firmware'

EXIT_CODE_SUCCESS = 0
created_folder = []

# install cmd "pip3 install adafruit-ampy"
uploader = "ampy"
port = "/dev/ttyACM0"


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
    print("\nUploading new files to Hardware...")
    if upload_firmware() != EXIT_CODE_SUCCESS:
        exit(0)
    print("\n\nFirmware Uploaded Succesfully Please restart the hardware once.\n")
