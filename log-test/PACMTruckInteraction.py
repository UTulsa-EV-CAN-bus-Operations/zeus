import can
import time
import datetime
from can import LogReader, MessageSync

#bus1 = can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000, receive_own_messages=True)
bus2 = can.interface.Bus(channel='PCAN_USBBUS2', interface='pcan', bitrate=500000, receive_own_messages=True)

print_listener = can.Printer()

# Instatiate logger to log received messages to timestamped file
filename = 'TESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger1 = can.Logger(filename)
filename = 'TESTlog2PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
logger2 = can.Logger(filename)

#notifier1 = can.Notifier(bus1, [logger1])
notifier2 = can.Notifier(bus2, [logger2])

def replayTrace(bus, filename):
    reader = LogReader(filename)
    for msg in MessageSync(messages=reader):
        try:
            if msg.is_error_frame == False:
                print(msg)
                bus.send(msg)

        except KeyboardInterrupt:
            pass


# Define trace to replay and then replay it
traceFile = "truckTESTlog1PACM-2025-04-10_20-54-09.trc"
replayTrace(bus2, traceFile)

time.sleep(1.0)

# Close/shutdown notifiers and buses
print("Shutting down...")
#notifier1.stop()
notifier2.stop()
#bus1.shutdown()
bus2.shutdown()