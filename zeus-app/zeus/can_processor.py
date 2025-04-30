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
from zeus.views.replay_view import ReplayView
from zeus.views.hmi_view import HMIView


class CANProcessor():
    
    app: App
    replay_view: ReplayView
    hmi_view: HMIView
    bus1: Bus
    bus1config: BusConfig
    db: database
    messagesToPlay: can.MessageSync

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bus1config = None
        self.db = None
        self.bus1 = None

    def set_app(self, app: App):
        self.app = app

    def set_replay_view(self, replay_view: ReplayView):
        self.replay_view = replay_view

    def set_hmi_view(self, hmi_view: HMIView):
        self.hmi_view = hmi_view
    
    def initializeBus(self, config: BusConfig):
            if self.bus1:
                self.bus1.shutdown()
            self.bus1 = config.create_bus()
            self.bus1config = config
            log("Bus was initialized")
            log(self.bus1)

    def load_dbc(self, dbc_path: str):
        try:
            self.db = cantools.database.load_file(dbc_path)
            self.valid_ids = set(msg.frame_id for msg in self.db.messages)
        except Exception as e:
            log("Failed to load dbc file: ", e)

    async def loadTrace(self, file_path):
        try:
            log_reader = can.LogReader(file_path)
            messages = can.MessageSync(log_reader)

            await self.replayTrace(messages)
        except Exception as e:
            log("Error with loading trace: ", e)

    async def replayTrace(self, message_sync):

      #logger = can.Logger(filename)

      #notifier = can.Notifier(self.bus1)
      
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

            self.bus1.send(msg)

            if self.db and msg.arbitration_id in self.valid_ids:
                    try:
                        decoded = self.db.decode_message(msg.arbitration_id, msg.data)
                        log(f"Decoded message {hex(msg.arbitration_id)}: {decoded}")
                        self.hmi_view.post_message(CAN_HMIMessageReceived(self, frame, decoded))
                    except Exception as decode_err:
                        log(f"Failed to decode message {hex(msg.arbitration_id)}: {decode_err}")

            # Posts message to live view
            self.replay_view.post_message(CANMessageReceived(self,frame))
            

            await asyncio.sleep(0.000001)  # Give some time for UI updates

    def load_replay(self, file_path):
        try:
            log_reader = can.LogReader(file_path)
            self.messagesToPlay = can.MessageSync(log_reader)

        except Exception as e:
            log("Error with loading trace: ", e)

    def replay(self):
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

            self.bus1.send(msg)

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