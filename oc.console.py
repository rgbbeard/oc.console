#!/usr/bin/python

from os import system
from os.path import dirname
from re import search, sub
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import importlib.util

BASE = dirname(__file__)

# load the Console class
spec = importlib.util.spec_from_file_location("c", f"{BASE}/sys/console.py")
cnsl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cnsl)
Console = cnsl.Console

console = Console()

# automatically login at startup
console.commands.do_login()

autocompletion = WordCompleter(console.call_manuel())
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

        # display a generic help message
        if cmd == "help" or cmd == "manuel" or cmd == "manuel!":
            console.get_help_for("help")

        # display the manual for a specific command
        elif argsvalid and (cmd == "help" or cmd == "manuel" or cmd == "manuel!"):
            console.get_help_for(args[0])

        elif cmd == "clear" or cmd == "cls":
            system("clear")

        elif cmd == "exit":
            exit()

        # required before login
        elif argsvalid and (cmd == "set-credentials-path" or cmd == "set-credentials"):
            console.set_credentials_path(args[0])

        # required before login
        elif argsvalid and cmd == "set-host":
            console.commands.set_host(args[0])

        elif cmd == "currhost" or cmd == "host" or cmd == "host?":
            console.get_host()
        
        elif cmd == "login":
            console.commands.do_login()

        elif cmd == "envs" or cmd == "envs?":
            console.get_envs()

        # set working environment
        elif argsvalid and cmd == "use-env":
            console.commands.set_env(args[0])

        elif cmd == "currenv" or cmd == "env" or cmd == "env?":
            console.commands.get_env()

        # list all the available pods
        elif not argsvalid and (cmd == "find" or cmd == "ls"):
            console.get_pods()

        # search for a specific pod
        elif argsvalid and cmd == "find":
            console.get_pod(args[0])

        # enter bash for the requested pod
        elif argsvalid and cmd == "enter":
            console.commands.spawn_bash(args[0])

        # show pod logs with stern
        elif argsvalid and cmd == "logs":
            _since = None

            for i in range(0, len(args)-1):
                a = args[i]

                if "--since" == a:
                    try:
                        _since = args[i+1]

                        # example: --since 1h24m10s
                        matches = search(r"(\d{1,2}[h|m|s])?", _since)
                        if not matches:
                            print("'Since' value not valid")
                            continue
                    except IndexError as ie:
                        print("'Since' value not found")
                    finally:
                        args.pop(i)
                        args.pop(i+1)

            console.get_logs(args[0], _since)

        # upload a file to the specified path inside a pod
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
                    continue
                else:
                    print("Invalid command syntax")

        # download a file from the specified path inside a pod
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
                    continue
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
    except KeyboardInterrupt as ki:
        exit()
