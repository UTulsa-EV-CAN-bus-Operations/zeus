from abc import ABC, abstractmethod
import can

class BusConfig(ABC):
    interface: str = None
    channel: str = None
    bitrate: int = None

    @abstractmethod
    def create_bus(self) -> can.Bus:
        pass

class VirtualBusConfig(BusConfig):
    interface = "virtual"
    channel = "test"
    bitrate = 500000

    def create_bus(self):
        return can.Bus(interface=self.interface, channel=self.channel, bitrate=self.bitrate)

class PCANBusConfig(BusConfig):
    interface = "pcan"
    channel = "PCAN_USBBUS1"
    bitrate = 500000

    def create_bus(self):
        return can.Bus(interface=self.interface, channel=self.channel, bitrate=self.bitrate)
