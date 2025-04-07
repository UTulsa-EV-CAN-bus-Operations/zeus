import can
import time
can.rc['interface'] = 'pcan'
can.rc['channel'] = 'PCAN_USBBUS1'
can.rc['bitrate'] = 500000
from can.interface import Bus

bus = Bus()
BufferedReader = can.BufferedReader()

Notifier = can.Notifier(bus=bus, listeners=[BufferedReader])
q = BufferedReader.buffer
file = open("PCAN_History.txt", "w")


try:
    while True: 
        try:

            msg = BufferedReader.get_message()
            if msg != None:
                print(msg)
                file.write(str(msg) + "\n")
                time.sleep(0.5)
            else:
                file.write("No Data\n")
                print("No Data")
                #if q.empty:
                #    print("Empty Message Queue")
                #    time.sleep(1)
                #else:
                #    while not q.empty:
                #        print(q.get())
        except AttributeError as a:
            print("No Data")
        except Exception as e:
            print("Can Error: " + str(e))
            time.sleep(2)
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    print("Closing Bus")
    file.close()
    bus.shutdown()
