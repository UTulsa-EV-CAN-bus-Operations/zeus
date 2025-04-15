import can
import time
import datetime
from can import LogReader, MessageSync

bus1 = can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000, receive_own_messages=True)

print_listener = can.Printer()

# Instatiate logger to log received messages to timestamped file
filename = 'ReplayTESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger = can.Logger(filename)

notifier1 = can.Notifier(bus1, [logger])

def replayTrace(bus, filename):
    reader = LogReader(filename)
    for msg in MessageSync(messages=reader):
        try:
            if msg.is_error_frame == False:
                print(msg)
                bus.send(msg)

        except KeyboardInterrupt:
            pass

traceFile = "reverse-isolated.trc"
replayTrace(bus1, traceFile)
time.sleep(1.0)

# Close/shutdown notifiers and buses
print("Shutting down...")
notifier1.stop()
bus1.shutdown()