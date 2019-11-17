#! /usr/bin/env python3
# function that changes mac addresses

# def mac_changer():
#     subprocess.run('ifconfig' ,shell=True)
#     interface = str(input('interface > '))
#     subprocess.run('ifconfig {} down'.format(interface) ,shell=True)
#     mac = input('choose a mac address you want. e.g 11:22:33:4g:e5:55: ')
#     subprocess.run('ifconfig {}  hw ether {}'.format(interface, mac) ,shell=True)
#     subprocess.run('ifconfig {} up'.format(interface) ,shell=True)
    
#     print('\n \nyour new address is :' + mac)


# mac_changer()


import subprocess
import optparse
import re




def mac_changer(interface, mac):

    subprocess.run(['ifconfig' , interface , 'down'])
    subprocess.run(['ifconfig' , interface ,'hw',  'ether' , mac ])
    subprocess.run(['ifconfig', interface , 'up'])
    
    # print('\n \n[+] your new mac address is :' + mac )



def mac_changer_arguments():

    parse = optparse.OptionParser()

    parse.add_option('-i', '--interface', dest='interface', help='choose an interface ')
    parse.add_option('-m', '--mac', dest='mac', help='choose a new mac address ')
    (option, arguments) = parse.parse_args()

    if not option.interface :
        parse.error('[-] please enter an interface before proceeding --help for more information')
    elif not option.mac :
        parse.error('[-] please enter an mac before proceeding --help for more information')
    else:
        return (option, arguments)



def check_mac(interface):
    result_ifconfig = subprocess.check_output(["ifconfig", interface])
    captured_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(result_ifconfig))

    if not captured_mac:
        print('[-] sorry no mac address was found')
    else:
        return captured_mac.group(0)



(option, arguments) = mac_changer_arguments()

before_change_mac = check_mac(option.interface)
print('[+] previous Mac: ' + before_change_mac)

mac_changer(option.interface , option.mac)
print('[+] Chaning Mac for {} to {}'.format(option.interface, option.mac))

after_change_mac = check_mac(option.interface)


if before_change_mac != after_change_mac:
    print('[+] Mac successfully changed to  ' + after_change_mac)
    
else:
    print('[-] Sorry Mac has not been changed to similarity to original Mac')




