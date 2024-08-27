#!/usr/bin/python

from console import Console
from os import system
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

console = Console()
autocompletion = WordCompleter(console.get_commands())
history = FileHistory('../.sesshstr')


def prompt(ppt):
    global autocompletion, history

    session = PromptSession(completer=autocompletion, history=history)

    try:
        return session.prompt(ppt, auto_suggest=AutoSuggestFromHistory())
    except KeyboardInterrupt:
        exit()
    except EOFError:
        exit()


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

        # list all the available PODS
        if cmd == "find":
            console.get_pods_list()

        # search for a specific POD
        elif argsvalid and args[0] == "find":
            console.get_pods_list(args[1])

        # enter bash for the requested POD
        elif args[0] == "enter":
            try:
                pod_name = args[1]
            except IndexError as ie:
                pod_name = ""
                print("An unexpected error has occurred")
                pass

            console.spawn_bash(pod_name)

        # upload a file to the specified path inside a POD
        elif argsvalid and args[0] == "upload":
            #console.do_upload(pod_name=args[2], args[4], args[6])
            pass

        # download a file from the specified path inside a POD
        elif argsvalid and args[0] == "download":
            #console.do_download(pod_name=args[1], args[2], args[3])
            pass

        # do i need to explain this?
        elif cmd == "login":
            console.do_login()

        # set working environment
        elif argsvalid and args[0] == "use-env":
            console.set_env(args[1])

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
