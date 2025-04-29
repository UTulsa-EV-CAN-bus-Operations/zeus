import can
import cantools
from pprint import pprint

import cantools.database

db = cantools.database.load_file('zeus-app\zeus\dbc\ChargerPortTest.dbc')
db.messages

door_message = db.get_message_by_name('Charger_Port_Door_State')
pprint(door_message)
pprint(door_message.signals)
data = door_message.encode({'Door': 1})
message = can.Message(arbitration_id=door_message.frame_id, data=data)
pprint(message)

pprint(db.decode_message(message.arbitration_id,message.data))


bus1 = can.Bus(channel='test',interface='virtual')
valid_ids = set(msg.frame_id for msg in db.messages)
file_path = 'zeus-app\zeus\logs\Open Close Door - ID 0x045E.trc'
log_reader = can.LogReader(file_path)
messages = can.MessageSync(log_reader)

for msg in messages:
    if msg.is_error_frame == False:
        if (msg.is_rx):
            rxtx="Rx"
        else:
            rxtx="Tx"
    if msg.arbitration_id in valid_ids:
        try:
            decoded = db.decode_message(msg.arbitration_id, msg.data)
            pprint(decoded)
        except Exception as decode_err:
            print(f"Failed to decode message {hex(msg.arbitration_id)}: {decode_err}")

bus1.shutdown()