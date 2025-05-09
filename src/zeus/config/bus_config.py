import can

class BusConfig:
    def __init__(self, interface: str, channel: str, bitrate: int):
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate


    def create_bus(self) -> can.Bus:
        return can.Bus(interface=self.interface, channel=self.channel, bitrate=self.bitrate, receive_own_messages = True)

