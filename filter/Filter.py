import base64

from textual.app import App, ComposeResult
from textual.widgets import RichLog
from rich.table import Table
import csv

class CSVLogApp(App):
    CSS = "RichLog { height: 100%; width: 100% }"

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_mount(self) -> None:
        table = self.create_table_from_csv("/Users/kiannajj/Desktop/zeus/interface/csv-logs/TableReplayTESTlog1PACM-2025-04-16_17-56-14.csv")
        log = self.query_one(RichLog)
        log.write(table)

    def create_table_from_csv(self, file_path: str) -> Table:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            table = Table(show_header=True, header_style="bold magenta")
            for header in headers:
                table.add_column(header)
                #print(header)

            id_tracker = set()
            arb_id_col = headers.index("arbitration_id")
            data_col = headers.index("data")

            for row in reader:
                arb_id = row[arb_id_col]
                if arb_id not in id_tracker:
                    # Convert data from base64 to bytearray form
                    data_b64 = row[data_col]
                    decoded_data = base64.b64decode(data_b64)
                    row[data_col] = str(bytearray(decoded_data))

                    # Add row to table and id
                    table.add_row(*row)
                    id_tracker.add(arb_id)
        print (table.row_count)

        return table

if __name__ == "__main__":
    app = CSVLogApp()
    app.run()