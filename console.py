#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import bluetooth._bluetooth as bluez
import struct

OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_ENABLE=0x000C
LE_META_EVENT = 0x3e

def packed_bdaddr_to_string(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(socket):
    cmd_pkt = struct.pack("<BB",1,0)
    bluez.hci_send_cmd(socket, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def parse_rssi(socket):
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    socket.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)
    myFullList = []

    pkt = socket.recv(255)
    event, = struct.unpack("B", pkt[1:2])

    if event == LE_META_EVENT:
        pkt = pkt[4:]
        mac = packed_bdaddr_to_string(pkt[3:9])
        MAC_ADDRESS = "d6:24:b0:e9:15:ea" #różowy

        if(mac == MAC_ADDRESS):
            Adstring = "%i" % struct.unpack("b", pkt[len(pkt)-1:len(pkt)])
            myFullList.append(Adstring)

    return myFullList

try:
    sock = bluez.hci_open_dev(0)

except:
    print ("Bład podczas uzyskiwania dostepu do urzadzenia bluetooth")
    sys.exit(1)

hci_enable_le_scan(sock)

i = 1

while True:
    returnedList = parse_rssi(sock)
    for beacon in returnedList:
        print (i, beacon)
        i += 1
#test