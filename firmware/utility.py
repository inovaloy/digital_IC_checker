import os
import json
from cryptolib import aes
import binascii

def isFile(path):
    mode = os.stat(path)[0]
    if mode & 0x8000:  # Regular file
        return True
    return False


def isFolder(path):
    mode = os.stat(path)[0]
    if mode & 0x4000:  # Directory
            return True
    return False


def get_config_data():
    config_data = None
    try:
        with open("config.json", 'r') as file:
            config_data = json.loads(file.read())
    except:
        pass
    return config_data


def update_config_data(data):
    with open("config.json", 'w') as file:
        file.write(json.dumps(data))


def init_user_config_data():
    config_data = get_config_data()
    if config_data != None:
        if config_data.get("user_data") == None:
            config_data["user_data"] = {}
        update_config_data(config_data)


def get_user_config_data():
    user_config_data = None
    config_data = get_config_data()
    if config_data != None:
        user_config_data = config_data.get("user_data")
        if user_config_data == None:
            init_user_config_data()
            user_config_data = {}
    
    return user_config_data


def update_user_config_data(data):
    config_data = get_config_data()
    if config_data == None:
        config_data = {}
    config_data["user_data"] = data
    update_config_data(config_data)


def get_machine_name():
    return os.uname()[-1]


def txt_padding(txt, pad_size, center, l_offset):
    txt_len = len(str(txt))
    space = pad_size - txt_len - 4
    if center:
        l_space = space//2
        r_space = space - l_space
        return "##" + " "*l_space + str(txt) + " "*r_space + "##"
    else:
        r_space = space - l_offset
        return "##" + " "*l_offset + str(txt) + " "*r_space + "##"


# Helper function for padding
def pad(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    return data + chr(padding_length) * padding_length

# Helper function for unpadding
def unpad(data):
    padding_length = ord(data[-1])
    return data[:-padding_length]

def base64_encode(data):
    return binascii.b2a_base64(data).decode('utf-8').strip()

# Simple base64 decoding
def base64_decode(data):
    return binascii.a2b_base64(data.encode('utf-8'))

# Encrypt function
def get_encrypted_password(data):
    cipher = aes(pad(get_machine_name()), 1)  # Mode 1 = ECB
    data = pad(data)  # Add padding
    encrypted = b""
    for i in range(0, len(data), 16):
        block = data[i:i + 16]
        encrypted += cipher.encrypt(block)
    return base64_encode(encrypted)

# Decrypt function
def get_decrypted_password(encrypted):
    encrypted = base64_decode(encrypted)
    cipher = aes(pad(get_machine_name()), 1)  # Mode 1 = ECB
    decrypted = ""
    for i in range(0, len(encrypted), 16):
        block = encrypted[i:i + 16]
        decrypted += cipher.decrypt(block).decode()
    return unpad(decrypted)  # Remove padding
