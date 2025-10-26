import textual
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Static
from textual.reactive import Reactive

TEXT = """BLAH
BLAH
BLAH"""


class MyApp(App):
    TITLE = "Lightning Tool ϟ"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="delete", action="delete", description="Delete the thing"),
    ]

    def compose(self) -> ComposeResult:
        self.header = Header(icon='⏷')
        self.widget = Static(TEXT)
        yield Footer()
        yield self.header
        yield self.widget
        

    def on_button_pressed(self) -> None:
        self.exit()
    
    def on_mount(self) -> None:
        self.screen.styles.background = "black"
        self.screen.styles.border = ("heavy", "white")
        # Handles container widget with TEXT, height fits text
        self.widget.styles.background = "purple"
        self.widget.styles.width = 30
        self.widget.styles.height = "auto"





    #COLORS = [
    #    "white",
    #    "maroon",
    #    "red",
    #    "purple",
    #    "fuchsia",
    #    "olive",
    #    "yellow",
    #    "navy",
    #    "teal",
    #    "aqua",
    #]

    #def on_mount(self) -> None:
    #    self.screen.styles.background = "red"

    #def on_key(self, event: events.Key) -> None:
    #    if event.key.isdecimal():
    #        self.screen.styles.background = self.COLORS[int(event.key)]


if __name__ == "__main__":
    app = MyApp()
    app.run()