from threading import Thread
from PCanBusObject import PCanBus
import queue
from colorama import Fore

if __name__ == "__main__":
    Left_to_Right = True
    Right_to_Left = True

    LeftBUS = PCanBus(channel='PCAN_USBBUS1')
    RightBUS = PCanBus(channel='PCAN_USBBUS2')

    SharedDataLtR = queue.Queue()
    SharedDataRtL = queue.Queue()

    LeftlistenerThread = Thread(target = LeftBUS.listen, daemon=True, kwargs={
                                                        'fileName' : 'PCAN_History_LeftToRightPACM.txt',
                                                        'DataStore' : SharedDataLtR
                                                        })

    RightsenderThread = Thread(target = RightBUS.sendMessages, daemon=True, kwargs={
                                                            'DataQueue' : SharedDataLtR
                                                            })
    
    RightlistenerThread = Thread(target = RightBUS.listen, daemon=True, kwargs={
                                                        'fileName' : 'PCAN_History_RighttoLeftPACM.txt',
                                                        'DataStore' : SharedDataRtL
                                                        })

    LeftsenderThread = Thread(target = LeftBUS.sendMessages, daemon=True, kwargs={
                                                            'DataQueue' : SharedDataRtL
                                                            })

    if Left_to_Right:
        print(f"{Fore.BLUE}Starting Left to Right{Fore.RESET}")
        LeftlistenerThread.start()
        RightsenderThread.start()
        print(f"{Fore.BLUE}Left to Right Running{Fore.RESET}")
    
    if Right_to_Left:
        print(f"{Fore.BLUE}Starting Right to Left{Fore.RESET}")
        RightlistenerThread.start()
        LeftsenderThread.start()
        print(f"{Fore.BLUE}Right to Left Running{Fore.RESET}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(f"{Fore.RED}STOPPING{Fore.RESET}")
