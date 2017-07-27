#!/usr/bin/python3
import socket, threading, subprocess, json, codecs, sys
from datetime import datetime
from urllib.request import urlopen

activeIP = []

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


def portscan(delay2, time):
    for hostIP in activeIP:
        print("Port Scan: " + hostIP + " - [" + str(time) + "]")
        threads = []
        output = {}

        for i in range(1025):
            t = threading.Thread(target=TCPconnect, args=(hostIP, i, delay2, output))
            threads.append(t)

        for i in range(1025):
            threads[i].start()

        for i in range(1025):
            threads[i].join()

        for i in range(1025):
            if output[i] == 'Listening':
                print("     " + str(i) + ": " + output[i])


def ipscan(delay1, time):
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipsock.settimeout(delay1)
    ipsock.connect(("8.8.8.8", 80))
    scanip = (ipsock.getsockname()[0])
    activeIP.append(scanip)
    scanip = (".".join(scanip.split('.')[0:-2]) + '.')
    print(str(time) + " - Scanning [" + scanip + "x.x] subnet  for living hosts..")
    for x in range(240,243):
        for i in range(1,254):
            try:
                ip = scanip + str(x) + "." + str(i)
                socket.gethostbyaddr(ip)
                activeIP.append(ip)
            except socket.herror as ex:
                pass
    print("Active IP's:")
    for i in activeIP:
        print(i)
    prompt = input("Continue with scan? (Y/N): ")
    if prompt == "Y" or "y":
        ipsock.close()
        portscan(delay1, time)
    else:
        sys.exit()


def main():
    # Clear Screen
    subprocess.call('clear', shell=True)

    # Obtain External IP
    currentIP = json.loads(urlopen("http://ip.jsontest.com/").read().decode('utf-8'))
    currentIP = currentIP["ip"]

    # Begin Scan
    delay = int(input("Enter time (in seconds) for socket timeout: "))
    t1 = datetime.now()
    ipscan(delay, t1)


if __name__ == '__main__':
    main()
