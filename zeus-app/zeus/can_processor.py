import asyncio
import can

from can import Bus

from textual import log
from textual.app import App

from zeus.messages.messages import CANFrame, CANMessageReceived, CAN_HMIMessageReceived
from zeus.config.app_config import BusConfig
from zeus.views.live_view import LiveView
from zeus.views.hmi_view import HMIView


class CANProcessor():
    
    app: App
    live_view: LiveView
    hmi_view: HMIView
    bus1: Bus
    bus1config: BusConfig

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bus1config = BusConfig()

    def set_app(self, app: App):
        self.app = app

    def set_live_view(self, live_view: LiveView):
        self.live_view = live_view

    def set_hmi_view(self, hmi_view: HMIView):
        self.hmi_view = hmi_view
    

    def initializeBus(self):
            self.bus1 = can.Bus(channel=self.bus1config.channel, interface=self.bus1config.interface, bitrate=self.bus1config.bitrate)
            log("Bus was initialized")
            log(self.bus1)

    async def loadTrace(self, file_path):
        try:
            log_reader = can.LogReader(file_path)
            messages = can.MessageSync(log_reader)

            await self.replayTrace(messages)
        except Exception as e:
            log("Error with loading trace")

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

            if (msg.arbitration_id == 0x02EC):
                self.hmi_view.post_message(CAN_HMIMessageReceived(self,frame))
            # Posts message to live view
            self.live_view.post_message(CANMessageReceived(self,frame))
            

            await asyncio.sleep(0.0001)  # Give some time for UI updates