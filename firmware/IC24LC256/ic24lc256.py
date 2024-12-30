from machine import Pin, SoftI2C
from dicc import *
from IC24LC256.ic24lc256_pin import *
import time
import random


def metadata():
    ic_pin_count  = IC_8_PIN
    ic_brief_name = "256Kbits EEPROM IC"

    return ic_pin_count, ic_brief_name


def zfill(data, size, char="0"):
    data = str(data)
    if len(data) < size:
        return char*(size-len(data))+data

    return data


def eeprom_read(i2c, i2c_addr, addr, nbytes):
    """Read one or more bytes from the EEPROM starting from a specific address"""
    return i2c.readfrom_mem(i2c_addr, addr, nbytes, addrsize=16)


def eeprom_write(i2c, i2c_addr, addr, buf):
    #
    # Memory Size: 256 Kbits => 32 KBytes
    # Bytes per Page (BPP) => 32
    # Page number: 1024
    #

    BPP  = 32
    PAGE = 1024

    """Write one or more bytes to the EEPROM starting from a specific address"""

    offset = addr % BPP
    partial = 0
    # partial page write
    if offset > 0:
        partial = BPP - offset
        i2c.writeto_mem(i2c_addr, addr, buf[0:partial], addrsize=16)
        time.sleep_ms(5)
        addr += partial
    # full page write
    for i in range(partial, len(buf), BPP):
        i2c.writeto_mem(i2c_addr, addr+i-partial, buf[i:i+BPP], addrsize=16)
        time.sleep_ms(5)


def main():
    #
    # Memory Size: 256 Kbits => 32 KBytes
    # Bytes per Page (BPP) => 32
    # Page number: 1024
    #

    BPP  = 32
    PAGE = 1024

    fail_counter = 0
    i2c_add_dict = {
        "address_list" :
        [
            {
                "address_line" : [0, 0, 0],
                "address"      : 80
            },
            {
                "address_line" : [0, 0, 1],
                "address"      : 84
            },
            {
                "address_line" : [0, 1, 0],
                "address"      : 82
            },
            {
                "address_line" : [0, 1, 1],
                "address"      : 86
            },
            {
                "address_line" : [1, 0, 0],
                "address"      : 81
            },
            {
                "address_line" : [1, 0, 1],
                "address"      : 85
            },
            {
                "address_line" : [1, 1, 0],
                "address"      : 83
            },
            {
                "address_line" : [1, 1, 1],
                "address"      : 87
            }
        ]
    }

    i2c_address_0 = Pin(PIN_A0_IN_1, Pin.OUT)
    i2c_address_1 = Pin(PIN_A1_IN_2, Pin.OUT)
    i2c_address_2 = Pin(PIN_A2_IN_3, Pin.OUT)

    write_protect = Pin(PIN_WP_IN, Pin.OUT)


    write_protect.value(LOW)

    i2c = SoftI2C(scl=Pin(PIN_SCL_IN, Pin.IN, Pin.PULL_UP), sda=Pin(PIN_SDA_IN, Pin.IN, Pin.PULL_UP))
    i2c_address = 0

    # Address Test
    for address_node in i2c_add_dict["address_list"]:
        print("Test for address line ", address_node["address_line"], end="")
        i2c_address_0.value(address_node["address_line"][0])
        i2c_address_1.value(address_node["address_line"][1])
        i2c_address_2.value(address_node["address_line"][2])
        i2c_devices = i2c.scan()
        if len(i2c_devices) > 0:
            if i2c_devices[0] == address_node["address"]:
                print(": PASS")
                i2c_address = i2c_devices[0]
            else:
                print(": FAIL")
                fail_counter += 1
                i2c_address = 0
        else:
            print(": FAIL")
            fail_counter += 1
            i2c_address = 0
        time.sleep(0.5)

    # Read Test
    if i2c_address:
        test_number = 100
        print("\n")
        for counter in range(1, test_number+1):
            print("Random Data Read/Write Test "+zfill(counter, 3, " ")+"/"+str(test_number), end=": ")
            salt = "ABCDEFGHIJKLMNOPQRSTUVWNYZabcdefghijklmnopqrstuvwnyz0123456789"
            data = ""
            for _ in range(random.randint(0, 1024)):
                index = random.randint(0, len(salt)-1)
                data += salt[index]

            data_write_address = random.randint(0, (BPP*PAGE) - len(data))

            print("Address:", zfill(data_write_address, 5, " "), end=", ")
            print("Read/Write:", zfill(len(data),4, " "), "Byte(s)", end=", ")
            eeprom_write(i2c, i2c_address, data_write_address, data)
            read_data = eeprom_read(i2c, i2c_address, data_write_address, len(data))
            if read_data.decode() == data:
                print("PASS")
            else:
                print("FAIL")
                print("    Write on Address :", data_write_address)
                print("    Data             :", data)
                print("    Read from Address:", read_data.decode())
                fail_counter += 1
    else:
        print("i2c Address not Found")
        fail_counter += 1


    if fail_counter:
        return RETURN_ERROR
    else:
        return RETURN_SUCCESS
