#!/usr/bin/python

from console import Console
from os import system
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

console = Console()

# automatically login at startup
console.do_login()

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
            console.get_pods()

        # search for a specific POD
        elif argsvalid and cmd == "find":
            console.get_pod(args[0])

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
                check = console.verify_xload_args(args, len(args), 1)
                
                if check:
                    console.do_upload(args[0], args[1])
                else:
                    print("Invalid command syntax")
            elif len(args) == 3:
                check = console.verify_xload_args(args, len(args), 1)
                
                if check:
                    #console.do_upload(pod_name=args[2], args[0], args[1])
                    pass
                else:
                    print("Invalid command syntax")

        # download a file from the specified path inside a POD
        elif argsvalid and cmd == "download":
            if len(args) == 2:
                check = console.verify_xload_args(args, len(args), 2)
                
                if check:
                    console.do_download(args[0], args[1])
                else:
                    print("Invalid command syntax")
            elif len(args) == 3:
                check = console.verify_xload_args(args, len(args), 2)
                
                if check:
                    #console.do_download(pod_name=args[2], args[0], args[1])
                    pass
                else:
                    print("Invalid command syntax")

        # move a file from a pod to another
        elif argsvalid and cmd == "upload-pod2pod":
            if len(args) == 2:
                check = console.verify_xload_args(args, len(args), 3)
                
                if check:
                    console.do_download(args[0], args[1])
                else:
                    print("Invalid command syntax")
        
        # do i need to explain this?
        elif cmd == "login":
            console.do_login()

        # set working environment
        elif argsvalid and cmd == "use-env":
            console.set_env(args[0])

        elif cmd == "currenv" or cmd == "env" or cmd == "env?":
            console.get_env()

        # required before login
        elif argsvalid and (cmd == "set-credentials-path" or cmd == "set-credentials"):
            console.set_credentials_path(args[0])

        # required before login
        elif argsvalid and cmd == "set-host":
            console.set_host(args[0])

        elif cmd == "host?" or cmd == "host":
            console.get_host()

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
