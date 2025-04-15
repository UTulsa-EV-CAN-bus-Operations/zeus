import can
import time
import datetime
from threading import Thread

# Instantiate virtual buses on same channel for communication
bus1 = can.interface.Bus(channel='test', interface='virtual', bitrate=500000, receive_own_messages = True)
bus2 = can.interface.Bus(channel='test', interface='virtual', bitrate=500000, receive_own_messages = True)

#bus1 = can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000)
#bus2 = can.interface.Bus(channel='PCAN_USBBUS2', interface='pcan', bitrate=500000)

# Instantiate a printer to print received messages
print_listener = can.Printer()

# Instatiate logger to log received messages to timestamped file
filename = 'TESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger = can.Logger(filename)
filename2 = 'TESTlog2PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger2 = can.Logger(filename2)

BufferedReader = can.BufferedReader()
BufferedReader2 = can.BufferedReader()

RedirectReader = can.RedirectReader(bus2)
RedirectReader2 = can.RedirectReader(bus1)

# Instantiate notifier with specified bus and listeners
notifier1 = can.Notifier(bus1, [print_listener,logger, BufferedReader])
notifier2 = can.Notifier(bus2,[print_listener,logger2, BufferedReader2,RedirectReader2])

# Send messages from a specified bus with an id in the first 
def sendMessageChain(bus, id):
    for i in range(5):
        msg = can.Message(arbitration_id=0xc0ffee, data=[ id, i, 1, 3, 1, 4, 1], is_extended_id=True)
        bus.send(msg)

#sendMessageChain(bus1,1)
#sendMessageChain(bus2,2)

def sendMessages(BufferedReader, bus):
    while True:
        msg = BufferedReader.get_message()
        #bus.send(msg)

#sendThread1 = Thread(target= sendMessages, args=(BufferedReader, bus1), daemon=True)
#sendThread2 = Thread(target= sendMessages, args=(BufferedReader2, bus2), daemon=True)


"""startTime = time.time()
while True:
    currTime = time.time()

    if(currTime > startTime+30):
        break"""
#try:
#    sendThread1.start()
#    sendThread2.start()
#
#    while True:
#        pass
#except KeyboardInterrupt:
#    pass

#sendMessageChain(bus1, 1)
msg = can.Message(arbitration_id=0xc0ffee, data=[ 2, 1, 3, 1, 4, 1], is_extended_id=True)
bus1.send(msg)

RedirectReader2.stop()


# Ensure all messages are logged
time.sleep(1.0)

# Close/shutdown notifiers and buses
print("Shutting down...")
notifier1.stop()
notifier2.stop()
bus1.shutdown()
bus2.shutdown()