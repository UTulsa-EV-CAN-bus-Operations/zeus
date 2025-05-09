from typing import Literal, TypeAlias

TabType: TypeAlias = Literal[
    "Live",
    "HMI"
]
valid_tabs: list[TabType] = [
    "Live",
    "HMI"
]