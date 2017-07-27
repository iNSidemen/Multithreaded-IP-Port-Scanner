#!/usr/bin/python3
import socket, threading, subprocess, json, codecs, sys, os
from datetime import datetime
from urllib.request import urlopen

activeIP = []
for i in range(240,243):
    for x in range(1,254):
        activeIP.append("192.168." + str(i) + "." + str(x))

endout = []

# Initialize Sockets
def TCPconnect (ip, portNum, delay, output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(delay)
    try:
        sock.connect((ip, portNum))
        output[portNum] = 'Listening'
    except:
        output[portNum] = ''


def portscan(hostIP, delay):
    threads = []
    output = {}
    for i in range(1025):
        t = threading.Thread(target=TCPconnect, args=(hostIP, i, delay, output))
        threads.append(t)

    for i in range(1025):
        threads[i].start()

    for i in range(1025):
        threads[i].join()

    for i in range(1025):
        if output[i] == 'Listening':
            collect(hostIP, i, output[i])

def collect(ipp, port, out):
    if ipp not in endout:
        endout.append("[" + ipp + "] Active")
    endout.append("     " + str(port) + ": " + out)

def main():
    # Clear Screen
    subprocess.call('clear', shell=True)

    # Obtain External IP If needed
    currentIP = json.loads(urlopen("http://ip.jsontest.com/").read().decode('utf-8'))
    currentIP = currentIP["ip"]

    # Begin Scan
    delay = float(input("Enter time (in seconds) for socket timeout: "))
    print("Scanning IP range [192.168.x.x] - " + str(datetime.now()))
    for i in activeIP:
        portscan(i, delay)
    print(endout)


if __name__ == '__main__':
    main()
