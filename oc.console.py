#!/usr/bin/python

from console import Console
from os import system
from prompt_toolkit import PromptSession
from pygame.locals import *
from pygame import event
import pygame

console = Console()

# without this the keyboard won't be captured
pygame.init()

history = console.get_history()
hcursor: int = len(history) - 1


# WIP
# TODO: make the history be shown
def prompt(ppt):
    global history, hcursor

    session = PromptSession()

    while True:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    hcursor -= 1

                    if hcursor < 0:
                        hcursor = 0

                    ppt = history[hcursor] if hcursor < len(history) else ''
                elif e.key == K_DOWN:
                    hcursor += 1

                    if hcursor >= len(history):
                        hcursor = len(history) - 1

                    ppt = history[hcursor] if hcursor < len(history) else ''
                elif e.key == K_RETURN:
                    return session.prompt(ppt)

        return session.prompt(ppt)


# this is the core of the program
while True:
    cmd = prompt("oc.console $>")
    cmd = cmd.strip()
    argsvalid = False
    args = []

    if not (not cmd):
        args = cmd.split(" ")
        argsvalid = len(args) >= 2

    try:
        # save every entry
        console.save_history(cmd, args, argsvalid)

        # reload history
        history = console.get_history()

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
