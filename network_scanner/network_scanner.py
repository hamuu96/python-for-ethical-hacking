#!/usr/bin/python3
import scapy.all as scapy
import optparse
import argparse
def scan(ip):
    
    # creating an instance of the class arp
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast / arp_request  
    # The show commands dont work in python 3  but you are able to send and receive packets \
    # This is used to list the fields in the arp packet and broadcast
    # arp_request.show()
    # broadcast.show()
    # arp_broadcast.show()   
    answered= scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    #the answered request consists of two lists request and result
    
    result = []
    for x in answered:
        result_dict = {'ip': x[1].psrc ,'mac':x[1].hwsrc}
        result.append(result_dict)
    return result  

#function is iterating through the result and printing 
def printing(result_scan):
    print('IP\t\t\tMac address')
    print('------------------------------------------') 

    for element in result_scan:
        print(element['ip'] + '\t\t'+ element['mac'])

def scan_arguments():
    #create an instance of Argumentparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--target', dest='ip', help='This allows you to choose an ip range')
    args = parser.parse_args()

    if not args.ip:
        parser.error('[-] please specify an ip address and range')
    else:
        return args


args = scan_arguments()

scan_result = scan(args.ip)
printing(scan_result)