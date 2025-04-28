"""Widget for viewing HMI"""

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.events import Show
from textual.validation import Integer
from textual.widgets import Button, Checkbox, Input, Label, Select, Static

class HMIView(Horizontal):
    DEFAULT_CSS = """
    LogView {
      #tool_bar {
        height: 3;
        background: $surface-darken-1;
        #max_lines {
          width: 12;
        }
        Label {
          margin-top: 1;
          background: transparent;
        }
      }
      #logs {
        border: solid $primary;
      }
    }
    """
