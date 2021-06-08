"""
Find-Interfaces-In-Old-VLANs

This script allows you to enter an old VLAN that you want to get rid of (such as VLAN 1)
And then returns all interfaces that are currently up and down in that VLAN

To get getpass() to work:
1. 'Run'
2. 'Edit Configurations'
3. Check 'Emulate terminal in output console'
4. Apply

Jared Hylton
"""

from datetime import datetime
from netmiko import ConnectHandler
import getpass
import sys
from UsefulFunctions import validate_ip
import textfsm

from pprint import pprint

username = getpass.getuser()
userPassword = getpass.getpass()
oldVlanNumber = input('Enter in a single old VLAN number: ')
#oldVlanNumber = "1"


outputFileName = 'c:/Users/' + username + '/Desktop/Find-Notconnected-Interfaces-In-Old-VLANs.txt'

print(username)
print('ALL SCRIPT OUTPUT WILL BE PLACED AT ' + outputFileName)
print('------------------------------------')
print('THIS SCRIPT IS NOW RUNNING. PLEASE BE PATIENT. THIS CAN TAKE UP TO 1 MINUTE PER SWITCH')
print('------------------------------------')

### Template for Netmiko
cisco = {
    'device_type': 'cisco_ios',
    'host': '1.1.1.1',
    'username': username,
    'password': userPassword
    #'secret': 'mysecret'
 }

switchTextFileName = 'switches'

def getSwitchIps(switchTextFileName):
    switchTextFileName = str(switchTextFileName)
    if switchTextFileName.endswith('.txt'):
        pass
    else:
        switchTextFileName = switchTextFileName + '.txt'
    switchTextFileName = 'c:/Users/' + username + '/Desktop/' + switchTextFileName
    print('Attempting to access', switchTextFileName)
    with open(switchTextFileName) as switchTextFileName_in:
        listOfSwitches = switchTextFileName_in.read()
        listOfSwitches = listOfSwitches.split()

        for i in listOfSwitches:
            if validate_ip(i) == False:
                sys.exit('AN ERROR HAS OCCURRED. THE TEXT FILE PROVIDED DOES NOT ONLY CONTAIN IP ADDRESSES '
                      'PLEASE CONFIRM THERE ARE NO ERRORS IN THE FILE')

    #print(listOfSwitches)
    return listOfSwitches

def sshToSwitch(ipAddress):
    #cisco_ios_show_interfaces_status.textfsm
    cisco['host'] = ipAddress
    net_connect = ConnectHandler(**cisco)

    showIntStatus = net_connect.send_command("show interfaces status", use_textfsm=True)
    hostname = net_connect.send_command("show run | inc hostname", use_textfsm=True)
    #pprint(showIntStatus)

    return showIntStatus, hostname

def getInterfacesInOldVlan(showIntStatus, oldVlanNumber):
    listOfDownedInterfacesInOldVlan = []
    listOfUpInterfacesInOldVlan = []

    for interface in showIntStatus:
        physicalInterface = interface.__getitem__('port')
        vlanNumber = interface.__getitem__('vlan')
        status = interface.__getitem__('status')
        if vlanNumber == oldVlanNumber:
            if status == 'notconnect':
                listOfDownedInterfacesInOldVlan.append(physicalInterface)
            if status == 'connected':
                listOfUpInterfacesInOldVlan.append(physicalInterface)

    return listOfDownedInterfacesInOldVlan, listOfUpInterfacesInOldVlan

def printLists(listOfDownedInterfacesInOldVlan, listOfUpInterfacesInOldVlan, oldVlanNumber):
    print('ACCESS INTERFACES IN VLAN', oldVlanNumber, 'THAT ARE NOTCONNECT')
    for interface in listOfDownedInterfacesInOldVlan:
        print(interface)
    #print(listOfDownedInterfacesInOldVlan)
    print('-' * 25)
    print('ACCESS INTERFACES IN VLAN', oldVlanNumber, 'THAT ARE CONNECTED')
    for interface in listOfUpInterfacesInOldVlan:
        print(interface)
    print('-' * 25)

def scriptToShutDownedInterfaces(listOfDownedInterfacesInOldVlan):
    if len(listOfDownedInterfacesInOldVlan) > 0:
        printEmptyLines(1)
        print('SCRIPT TO SHUTDOWN DOWNED INTERFACES')
        printEmptyLines(1)
        print('conf t')
        for interface in listOfDownedInterfacesInOldVlan:
            print('interface', interface)
            print('shutdown')
            print('description SHUTDOWN BY PYTHON SCRIPT')
            print('exit')
            printEmptyLines(1)

def scriptHeader():
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    print('------------------------------------')
    print('PLEASE CONTACT JARED HYLTON WITH ANY ISSUES OR RECOMMENDATIONS')
    print('------------------------------------')
    print('THIS SCRIPT WAS RUN AT', timestamp, 'by', username)
    print('------------------------------------')
    printEmptyLines(1)

def scriptEnding():
    timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    print('------------------------------------')
    print('------------------------------------')
    print('THIS SCRIPT ENDED AT', timestamp)
    print('------------------------------------')
    print('------------------------------------')


def headerForEachSwitch(ipAddress, hostname):
    print('------------------------------------')
    print('------------------------------------')
    print('THIS IS THE OUTPUT FOR')
    print(hostname)
    print(ipAddress)

    print('------------------------------------')
    printEmptyLines(1)

def endingForEachSwitch():
    print('------------------------------------')
    print('------------------------------------')
    printEmptyLines(2)

def printEmptyLines(s):
    i = 0
    while i < s:
        print('')
        i += 1

def main():
    sys.stdout = open(outputFileName, 'w')
    scriptHeader()
    productionAccessSwitchList = getSwitchIps(switchTextFileName)

    for ipAddress in productionAccessSwitchList:
        showIntStatus, hostname = sshToSwitch(ipAddress)
        headerForEachSwitch(ipAddress, hostname)
        listOfDownedInterfacesInOldVlan, listOfUpInterfacesInOldVlan = getInterfacesInOldVlan(showIntStatus, oldVlanNumber)
        printLists(listOfDownedInterfacesInOldVlan, listOfUpInterfacesInOldVlan, oldVlanNumber)
        #scriptToShutDownedInterfaces(listOfDownedInterfacesInOldVlan)
        endingForEachSwitch()

    scriptEnding()

main()