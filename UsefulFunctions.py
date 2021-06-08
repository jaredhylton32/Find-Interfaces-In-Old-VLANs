"""
Useful Functions
Jared Hylton
"""

import sys
import argparse
import tcl
#from IPy import IP
from pprint import pprint
import ipaddress
import time
import cli

### Validates whether a string is a valid IP or not
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
"""
### Gets the list of VLAN IDs and names for all VLANS in the 'show vlan' command
def getVlanNameAndNumber(): ### show vlan
    for line in showVlan.splitlines():
        # Skip certain lines
            if "VLAN" in line or "-----" in line or line.startswith("  "):
                continue
            fields = line.split()
            vlanID = fields[0]
            vlanName = fields[1]
            vlanList.append((vlanID, vlanName))
"""
def getVlanNameAndNumber(showVlanBrief):
    vlanList = []
    vlanNumbersOnlyList = []
    vlanNumberVlanNameDict = {}
    defaultVlans = ['1002', '1003', '1004', '1005']
    for line in showVlanBrief.splitlines():
        #print(line)
        # Skip certain lines
        line = line.strip(r'\n')
        if len(line) == 0:
            continue
        lineSplit = line.split()
        #print(lineSplit)
        if str(lineSplit[0]).isdigit():
            vlanID = lineSplit[0]
            vlanName = lineSplit[1]
            if int(vlanID) < 4096 and int(vlanID) > 1 and vlanID not in defaultVlans:
                print('vlan', vlanID)
                print('name', vlanName)
                print('exit')
                printEmptyLines(1)
                vlanList.append((vlanID, vlanName))
                vlanNumbersOnlyList.append(vlanID)
    #print(vlanNumbersOnlyList)
    #print(vlanList)
    return vlanList

### Takes the MAC address format of aaaa.bbbb.cccc and formats it as AA:BB:CC:DD:EE:FF
def formatMacAddresses(): ### show ip arp
    macAddress = []

    for line in arpFile:
        if line.startswith('Protocol '):
            continue
        lineList = line.split()
        macAddress.append(lineList[3])
        #pprint(macAddress)

    pprint(macAddress)

    macSection1 = ('')
    macSection2 = ('')
    macSection3 = ('')

    for line in macAddress:
        newLine = line.split('.')
        macSection1 = newLine[0]
        macSection2 = newLine[1]
        macSection3 = newLine[2]
        fullMac = (macSection1 + macSection2 + macSection3)
        fullMac = fullMac.upper()
        formattedMac = fullMac[:2] + ':' + fullMac[2:]
        formattedMac = formattedMac[:5] + ':' + fullMac[4:]
        formattedMac = formattedMac[:8] + ':' + fullMac[6:]
        formattedMac = formattedMac[:11] + ':' + fullMac[8:]
        formattedMac = formattedMac[:14] + ':' + fullMac[10:]
        print(formattedMac)

### Gets the BGP peer AS number and peer IP number
def getBgpPeerInfo(): ### show bgp summary
    bgpSumm = bgpSumm.splitlines()

    firstLine = bgpSumm[0]
    asNumber = firstLine.split()
    asNumber = asNumber[-1]
    print('The AS number is: ',asNumber)

    lastLine = bgpSumm[-1]
    peer = lastLine.split()[0]
    print('The peer IP is: ',peer)


### After returning 'show run interface g1/0/42' command, prints the description of that interface
### Can be modified to pull a different lines information or check for a certain command like portfast
def printInterfaceDescription():
    ### Create empty string variable
    interfaceDescription = ''
    for line in splitShowRunInterface:
        ### Find the description line
        if line.startswith(' description '):
            ### Split line by whitespace
            splitLine = line.split()
            ### Remove the first element which is 'description'
            splitLine.pop(0)
            ### Add each element of the tuple together, separated with a space
            for i in splitLine:
                interfaceDescription = interfaceDescription + ' ' + i
            print(interfaceDescription)
