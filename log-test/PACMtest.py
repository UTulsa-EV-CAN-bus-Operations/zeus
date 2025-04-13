import can
import time
import datetime

bus1 = can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000)

print_listener = can.Printer()

# Instatiate logger to log received messages to timestamped file
filename = 'TESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger = can.Logger(filename)

notifier1 = can.Notifier(bus1, [print_listener,logger])

time.sleep(1.0)

while True:
    if input()=='q':
        break

# Close/shutdown notifiers and buses
print("Shutting down...")
notifier1.stop()
bus1.shutdown()