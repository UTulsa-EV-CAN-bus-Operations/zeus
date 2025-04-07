import can
can.rc['interface'] = 'pcan'
can.rc['channel'] = 'PCAN_USBBUS1'
can.rc['bitrate'] = 500000
from can.interface import Bus

import time
import termcolor
from termcolor import colored
                           
# Initialization of PCAN bus
try:
    peak_bus = Bus()
except can.CanError as e:
    print(colored(("CAN bus initialization error: " + str(e)),"blue"))
    exit()





