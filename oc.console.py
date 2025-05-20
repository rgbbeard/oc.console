#!/usr/bin/python

from sys import argv
from os import system
from os.path import dirname
from re import search, sub
from typing import Union

modules = {
    "prompt_toolkit": {
        "url": "https://pypi.org/project/prompt-toolkit/",
        "command": "pip install prompt-toolkit"
    },
    "pynput": {
        "url": "https://pypi.org/project/pynput/",
        "command": "pip install pynput"
    }
}


def try_install(module_name: str):
    command = modules[module_name]["command"]

    print(f"Executing {command}...\n")
    try:
        system(command)
    except Exception as e:
        print(e)
        exit()

    print("Restart the console to see the changes")
    exit()


def display_error_message(module_name: str):
    url = modules[module_name]["url"]

    print(f"Package {module_name} is required\n")

    response = input("Would you like to install it now? (yes/no) ")
    if "yes" == response:
        try_install(module_name)
    else:
        print("See {url} for more details\n")
    exit()


try:
    from prompt_toolkit import PromptSession, prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory, InMemoryHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
except ImportError as ie:
    display_error_message("prompt_toolkit")

try:
    from pynput.keyboard import Key, Listener, Controller
except ImportError as ie:
    display_error_message("pynput")

from oc_deps_manager import OCDepsManager
import utilities

# program settings
BASE = dirname(__file__)
__line__ = utilities._line()

IS_CLONED = len(argv) > 1 and not (not argv[1]) and bool("--clone" == argv[1])

if IS_CLONED:
    print("""THIS WINDOW IS RUNNING AS A CLONE, SOME COMMANDS WILL NOT BE AVAILABLE IN THIS MODE\n""")

# load the Console class
cnsl = OCDepsManager.module_from_path(f"{BASE}/sys/console.py")
Console = cnsl.Console

# load the ThreadMaid class
thdmd = OCDepsManager.module_from_path(f"{BASE}/sys/thread_maid.py")
ThreadMaid = thdmd.ThreadMaid

console = Console()
commands_thread = ThreadMaid()

# TODO: implement login only if necessary
# automatically login at startup
# console.commands.do_login()
autocompletion = WordCompleter(console.call_manuel())
history = FileHistory('.sesshstr')


# TODO: complete this feature
def detect_console_commands():
    pass


commands_thread.setup(target=detect_console_commands).run()


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
            # display the manual for a specific command
            if argsvalid:
                console.get_help_for(args[0])
            else:
                console.get_help_for("help")

        elif cmd == "clear" or cmd == "cls":
            system("clear")

        elif cmd == "exit":
            exit()

        # required before login
        elif argsvalid and (cmd == "set-credentials-path" or cmd == "set-credentials"):
            console.set_credentials_path(args[0])

        # required before login
        elif argsvalid and cmd == "set-host":
            console.set_host(args[0])

        elif cmd == "currhost" or cmd == "host" or cmd == "host?":
            console.get_host()
        
        elif cmd == "login":
            console.commands.do_login()

        elif cmd == "envs" or cmd == "envs?":
            console.get_envs()

        # set working environment
        elif cmd == "use-env":
            if argsvalid:
                console.commands.set_env(args[0])
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        elif cmd == "currenv" or cmd == "env" or cmd == "env?":
            console.commands.get_env()

        # list all the available pods
        elif cmd == "ls":
            console.get_pods()

        # search for a specific pod
        elif cmd == "find":
            if argsvalid:
                console.get_pod(args[0])
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        # enter bash for the requested pod
        elif cmd == "enter":
            if argsvalid:
                console.commands.spawn_bash(args[0])
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        # show pod logs with stern
        elif cmd == "logs":
            if argsvalid:
                since = None
                save_logs = False
                search_: Union[str, list] = None
                debug: bool = False

                for i in range(0, len(args)):
                    a = args[i]

                    if "--since" == a:
                        try:
                            since = args[i+1]

                            # example: --since 1h24m10s
                            matches = search(r"(\d{1,2}[h|m|s])?", since)
                            if not matches:
                                print("'Since' value not valid")
                                continue
                        except IndexError as ie:
                            print("'Since' value not found")
                    if "--debug" == a:
                        debug = True
                    if "--save-logs" == a:
                        save_logs = True
                    if "--search" == a:
                        try:
                            r = range(i+1, len(args))

                            if len(r) > 1:
                                search_ = []

                                for j in r:
                                    search_.append(args[j])
                            else:
                                search_ = args[i+1]
                        except IndexError as ie:
                            print("No filters passed")

                console.get_logs(
                    args[0], 
                    since=since, 
                    search=search_, 
                    save_logs=save_logs, 
                    debug=debug
                )
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        # upload a file to the specified path inside a pod
        elif cmd == "upload":
            if argsvalid:
                check = console.verify_xload_args(args, len(args), 1)

                if len(args) == 2:
                    if check:
                        console.do_upload(_from=args[0], _to=args[1])
                    else:
                        print(f"Invalid command syntax :: {__line__}")
                elif len(args) == 3:
                    if check:
                        console.do_upload(
                            pod_name=args[0], 
                            _from=args[1], 
                            _to=args[2]
                        )
                    else:
                        print(f"Invalid command syntax :: {__line__}")
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        # download a file from the specified path inside a pod
        elif cmd == "download":
            if argsvalid:
                check = console.verify_xload_args(args, len(args), 2)

                if len(args) == 2:
                    if check:
                        console.do_download(_from=args[0], _to=args[1])
                    else:
                        print(f"Invalid command syntax :: {__line__}")
                elif len(args) == 3:
                    if check:
                        console.do_download(
                            pod_name=args[0], 
                            _from=args[1], 
                            _to=args[2]
                        )
                    else:
                        print(f"Invalid command syntax :: {__line__}")
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")

        # move a file from a pod to another
        elif cmd == "upload-pod2pod":
            if argsvalid:
                check = console.verify_xload_args(args, len(args), 3)

                if len(args) == 2:  
                    if check:
                        console.do_pod2pod_transfer(args[0], args[1])
                    else:
                        print(f"Invalid command syntax :: {__line__}")
            else:
                print(f"Command incomplete, please read the documentation for {cmd}")
        else:
            if not (not cmd):
                print(f"Command not recognized: {cmd}")
    except KeyboardInterrupt as ki:
        print("Type 'exit' to terminate the session")
