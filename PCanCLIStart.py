import can
import time
can.rc['interface'] = 'pcan'
can.rc['channel'] = 'PCAN_USBBUS1'
can.rc['bitrate'] = 500000
from can.interface import Bus
import click
from colorama import Fore