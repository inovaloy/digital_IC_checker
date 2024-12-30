import network
import time
import socket


def get_all_wifi():
    print("Scanning for Wi-Fi networks...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    all_wifi = []
    for _network in networks:
        ssid = _network[0].decode('utf-8')
        all_wifi.append(ssid)

    return all_wifi


def wifi_setup(ssid, password):
    print("Connecting to WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    timeout = 10

    while not wlan.isconnected():
        time.sleep(1)
        timeout -= 1
        if timeout == 0:
            print("Connection failed!")
            return False, None

    print("Connected to WiFi!")
    print("IP Address:", wlan.ifconfig()[0])

    return True, wlan.ifconfig()[0]


def get_wifi_ip():
    wlan = network.WLAN(network.STA_IF)
    return wlan.ifconfig()[0]


def setup2():

    # Create a socket and bind to IP and port 80
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)

    return s


def main():
    s = setup2()

    f = open('web/index.html')
    html = f.read()
    f.close()
    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        print("Request:", request)

        # Send HTTP response
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
