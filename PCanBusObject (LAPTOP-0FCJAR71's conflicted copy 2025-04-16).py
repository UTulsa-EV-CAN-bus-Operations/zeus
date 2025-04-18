import can
import time
from can.interface import Bus
import click
from colorama import Fore
from threading import Thread, Lock
import queue

class PCanBus:
    def __init__(self, interface = 'pcan', channel = 'PCAN_USBBUS1', bitrate = 500000):
        can.rc['interface'] = interface
        can.rc['channel'] = channel
        can.rc['bitrate'] = bitrate

        self.bus = Bus()
        self.BufferedReader = can.BufferedReader()
        self.Notifier = can.Notifier(bus=self.bus, listeners=[self.BufferedReader])

        self.fileWriteLock = Lock()
        #self.busLock - Lock()
    
    def listen(self, fileName = "PCAN_History.txt", DataStore : queue.Queue = queue.Queue):
        """"""
        try:
            while True:
                try:
                    #self.busLock.acquire()
                    msg = self.BufferedReader.get_message()
                    if msg != None:
                        print(f"{Fore.CYAN} Received: {msg}{Fore.RESET}")
                        DataStore.put(msg)
                        with self.fileWriteLock:
                            with open(fileName, mode = 'a') as file:
                                file.write(str(msg) + "\n")
                        time.sleep(0.5)
                    #self.busLock.release()
                    #else:
                    #    pass
                        #file.write("No Data\n")
                        #print("No Data")
                        #if q.empty:
                        #    print("Empty Message Queue")
                        #    time.sleep(1)
                        #else:
                        #    while not q.empty:
                        #        print(q.get())
                except AttributeError as a:
                    print(a)
                except Exception as e:
                    print("Can Error: " + str(e))
                    time.sleep(2)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        finally:
            print("Closing Bus")
            file.close()
            self.bus.shutdown()

    def sendMessages(self, DataQueue : queue.Queue):
        """"""
        try:
            while True:
                while not DataQueue.empty():
                    #self.busLock.acquire()
                    msgToSend = DataQueue.get()
                    print(f"{Fore.GREEN} Sending: {msgToSend}{Fore.RESET}")
                    self.bus.send(msg=msgToSend)
                    #self.busLock.release()
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
        finally:
            print("Closing Bus")
            self.bus.shutdown()
    
    def __del__(self):
        print("Closing Bus")
        self.bus.shutdown()


if __name__ == "__main__":
    InputBUS = PCanBus(channel='PCAN_USBBUS1')
    OutputBUS = PCanBus(channel='PCAN_USBBUS2')

    SharedData = queue.Queue()

    listenerThread = Thread(target = InputBUS.listen, kwargs={
                                                        'fileName' : 'PCAN_History_Default.txt',
                                                        'DataStore' : SharedData
                                                        })

    senderThread = Thread(target = OutputBUS.sendMessages, kwargs={
                                                            'DataQueue' : SharedData
                                                            })
    
    listenerThread.start()
    senderThread.start()

    listenerThread.join()
    senderThread.join()