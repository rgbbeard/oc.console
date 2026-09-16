#!/usr/bin/python

from typing import Union
from os import system
from os.path import dirname
from re import search
import random
from shlex import split as parse_params
from utilities import (
    has,
    is_scrambled,
    printerr,
    printalr,
    printinf,
    printsuc,
    is_empty,
    import_module_error,
    array_clear,
    _line
)
from echo import Echo
from krypto import Krypto
from exceptions import InvalidSyntaxError

BASE = dirname(__file__)
commands_queue = []


def send_command(cmd: Union[str, list]):
    global commands_queue

    commands_queue.append(cmd) if isinstance(cmd, str) else commands_queue.extend(cmd)


# Install required modules
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
except ImportError:
    import_module_error("prompt_toolkit")

try:
    from pynput.keyboard import Key, Listener, Controller
except ImportError:
    import_module_error("pynput")

from oc_deps_manager import OCDepsManager

# Load the Console class
cnsl = OCDepsManager.module_from_path(f"{BASE}/sys/console.py")
Console = cnsl.Console

"""
This will autonomously ask
for the login credentials if they're missing

see: sys/console.py -> Console -> __init__
"""
console = Console()
kt = console.kt
globalcfg = console.get_config()

# Automatically login if necessary
if not console.oc.session_is_valid():
    printalr("User is not authenticated or previous session expired")
    send_command("login via web")

autocompletion = WordCompleter(console.call_manuel())
history = FileHistory(f"{BASE}/.sesshstr")


def prompt(ppt):
    global autocompletion, history

    session = PromptSession(
        completer=autocompletion, 
        history=history
    )

    try:
        return session.prompt(ppt, auto_suggest=AutoSuggestFromHistory())
    except KeyboardInterrupt:
        printinf("Exiting")
        exit()
    except EOFError:
        printerr("Unexpected error in prompt")
        exit()


while True:
    cmd = ""
    from_queue = False

    if len(commands_queue) > 0:
        cmd = commands_queue.pop(0)
        from_queue = True
    else:
        env = console.get_currns()
        envcolor = "ansigreen"

        if "PRODUCTION" in env:
            envcolor = "ansired"
        elif "TEST" in env:
            envcolor = "ansiyellow"

        cmd = prompt(
            Echo.ansi(
                # Command string
                "".join([
                    "{%0%}",
                    f" - <{envcolor}>{{%1%}}</{envcolor}>",
                    "<ansiblue>{%2%}</ansiblue>"
                ]),
                # Replacements
                "oc.console",
                env,
                "\n $> "
            )
        )

    cmd = cmd.strip()
    argsvalid: bool = False
    args: list = []

    if cmd:
        try:
            args = parse_params(cmd)
        except ValueError as e:
            printerr(str(e))
            continue

        # Remove extra spaces
        args = array_clear(args)

        # The first element is always the command
        cmd = args.pop(0)
        argsvalid = len(args) >= 1

        cmdstring = cmd + " ".join(args)

        if from_queue:
            printinf(f"Auto-executing command '{cmdstring}'")
    else:
        continue

    try:
        console.save_history(cmd, args, argsvalid)

        # -------------------------
        # MANUAL
        # -------------------------
        if cmd in ["help", "manuel", "manuel!"]:
            # Display the manual for a specific command
            if argsvalid:
                console.get_help_for(args[0])
            else:
                console.get_help_for()

        # -------------------------
        # CLEAR OUTPUT
        # -------------------------
        elif is_scrambled(cmd, "clear") or cmd == "cls":
            system("clear")

        # -------------------------
        # PURGE
        # -------------------------
        elif argsvalid and cmd == "purge":
            if args[0] == "history":
                result = console.delete_history()

                if result == True:
                    printsuc("History successfully deleted")
                else:
                    printerr("Unable to delete commands history")
            elif args[0] == "note":
                try:
                    note = args[1]

                    console.delete_note(note)
                except IndexError:
                    printerr("No name was provided")

        # -------------------------
        # RELOAD-CONFIG
        # -------------------------
        elif cmd in ["reload-config", "reload-conf", "reload-env", "reload"]:
            printinf("Reading the configuration file..")

            globalcfg = console.get_config()

            printsuc("Configuration loaded")

        # -------------------------
        # GETTERS
        # -------------------------
        elif argsvalid and cmd == "show":
            # Show connection details
            if args[0] == "config":
                console.show_config(args[1:])

            # Show specific pod's details
            # oc explain pod
            elif args[0] == "pod":
                print("This feature is still in development")

            elif args[0] == "notes":
                console.show_notes()

        # -------------------------
        # SETTERS
        # -------------------------
        elif argsvalid and cmd == "set":
            # Required before login
            if args[0] == "host":
                try:
                    # TODO: fix this                    
                    index = int(args[1])
                    console.set_host(index)
                    send_command(["logout", "login via web"])
                except IndexError:
                    printerr("Please provide a host")
                    continue

            # Required to login
            elif args[0] == "credentials":
                console.set_credentials(args[1], args[2])

            elif args[0] == "username":
                console.set_username(args[1])

            elif args[0] == "password":
                console.set_password(args[1])

            # Set working environment
            elif args[0] == "namespace" or args[0] == "env":
                console.set_namespace(args[1])

            else:
                printalr(f"Command incomplete, please read the documentation for {cmd}")
                continue

            globalcfg = console.get_config()

        elif argsvalid and cmd == "add":
            if args[0] == "new":
                if args[1] == "host":
                    try:
                        console.add_host(args[2])
                    except IndexError:
                        printalr(f"Command incomplete please read the documentation for {cmd}")
                        continue

                elif args[1] == "note":
                    i = random.randint(0, 1000)

                    try:
                        if args[2]:
                            i = args[2]
                    except IndexError:
                        pass

                    console.spawn_nano(i)

        # -------------------------
        # LOGIN
        # -------------------------
        elif cmd == "login":
            params = {
                "token": None,
                "host": console.get_currhost(),
                "username": console.get_user(),
                "password": console.get_pasw(),
                "web": False
            }

            if argsvalid and args[0] == "with":
                it = iter(args[1:])
                for a in it:
                    if a in params:
                        tmp = next(it, params[a])

                        if tmp in params:
                            printerr(f"Missing value for '{a}'")
                            continue

                        params[a] = tmp
                    else:
                        printerr(f"Parameter not allowed: '{a}'")
            elif argsvalid and args[0] == "via":
                if args[1] == "web":
                    params["web"] = True

            status = console.oc.do_login(
                params["host"],
                params["username"],
                params["password"],
                params["token"],
                params["web"]
            )

            send_command(f"set namespace {console.oc.get_env()}")
            send_command("reload")

            console.oc.get_envs()

            if status != 0:
                printerr("Login failed during automated sequence")

                if from_queue:
                    printinf("Purging queue")
                    commands_queue.clear()
        
        # -------------------------
        # LOGOUT
        # -------------------------
        elif cmd == "logout" or cmd == "exit":
            console.oc.do_logout(cmd)

        # -------------------------
        # CONNECTION STATUS
        # -------------------------
        elif is_scrambled(cmd, "status") or cmd == "status":
            # TODO: change user status method
            console.oc.get_status()

        # -------------------------
        # LIST ENVS
        # -------------------------
        elif cmd in ["envs", "envs?", "namespaces"]:
            console.get_envs()

        # -------------------------
        # LIST PODS
        # 
        # List all the available pods
        # belonging to the current namespace
        # -------------------------
        elif cmd == "ls" or cmd == "pods":
            console.get_pods()

        # -------------------------
        # FIND
        # 
        # search for a specific pod
        # -------------------------
        elif cmd == "find":
            if argsvalid:
                console.get_pod(args[0])
            else:
                printalr(f"Command incomplete, please read the documentation for {cmd}")

        # -------------------------
        # ENTER
        # 
        # Start an interactive bash session 
        # for the requested pod
        # -------------------------
        elif cmd == "enter":
            if argsvalid:
                try:
                    console.spawn_bash(args[0])
                except KeyboardInterrupt:
                    continue
            else:
                printalr(f"Command incomplete, please read the documentation for {cmd}")

        # -------------------------
        # LOGS
        # 
        # Using stern
        # shows the selected pod's logs 
        # with a json notation
        # -------------------------
        elif cmd == "logs":
            if argsvalid:
                since: Union[str, None] = None
                save_logs: bool = False
                filename: Union[str, None] = None
                search_: Union[str, list, None] = None
                debug: bool = False

                options = [
                    "--since", 
                    "-T", 
                    "--debug", 
                    "-D", 
                    "--save-logs", 
                    ">", 
                    "--search", 
                    "-F"
                ]

                for i in range(1, len(args)):
                    a = args[i]

                    # as option
                    o = a
                    v = None

                    # options can be written as
                    # --option=value
                    if "=" in a:
                        o = a.split("=")[0]

                    if "--since" == o or "-T" == o:
                        try:
                            since = v

                            if v is None:
                                since = args[i+1]

                            # Example: --since 1h24m10s
                            matches = search(r"^(\d{1,2}[dhms]{1}){1,3}$", since)
                            if not matches:
                                printerr("--since value not valid")
                                continue
                        except IndexError:
                            printerr("--since value not found")

                    if "--debug" == o or "-D" == o:
                        debug = True

                    if "--save-logs" == o or ">" == o:
                        if v is None:
                            v = args[i+1]

                        save_logs = True

                        # save to a specified file
                        if v not in options:
                            filename = str(v).strip()
                    
                    if "--search" == o or "-F" == o:
                        try:
                            r = range(i+1, len(args))

                            if len(r) > 1:
                                search_ = []

                                for j in r:
                                    search_.append(args[j])
                            else:
                                if v is None:
                                    v = args[i+1]

                                search_ = v
                        except IndexError:
                            printerr("No filters passed to the --search parameter")

                console.oc.get_logs(
                    args[0],
                    since=since,
                    search=search_,
                    save_logs=save_logs,
                    debug=debug
                )
            else:
                printalr(f"Command incomplete, please read the documentation for {cmd}")

        # -------------------------
        # UPLOAD
        # -------------------------
        elif cmd == "upload":
            if argsvalid:
                check = console.verify_xload_args(args, len(args), 1)

                if len(args) == 2:
                    if check:
                        console.do_upload(_from=args[0], _to=args[1])
                    else:
                        printerr(f"Invalid command syntax :: {_line()}")
                elif len(args) == 3:
                    if check:
                        console.do_upload(
                            pod_name=args[0],
                            _from=args[1],
                            _to=args[2]
                        )
                    else:
                        printerr(f"Invalid command syntax :: {_line()}")
            else:
                printerr(f"Command incomplete, please read the documentation for {cmd}")

        # -------------------------
        # DOWNLOAD
        # -------------------------
        elif cmd == "download":
            if argsvalid:
                exclude_list = []
                flag = has(args, ["--except", "--exclude"])

                if flag != False:
                    i = args.index(flag)
                    exclude_list = args[i+1:]
                    args = args[0:i]

                check = console.verify_xload_args(args, len(args), 2)

                if check:
                    if len(args) == 2:
                        console.do_download(
                            _from=args[0], 
                            _to=args[1], 
                            exclude_list=exclude_list
                        )
                    elif len(args) == 3:
                        console.do_download(
                            pod_name=args[0],
                            _from=args[1],
                            _to=args[2],
                            exclude_list=exclude_list
                        )
                else:
                    raise InvalidSyntaxError(f"Invalid command syntax :: {_line()}")
            else:
                raise InvalidSyntaxError(f"Command incomplete, please read the documentation for {cmd}")

        # -------------------------
        # UPLOAD-POD2POD
        #
        # Move a file from a pod to another
        # -------------------------
        elif cmd == "upload-pod2pod":
            if argsvalid:
                check = console.verify_xload_args(args, len(args), 3)

                if len(args) == 2:  
                    if check:
                        console.do_pod2pod_transfer(args[0], args[1])
                    else:
                        printerr(f"Invalid command syntax :: {_line()}")
            else:
                printerr(f"Command incomplete, please read the documentation for {cmd}")
        else:
            if not (not cmd):
                printerr(f"Command not recognized: {cmd}")

    except InvalidSyntaxError as ise:
        printalr(ise)

    except KeyboardInterrupt as ki:
        console.oc.do_logout("exit")
