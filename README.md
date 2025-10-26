# zeus
#### **DISCLAIMER**: This is a WIP TUI, it is not 100% stable, there are most certainly bugs. This tool also purely supports the PCAN CAN Bus Interface, we didn't have time to design and test supporting other interfaces. This project was designed within a rather short window of time. The current version is not polished to perfection, there's still a lot left to be desired. 

Zeus is intended to be used as an easily accessible library of CAN bus analysis tools that allow users to analyze, capture, and replay traffic via connected CAN bus adapters.

## Prerequisites
There are currently two options for running this.

1. You can run the app directly by navigating to `dist\zeus.exe`. This executable should work for supported machines.

2. If you by chance are on a machine that can't run `.exe` files, you'll likely have to defer to this method (and may want to have this method set up anyways, in case you want to fork off the repo and make changes to the project yourself).

    - Set up a python virtual environment (if you're unfamiliar, [this link](https://www.w3schools.com/python/python_virtualenv.asp) is helpful)
    - Check out the `requirements.txt` file which contains the dependencies (there aren't many). You can then run `pip install -r requirements.txt` to auto-install these dependencies.
    - Navigate to the `.\zeus\src\` directory (not the package folder in the src) and run `python -m zeus` from the CLI. The TUI should be up and running.

## Features & Current State

This version has the following features:

* Bus Setup/Status - allows users to select and connect/disconnect CAN bus interfaces that are available. It also should show the status of the connection, channel information, and bitrate.

* Trace Setup - should allow for users to select an actively connected CAN bus interface, enter a desired trace log file name and record the activity. You can then close the log file when you're done and want to save it.

* DBC Management - `.dbc` files are essentially a cheat-sheet that allows you to define rules/how CAN data should be interpreted. It allows us to take the raw data/signal names, etc. and make things understandable for humans to read. We set this tab up to allow you to select from the `dbc` directory in the project directory and load the file and view the structure/rules on the right-hand side of the screen. 
    * (**NOTE:** the directory pane is scoped to the project directory, I'd recommend placing any `.dbc` files in the `zeus\dbc` directory)

* Replay -the idea is self-explanatory, you can select the CAN bus interface you want to replay a trace/capture to, select and load the trace/capture from `zeus\logs`, and then start the replay. 

   * (**NOTE:** Because of time-restrictions and python multi-threading challenges, we added a delayed replay button due to the tool being poorly optimized for the sheer scale of data being handled. If the interface freezes when replaying, you may want to avoid the replay button and use the delayed replay button instead)

* Passthrough - this tab allows you to select two CAN bus interfaces that you'd like to have your machine sit between. This isn't 100% stable, more investigation needs to be done as it almost seemed like the PEAK adapters were struggling to keep up (along with the python code behind-the-scenes) with the number of packets being received/sent.

* HMI (Human Machine Interface) - this was a proof-of-concept that showed we could take a loaded `.dbc` file and replay a capture and see real-time signal behavior. This isn't dynamic, it isn't really useful in its current state.

