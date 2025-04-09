import can
import time
import datetime

# Instantiate virtual buses on same channel for communication
bus1 = can.interface.Bus('test', interface='virtual', bitrate=500000)
bus2 = can.interface.Bus('test', interface='virtual', bitrate=500000)

# Instantiate a printer to print received messages
print_listener = can.Printer()

# Instatiate logger to log received messages to timestamped file
filename = 'log-{date:%Y-%m-%d_%H:%M:%S}.trc'.format(date=datetime.datetime.now())
logger = can.Logger(filename)

# Instantiate notifier with specified bus and listeners
notifier1 = can.Notifier(bus1, [print_listener,logger])
notifier2 = can.Notifier(bus2,[print_listener,logger])

# Send messages from a specified bus with an id in the first 
def sendMessageChain(bus, id):
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[ id, i, 1, 3, 1, 4, 1], is_extended_id=True)
        bus.send(msg)

sendMessageChain(bus1,1)
sendMessageChain(bus2,2)

# Ensure all messages are logged
time.sleep(1.0)

# Close/shutdown notifiers and buses
print("Shutting down...")
notifier1.stop()
notifier2.stop()
bus1.shutdown()
bus2.shutdown()