"""
Find-Notconnected-Interfaces-In-Old-VLANs

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
#from UsefulFunctions import validate_ip
import textfsm

from pprint import pprint

username = getpass.getuser()
userPassword = getpass.getpass()

outputFileName = 'c:/Users/' + username + '/Desktop/Find-Multiple-MACs-Output.txt'

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
    print('THIS IS THE CONFIGURATION FOR')
    print(hostname)
    print(ipAddress)
    print('------------------------------------')
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
    productionAccessSwitchList = getSwitchIps(switchTextFileName)

    scriptHeader()

main()