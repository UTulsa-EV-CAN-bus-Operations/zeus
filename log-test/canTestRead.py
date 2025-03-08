import can 
from can import TRCReader

import os
import re
import xlsxwriter

### This can open the raw .trc file and print it out. 
#file = open("Charging - Ignition Off.trc")
#print(file.read())

###### Get all messages with a specific id value ######
###### Returns list of messages
def getAllMessages(fileReader):
    messageList = []
    for msg in fileReader:
        messageList.append(msg)
    
    return messageList

def getMessagesById(packetList, id):
    messageList = []
    for packet in packetList:
        if (re.search(str(id), str(packet)) != None):
            messageList.append(packet)

    return messageList


###### Grab bytearrays of data from messages ######
def getByteData(fileReader):
    data = []
    for line in fileReader:
        data.append(line.data)
    
    return data

def getData(packetList):
    data = []
    for packet in packetList:
        # substring 
        data.append(packet)

###### Highlights/bold any message that isn't the 
###### initial state of some id group of messages

#def highlightDiff(fileReader):


###### Export to excel file
#def exportMessages(fileReader):



###### Get packets of transmitted
def getTransmittedPackets(packetList):
    transmitted = []
    for msg in packetList:
        if(not msg.is_rx):
            transmitted.append(msg)
    
    return transmitted


###### Get packets of received
def getReceptionPackets(packetList):
    received = []
    for msg in packetList:
        if(msg.is_rx):
            received.append(msg)
    
    return received


reader = TRCReader("Charging - Ignition Off.trc")


packetList = getAllMessages(reader)

#for msg in getMessagesById(packetList, 167):
#    print(msg)

print(str(packetList[0]))

workbook = xlsxwriter.Workbook('Output.xlsx')
sheet = workbook.add_worksheet()

row = 0
for msg in getMessagesById(packetList,167):
    sheet.write(row,0,str(msg))
    row+=1

workbook.close()
