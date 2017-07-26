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

def portscan(ips, delay, time):
    for hostIP in ips:
        print("Port Scan: " + hostIP + "[" + str(time) + "]")
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
                print("     " + str(i) + ": " + output[i])

def ipscan(scanip, delay, time):
    ipsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipsock.settimeout(delay)
    scanip = (".".join(scanip.split('.')[0:-1]) + '.')
    print(str(time) + " - Scanning [" + scanip + "x] subnet for living hosts..")
    for i in range(1,254):
        try:
            ip = scanip + str(i)
            socket.gethostbyaddr(ip)
            activeIP.append(ip)
        except socket.herror as ex:
            pass
    print("Active IP's:")
    for i in activeIP:
        print(i)
    prompt = input("Continue with scan? (Y/N): ")
    if prompt == "Y" or "y":
        portscan(activeIP, delay, time)
    else:
        sys.exit()


def main():
    # Clear Screen
    subprocess.call('clear', shell=True)

    # Obtain External IP
    currentIP = json.loads(urlopen("http://ip.jsontest.com/").read().decode('utf-8'))
    currentIP = currentIP["ip"]
    activeIP.append(currentIP)

    # Begin Scan
    delay = int(input("Enter time (in seconds) for socket timeout: "))
    t1 = datetime.now()
    ipscan(currentIP, delay, t1)

if __name__ == '__main__':
    main()
