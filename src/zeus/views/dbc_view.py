from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Label, Static, DirectoryTree, Button

from zeus.widgets.dbc_tree import DBCTree

class DBCView(Container):

    DEFAULT_CSS = """
    #left-panel{
        height: auto;
        width: 1fr;
        margin: 0 2;
    }
    #right-panel {
        height: auto;
        width: 2fr;
        margin: 0 2;
    }
    #dir_tree {
        margin: 1 0 1 0;
        border: round white;
    }
    #dbc_tree {
        margin: 1 0 2 0;
        border: round white;
    }
    """

    can_processor: object
    dir_tree: DirectoryTree
    db_tree: DBCTree
    
    def __init__(self, root_dir: str = ".", **kwargs):
        super().__init__(**kwargs)
        self.root_dir = root_dir
        self.selected_dbc_path = None
        self.db = None
        self.db_tree = DBCTree("dbc_tree")
        self.dir_tree = DirectoryTree(self.root_dir, id="dir_tree")

        self.can_processor = self.app.can_processor

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with Horizontal():
                with Vertical(id="left-panel"):
                    self.dir_tree.border_title = "Select a .dbc file: "
                    yield self.dir_tree
                    yield Button(label="Load DBC", id="load_dbc")
                with ScrollableContainer(id="right-panel"):
                    self.db_tree.border_title = f"Filename: {None}"
                    yield self.db_tree

    @on(DirectoryTree.FileSelected)
    def on_directory_tree_click(self, event: DirectoryTree.FileSelected) -> None:
        if str(event.path).endswith(".dbc"):
            self.selected_dbc_path = event.path
            log(f"Selected DBC: {self.selected_dbc_path}")
        else:
            self.selected_dbc_path = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load_dbc":
            log("DBC file loading...")
            self.can_processor.load_dbc(self.selected_dbc_path)
            if (self.can_processor.db != None):
                self.db = self.can_processor.db 
                self.db_tree.border_title = f"Filename: {self.selected_dbc_path.name}"
            self.display_dbc_info()

    def display_dbc_info(self):
        if not self.db:
            return
        self.db_tree.load_dbc(self.db)
