from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Footer
from textual.reactive import reactive
from rich.text import Text  # Ensure to import Text

class SignalWidget(Static):
    """Widget to display a label and a value, optionally with a visual bar."""

    def __init__(self, label: str, value: str = "---", visual: bool = False):
        super().__init__()
        self.label = label
        self._visual = visual  # private attribute
        self.value = value
        self.update_display()

    def update_value(self, new_value):
        self.value = new_value
        self.update_display()

    def update_display(self):
        if self._visual and isinstance(self.value, (int, float)):
            filled = int(min(max(self.value / 500, 0), 1) * 10)
            bar = "▓" * filled + "░" * (10 - filled)
            # Use rich.text.Text to safely handle the text with brackets
            display = Text(f"{self.label}\n{bar}\n[{self.value} W]")
        else:
            display = Text(f"{self.label}: {self.value}")

        self.update(display)

class CanHmiDashboard(App):
    BINDINGS = [("q", "quit", "Quit")]

    charging_status = reactive("Not Charging")
    charging_power = reactive(0)
    door_status = reactive("Closed")
    voltage = reactive("380.2 V")
    current = reactive("8.5 A")
    temperature = reactive("45.6 °C")
    system_state = reactive("OK")

    def compose(self) -> ComposeResult:
        self.status_widget = SignalWidget("Charging Status", self.charging_status)
        self.power_widget = SignalWidget("Charging Power", self.charging_power, visual=True)
        self.door_widget = SignalWidget("Port Door", self.door_status)
        self.voltage_widget = SignalWidget("Voltage", self.voltage)
        self.current_widget = SignalWidget("Current", self.current)
        self.temp_widget = SignalWidget("Temperature", self.temperature)
        self.state_widget = SignalWidget("State", self.system_state)

        yield Static("⚡ Onboard Charger HMI", id="title", classes="header")
        with Horizontal():
            yield self.status_widget
            yield self.power_widget
            yield self.door_widget
        with Horizontal():
            yield self.voltage_widget
            yield self.current_widget
        with Horizontal():
            yield self.temp_widget
            yield self.state_widget
        yield Footer()

    def on_mount(self):
        self.set_interval(1.0, self.mock_update)

    def mock_update(self):
        import random
        self.status_widget.update_value(random.choice(["Charging", "Not Charging"]))
        self.power_widget.update_value(random.randint(0, 5000))
        self.door_widget.update_value(random.choice(["Open", "Closed"]))
        self.voltage_widget.update_value(f"{random.uniform(350, 400):.1f} V")
        self.current_widget.update_value(f"{random.uniform(0, 20):.1f} A")
        self.temp_widget.update_value(f"{random.uniform(30, 50):.1f} °C")
        self.state_widget.update_value(random.choice(["OK", "Idle", "Fault"]))


if __name__ == "__main__":
    CanHmiDashboard().run()