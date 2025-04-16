import csv
import io

from rich.table import Table

import can
import time
import datetime
from can import LogReader, MessageSync

from textual import on
from textual.app import App
from textual.widgets import Input, Label, RichLog

class ReplayConfig:
    filename: str = ''
    channel: str = 'PCAN_USBBUS1'
    interface: str = 'virtual'
    bitrate: int = 500000

class LogReplay(App):
    
    def __init__(self):
        super().__init__()
        self.config = ReplayConfig()

    def compose(self):
        yield Input(placeholder="Type filepath of log you want to replay...")
        self.logwidget = RichLog()
        yield self.logwidget

    def on_mount(self):
        self.logwidget.styles.height = 30

    @on(Input.Submitted)
    def accept_config(self):
        if (self.config.filename == ''):
            input = self.query_one(Input)
            self.config.filename = input.value
            self.mount(Label(self.config.filename))
            input.value = ""
        
        log=self.query_one(RichLog)

        bus = can.interface.Bus(channel=self.config.channel, interface=self.config.interface, bitrate=self.config.bitrate, receive_own_messages=True)

        filename = 'TextualReplayTESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
        logger = can.Logger(filename)

        csvfile = 'TableReplayTESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.csv'.format(date=datetime.datetime.now())
        csvlogger = can.Logger(csvfile)

        reader = LogReader(self.config.filename)

        notifier = can.Notifier(bus, [logger,csvlogger])
        
        for msg in MessageSync(messages=reader):
            try:
                if msg.is_error_frame == False:
                    #log.write(str(msg))
                    bus.send(msg)

            except KeyboardInterrupt:
                pass
        
        time.sleep(1.0)
        log.write("Shutting down...")
        notifier.stop()
        bus.shutdown()


        


if __name__ == "__main__":
    app=LogReplay()
    app.run()
