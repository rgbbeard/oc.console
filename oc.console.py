#!/usr/bin/python

from console import Console
from os import system
import curses

console = Console()


# WIP
# TODO: make this function work properly
def get_input(prompt):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.addstr(prompt)
    input_str = ""
    while True:
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key == 10:
            break
        elif key == curses.KEY_BACKSPACE or key == 127:
            input_str = input_str[:-1]
        else:
            input_str += chr(key)
        stdscr.addstr(prompt + input_str + " " * (curses.COLS - len(prompt) - len(input_str) - 1))
        stdscr.refresh()
    curses.endwin()
    return input_str


while True:
    # cmd = input("oc.console $>")
    cmd = get_input("oc.console $>")
    cmd = cmd.strip()
    argsvalid = False
    args = []

    if not (not cmd):
        args = cmd.split(" ")
        argsvalid = len(args) >= 2

    try:
        # save every entry
        console.save_history(cmd, args, argsvalid)

        # list all the available PODS
        if cmd == "find":
            console.get_pods_list()

        # search for a specific POD
        elif argsvalid and args[0] == "find":
            console.get_pods_list(args[1])

        # enter bash for the requested POD
        elif argsvalid and args[0] == "enter":
            console.spawn_bash(args[1])

        # upload a file to the specified path inside a POD
        elif argsvalid and args[0] == "upload":
            # TODO: fix the bash script to enable this feature
            print("This feature is not available yet.")

        # do i need to explain this?
        elif cmd == "login":
            console.do_login()

        # needed for login
        elif argsvalid and args[0] == "set-credentials-path":
            console.set_credentials_path(args[1])

        # display a generic help message
        elif cmd == "help":
            console.get_help_for(cmd)

        # display the manual for a specific command
        # TODO: add the possibility to get the manual for multiple commands
        elif argsvalid and args[0] == "help":
            console.get_help_for(args[1])

        # clear the screen, obviously
        elif cmd == "clear" or cmd == "cls":
            system("clear")

        elif cmd == "exit":
            exit()
    except KeyboardInterrupt as ki:
        exit()
