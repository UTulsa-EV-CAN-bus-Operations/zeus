import asyncio
import can
import cantools

from can import Bus

from cantools import database

import cantools.database
from textual import log
from textual.app import App

from zeus.messages.messages import CANFrame, CANMessageReceived, CAN_HMIMessageReceived
from zeus.config.bus_config import BusConfig
#from zeus.views.replay_view import ReplayView
from zeus.views.hmi_view import HMIView

import time
import datetime
from multiprocessing import Process, Queue

class CANProcessor():
    
    app: App
    #replay_view: ReplayView
    hmi_view: HMIView

    busDict : dict[str, Bus]
    configDict : dict[str, BusConfig]
    loggerDict : dict[str, can.Logger]
    notifierDict : dict[str, can.Notifier]

    db: database
    messagesToPlay: can.MessageSync
    shouldLog: bool
    logger: can.Logger
    notifier: can.Notifier
    BusyCANConnections: list[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.shouldLog = False
        self.messagesToPlay = None

        self.busDict = {}
        self.configDict = {}
        self.loggerDict = {}
        self.notifierDict = {}

        self.BusyCANConnections = []

    def set_app(self, app: App):
        self.app = app

    #def set_replay_view(self, replay_view: ReplayView):
    #    self.replay_view = replay_view

    def set_hmi_view(self, hmi_view: HMIView):
        self.hmi_view = hmi_view
    
    def initializeBus(self, config: BusConfig, busName : str):
        try:
            if self.busDict[busName]:
                self.busDict[busName].shutdown()

        except KeyError as k:
            self.busDict[busName] = config.create_bus()
            self.configDict[busName] = config
            log(f"Bus {busName} was initialized")
            log(self.busDict[busName])

    def load_dbc(self, dbc_path: str):
        try:
            self.db = cantools.database.load_file(dbc_path)
            self.valid_ids = set(msg.frame_id for msg in self.db.messages)
        except Exception as e:
            log("Failed to load dbc file: ", e)

    def registerLogger(self, filename : str, busName : str): # TODO: Trackdown references and update // tf does this do?
        # If I understand this correctly we need to associate a Logger with a can Notifier object which is associated with a can python object?
        self.shouldLog = True
        file_path = "zeus/logs/" + filename + ".trc" 
        log("Registering logger and notifier...")
        self.loggerDict[busName] = can.Logger(file_path)
        self.notifierDict[busName] = can.Notifier(self.busDict[busName], [self.loggerDict[busName]])
        log("Logger registration complete!")
    
    def closeLogger(self):
        if (self.logger != None and self.notifier!=None):
            self.logger.stop()
            self.notifier.stop()

    async def loadTrace(self, file_path, busname: str):
        try:
            log_reader = can.LogReader(file_path)
            messages = can.MessageSync(log_reader)

            await self.replayTrace(messages, busname)
        except Exception as e:
            log("Error with loading trace: ", e)

    async def replayTrace(self, message_sync, busName : str):
      
        for msg in message_sync:
            log(f"Got message: {msg}")
            if msg.is_error_frame == False:
                if (msg.is_rx):
                    rxtx="Rx"
                else:
                    rxtx="Tx"

            frame = CANFrame(
                timestamp = f"{msg.timestamp:.3f}",
                can_id = f"{msg.arbitration_id:03X}",
                rxtx=rxtx,
                length = msg.dlc,
                data = " ".join(f"{b:02X}" for b in msg.data),
            )

            self.busDict[busName].send(msg)

            if self.db and msg.arbitration_id in self.valid_ids:
                    try:
                        decoded = self.db.decode_message(msg.arbitration_id, msg.data)
                        log(f"Decoded message {hex(msg.arbitration_id)}: {decoded}")
                        self.hmi_view.post_message(CAN_HMIMessageReceived(self, frame, decoded))
                    except Exception as decode_err:
                        log(f"Failed to decode message {hex(msg.arbitration_id)}: {decode_err}")

            # Posts message to live view
            #self.replay_view.post_message(CANMessageReceived(self,frame))
            

            await asyncio.sleep(0.000001)  # Give some time for UI updates

    def load_replay(self, file_path):
        try:
            log_reader = can.LogReader(file_path)
            self.messagesToPlay = can.MessageSync(log_reader)

        except Exception as e:
            log("Error with loading trace: ", e)

    def replay(self, busName : str):
        for msg in self.messagesToPlay:
            log(f"Got message: {msg}")
            if msg.is_error_frame == False:
                if (msg.is_rx):
                    rxtx="Rx"
                else:
                    rxtx="Tx"

            frame = CANFrame(
                timestamp = f"{msg.timestamp:.3f}",
                can_id = f"{msg.arbitration_id:03X}",
                rxtx=rxtx,
                length = msg.dlc,
                data = " ".join(f"{b:02X}" for b in msg.data),
            )

            self.busDict[busName].send(msg)

            if self.db and msg.arbitration_id in self.valid_ids:
                    try:
                        decoded = self.db.decode_message(msg.arbitration_id, msg.data)
                        log(f"Decoded message {hex(msg.arbitration_id)}: {decoded}")
                        self.hmi_view.post_message(CAN_HMIMessageReceived(self, frame, decoded))
                    except Exception as decode_err:
                        log(f"Failed to decode message {hex(msg.arbitration_id)}: {decode_err}")

            # Posts message to live view
            #self.replay_view.post_message(CANMessageReceived(self,frame))
            

            #await asyncio.sleep(0.00001)  # Give some time for UI updates
    
    def startPassthrough(self, bus_1, bus_2, bus1_file, bus2_file):
        SharedDataLtR = Queue()
        SharedDataRtL = Queue()

        self.busDict[bus_1].shutdown()
        del self.busDict[bus_1]
        del self.configDict[bus_1]
        self.BusyCANConnections.append(bus_1)
        
        self.busDict[bus_2].shutdown()
        del self.busDict[bus_2]
        del self.configDict[bus_2]
        self.BusyCANConnections.append(bus_2)
        
        self.sendProcess1 = Process(target=sendPassthroughMessages, kwargs = {
            'bus_name' : bus_1,
            'logger_file' : bus1_file,
            'inQueue' :  SharedDataLtR,
            'outQueue' : SharedDataRtL
        }, daemon=True)


        self.sendProcess2 = Process(target=sendPassthroughMessages, kwargs = {
            'bus_name' : bus_2,
            'logger_file' : bus2_file,
            'inQueue' :  SharedDataRtL,
            'outQueue' : SharedDataLtR
        }, daemon=True)

        self.sendProcess1.start()
        self.sendProcess2.start()

    def stopPassThrough(self, bus_1, bus_2):
        self.sendProcess1.terminate()
        self.sendProcess2.terminate()
        self.BusyCANConnections.remove(bus_1)
        self.BusyCANConnections.remove(bus_2)


def sendPassthroughMessages(bus_name : str, logger_file : str, inQueue : Queue = [], outQueue : Queue = []): # TODO: Refactor
       
        # Instatiate logger to log received messages to timestamped file
        bus = can.interface.Bus(channel=bus_name, interface='pcan', bitrate=500000, receive_own_messages = True)
        BufferedReader = can.BufferedReader()

        if logger_file != None:
            logger = can.Logger(logger_file)
            notifier = can.Notifier(bus, [logger, BufferedReader])
        else:
            notifier = can.Notifier(bus, [BufferedReader])

        while True:
            msg = BufferedReader.get_message()
            if msg != None:
                outQueue.put(msg)
            while not inQueue.empty():
                #self.busLock.acquire()
                msgToSend = inQueue.get()
                #print(f"{Fore.GREEN} Sending: {msgToSend}{Fore.RESET}")
                if msgToSend != None:
                    try:
                        bus.send(msg=msgToSend)
                    except Exception as e:
                        print(f"Exception Occured {e}")
        