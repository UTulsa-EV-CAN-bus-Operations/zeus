from cantools.database import Database
from textual.widgets import Static, Tree

from zeus.messages.messages import SignalSelected

class DBCTree(Tree[str]):

    db: Database

    def __init__(self, name: str = "dbc_tree_view", **kwargs):
        super().__init__("DBC Messages", id=name, **kwargs)

    def load_dbc(self, db: Database):
        self.db = db
        self.clear_tree()

        for msg in db.messages:
            msg_label = f"Message Name: {msg.name} (0x{msg.frame_id:X})"
            msg_node = self.root.add(msg_label)
            for sig in msg.signals:
                sig_node = msg_node.add(f"Signal Name: {sig.name}", data=(msg.name, sig.name))
                sig_node.add_leaf(f"Start Bit: {sig.start}")
                sig_node.add_leaf(f"Length: {sig.length}")
                sig_node.add_leaf(f"Unit: {sig.unit or '–'}")
                
                if sig.choices:
                    choices_node = sig_node.add("Choices:")
                    for val, label in sig.choices.items():
                        choices_node.add_leaf(f"{val}: {label}")
                else:
                    sig_node.add_leaf("Choices: None")

        self.root.expand()
    
    def clear_tree(self):
        self.clear()
        self.refresh()