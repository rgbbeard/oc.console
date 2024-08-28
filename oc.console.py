#!/usr/bin/python

from console import Console
from os import system
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

console = Console()
autocompletion = WordCompleter(console.get_commands())
history = FileHistory('.sesshstr')


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
        # the first element is always the command
        cmd = args.pop(0)
        argsvalid = len(args) >= 1

    try:
        # save every entry
        console.save_history(cmd, args, argsvalid)

        # list all the available PODS
        if not argsvalid and (cmd == "find" or cmd == "ls"):
            console.get_pods_list()

        # search for a specific POD
        elif argsvalid and cmd == "find":
            console.get_pods_list(args[0])

        # enter bash for the requested POD
        elif argsvalid and cmd == "enter":
            try:
                pod_name = args[0]
            except IndexError as ie:
                pod_name = ""
                print("An unexpected error has occurred")
                pass

            console.spawn_bash(pod_name)

        # upload a file to the specified path inside a POD
        elif argsvalid and cmd == "upload":
            if len(args) == 2:
                console.verify_xload_args(args)
                #console.do_upload(pod_name=args[2], args[4], args[6])
            pass

        # download a file from the specified path inside a POD
        elif argsvalid and cmd == "download":
            print(args)
            #console.do_download(pod_name=args[1], args[2], args[3])
            pass

        # move a file from a pod to another
        elif argsvalid and cmd == "upload-pod2pod":
            print("Coming soon")
            pass

        # do i need to explain this?
        elif cmd == "login":
            console.do_login()

        # set working environment
        elif argsvalid and cmd == "use-env":
            console.set_env(args[0])

        elif cmd == "currenv" or cmd == "env" or cmd == "env?":
            console.get_env()

        # needed for login
        elif argsvalid and (cmd == "set-credentials-path" or cmd == "set-credentials"):
            console.set_credentials_path(args[0])

        # display a generic help message
        elif cmd == "help":
            console.get_help_for(cmd)

        # display the manual for a specific command
        # TODO: add the possibility to get the manual for multiple commands
        elif argsvalid and cmd == "help":
            console.get_help_for(args[0])

        # clear the screen, obviously
        elif cmd == "clear" or cmd == "cls":
            system("clear")

        elif cmd == "exit":
            exit()
    except KeyboardInterrupt as ki:
        exit()
