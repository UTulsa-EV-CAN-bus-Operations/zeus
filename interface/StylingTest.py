import can
import time
import datetime

from can import LogReader, MessageSync

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Log, Header, Footer, Input, Select, Button

class ReplayConfig():
    filename = "reverse-isolated.trc"
    interface = "pcan"
    channel = "PCAN_USBBUS1"
    bitrate = 500000


class LogApp(App):
    CSS_PATH = "StylingTest.tcss"
    
    def __init__(self):
        super().__init__()
        self.config = ReplayConfig()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Log(),
            id="logwindow"
        )
        yield Container(
            Input(placeholder="Enter log file to replay"),
            id="replayconfig"
        )
        yield Container(
            Horizontal(
                Select(options=[("pcan", "pcan"), ("virtual", "virtual")], prompt="Select Interface", id="interface"),
                Select(options=[("PCAN_USBBUS1", "PCAN_USBBUS1"), ("test", "test")], prompt="Select Channel", id="channel"),
                Select(options=[("500000", "500000")], prompt="Select Bitrate", id="bitrate")
            ),
            Button(label="Start Replay", id="start"), 
            name="busconfig",
            id="busconfig"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        log=self.query_one(Log)

        bus = can.interface.Bus(channel=self.config.channel, interface=self.config.interface, bitrate=self.config.bitrate, receive_own_messages=True)

        filename = 'trc-logs\\TextualReplayTESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
        logger = can.Logger(filename)

        reader = LogReader(self.config.filename)

        notifier = can.Notifier(bus, [logger])
        
        for msg in MessageSync(messages=reader):
            try:
                if msg.is_error_frame == False:
                    log.write(str(msg)+"\n")
                    bus.send(msg)

            except KeyboardInterrupt:
                pass
        
        time.sleep(1.0)
        log.write("Shutting down...")
        notifier.stop()
        bus.shutdown()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        select_widget = event.select
        if(select_widget.id == "interface"):
            self.config.interface = event.value
        elif(select_widget.id == "channel"):
            self.config.channel = event.value
        else:
            self.config.bitrate = int(event.value)
    
    @on(Input.Submitted)
    def accept_filename(self):
        input = self.query_one(Input)
        self.config.filename = input.value
    
            

if __name__ == "__main__":
    app = LogApp()
    app.run()