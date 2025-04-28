"""Entry point for the app"""

from zeus.app import ZeusAnalysis

def run() -> None:
    # Run application
    ZeusAnalysis().run()

if __name__ == "__main__":
    run()