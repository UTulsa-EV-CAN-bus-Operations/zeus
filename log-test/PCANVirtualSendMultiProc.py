import can
import time
import datetime
from multiprocessing import Process, Lock, Queue
from colorama import Fore

def sendMessages(channel='PCAN_USBBUS1', interface='pcan', bitrate=500000, receive_own_messages = True, fileName = "ForgotToNameFile.trc", inQueue : Queue = [], outQueue : Queue = []):
    bus = can.interface.Bus(channel=channel, interface=interface, bitrate=bitrate, receive_own_messages = receive_own_messages)
    print_listener = can.Printer()

    # Instatiate logger to log received messages to timestamped file
    logger = can.Logger(fileName)

    BufferedReader = can.BufferedReader()

    notifier1 = can.Notifier(bus, [print_listener,logger, BufferedReader])

    while True:
        msg = BufferedReader.get_message()
        outQueue.put(msg)
        while not inQueue.empty():
            #self.busLock.acquire()
            msgToSend = inQueue.get()
            print(f"{Fore.GREEN} Sending: {msgToSend}{Fore.RESET}")
            bus.send(msg=msgToSend)

SharedDataLtR = Queue()
SharedDataRtL = Queue()

sendProcess1 = Process(target=sendMessages, kwargs = {
    'channel' : 'PCAN_USBBUS1',
    'interface' :'pcan',
    'bitrate' : 500000,
    'receive_own_messages' : True, 
    'fileName' : './PassThroughTest/TruckOnlyMultiProcTestLeft-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now()),
    'inQueue' :  SharedDataLtR,
    'outQueue' : SharedDataRtL
}, daemon=True)


sendProcess2 = Process(target=sendMessages, kwargs = {
    'channel' : 'PCAN_USBBUS2',
    'interface' :'pcan',
    'bitrate' : 500000,
    'receive_own_messages' : True, 
    'fileName' : './PassThroughTest/TruckOnlyMultiProcTestRight-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now()),
    'inQueue' :  SharedDataRtL,
    'outQueue' : SharedDataLtR
}, daemon=True)


if __name__ == '__main__':
    try:
        sendProcess1.start()
        sendProcess2.start()

        while True:
            pass

    except KeyboardInterrupt:
        pass

    # Close/shutdown notifiers and buses
    print("Shutting down...")
    #notifier1.stop()
    #notifier2.stop()
    #bus1.shutdown()
    #bus2.shutdown()