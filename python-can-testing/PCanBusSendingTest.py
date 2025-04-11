import can
from can import Message
import time
can.rc['interface'] = 'pcan'
can.rc['channel'] = 'PCAN_USBBUS1'
can.rc['bitrate'] = 500000
from can.interface import Bus

bus = Bus()

test = can.Message(
        arbitration_id=0xC0F,
        data=[0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77],
        is_extended_id=True
    )

bus.send(test)

bus.shutdown()