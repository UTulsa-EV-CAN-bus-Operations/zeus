import click

def startMessage():
    print(r"""
         ___       ___  ________  ___  ___  _________  ________   ___  ________   ________     
        |\  \     |\  \|\   ____\|\  \|\  \|\___   ___\\   ___  \|\  \|\   ___  \|\   ____\    
        \ \  \    \ \  \ \  \___|\ \  \\\  \|___ \  \_\ \  \\ \  \ \  \ \  \\ \  \ \  \___|    
         \ \  \    \ \  \ \  \  __\ \   __  \   \ \  \ \ \  \\ \  \ \  \ \  \\ \  \ \  \  ___  
          \ \  \____\ \  \ \  \|\  \ \  \ \  \   \ \  \ \ \  \\ \  \ \  \ \  \\ \  \ \  \|\  \ 
           \ \_______\ \__\ \_______\ \__\ \__\   \ \__\ \ \__\\ \__\ \__\ \__\\ \__\ \_______\
            \|_______|\|__|\|_______|\|__|\|__|    \|__|  \|__| \|__|\|__|\|__| \|__|\|_______|
                                                                                       
                                                                                            """
        )

    print("Hello, User!")
    print("Enter 'quit' to exit the tool\n")

def getUserInput():
    optionsList = (
    "What would you like to do?\n"
    "   (1) Wake Battery\n"
    "   (2) View Battery Data\n"
    "   (3) Start Charging\n\n") 
    userInput = input(optionsList)
    return userInput

def wakeBattery():
    print("I'm awake!\n")

def viewData():
    print("Data stuff\n")

def startCharging():
    print("Charging now!\n")

def invalidCommand():
    print("Invalid Command.\n")

def handleInput(command):
    action = command_map.get(command, invalidCommand)
    action()


command_map = {
    "1": wakeBattery,
    "2": viewData,
    "3": startCharging,
    "quit": exit
}

startMessage()

userInput = getUserInput()
handleInput(userInput)
