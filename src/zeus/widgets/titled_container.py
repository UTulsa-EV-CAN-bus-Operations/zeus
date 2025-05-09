from textual.widgets import Static

class TitledContainer(Static):
    def __init__(self, title: str, *children, **kwargs):
        super().__init__(*children, **kwargs)
        self.title = title
        self.border_title = title  # Adds title to the border
        self.border = True  # Ensure the border is drawn