from zeus.utils import TabType, valid_tabs

class BusConfig():
    interface = "virtual"
    channel = "test"
    bitrate = 500000

class Settings():
    startTab: TabType = "Live"