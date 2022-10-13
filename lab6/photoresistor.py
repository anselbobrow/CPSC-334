#!/usr/bin/env python
import socket

UDP_IP = "172.29.31.240"
UDP_PORT = 5070

sock = socket.socket(
    socket.AF_INET,  # Internet
    socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print(data.decode("ASCII"))
