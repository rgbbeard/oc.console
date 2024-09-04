#!/usr/bin/python

from subprocess import Popen, PIPE, run
from os.path import dirname, isfile, islink
from os import symlink, unlink
from sys import path
import importlib.util

BASE = dirname(__file__)
PARENT = f"{BASE}/.."

# load the Commands class
spec = importlib.util.spec_from_file_location("c", f"{BASE}/commands.py")
cmds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmds)
Commands = cmds.Commands


class Console:
    commands: Commands = None

    __manuel: dict = {
        "help": """Interactive console interface for easier use of the OpenShift Client.
            Commands:
                help: Display this help message
                set-credentials: Save your login credentials (required before logging in)
                login: Log in using your saved credentials (required before executing other commands)
                upload: Upload a file to a specified pod
                download: Download a file from a specified pod
                find: Locate a pod
                use-env: Switch between work environments
                enter: Access a specified pod

            For more details use: help {COMMAND}
        """,
        "manuel!": "Alias of help",
        "manuel": "Alias of help",
        "login": """Log in to the OpenShift Client using your credentials. 
            An .ochost file with the host address is required.
        """,
        "set-host": """Save the host to login to.
            Usage:
                set-host http://host.example
        """,
        "currhost": "Show the host that's currently in use.",
        "host?": "Alias of currhost.",
        "host": "Alias of currhost.",
        "set-credentials": """Save your login credentials.
            This command requires the path to the file containing the login credentials.
            The file should contain only the username and password, each on a separate line.

            Usage:
                set-credentials {PATH}
        """,
        "set-credentials-path": "Alias of set-credentials",
        "find": "Locate a pod.",
        "ls": "Alias of find",
        "logs": """Shows the pod logs in real time.
            Usage:
                logs {POD} --since {TIME}
        """,
        "enter": """Access a pod.
            You can specify the pod you want to enter, or if no name is provided, the last accessed pod will be used.
            Usage:
                enter {POD}
        """,
        "use-env": """Switch between work environments.
            Usage:
                use-env {ENVIRONMENT}
        """,
        "currenv": "Show the current working environment.",
        "env?": "Alias of currenv.",
        "env": "Alias of currenv.",
        "upload": """Upload a file to a specified pod.
            Usage:
                --pod {POD} or default (uses the last accessed pod)
                --from {path/to/file}, the path to the file you want to upload
                --to {path/to/destination}, the destination path in the pod

            Example:
                upload --pod default --from /path/to/somefile.pdf --to /path/to/destination
        """,
        "download": """Download a file from a specified pod.
            Usage:
                --pod {POD} or default (uses the last accessed pod)
                --from {path/to/file}, the path to the file in the pod
                --to {path/to/destination}, the local destination path for the downloaded file

            Example:
                download --pod default --from /path/to/somefile.pdf --to ~/Downloads
        """,
        "upload-pod2pod": """***Coming soon***
            Move a file from a pod to another
        """
    }

    def __init__(self):
        self.commands = Commands()

    def call_manuel(self):
        return self.__manuel.keys()

    def save_history(self, cmd, args, argsvalid):
        with open(f"{PARENT}/.sesshstr", "a") as history:
            row = "\n"

            if not argsvalid:
                row += cmd
            else:
                row += " ".join(args)

            history.write(row)

    def get_help_for(self, cmd: str = ""):
        if not (not cmd) and self.__manuel.get(cmd):
            print(f"Manual for {cmd}:")
            print(self.__manuel.get(cmd))

    def get_logs(self, pod_name: str = "", _since: str = "30m"):
        if not _since:
            _since = "30m"

        if self.__is_pod(pod_name):
            run(["stern", f"{pod_name}", "--since", _since])
        else:
            print("Invalid pod name")

    def __is_pod(self, pod_name: str = ""):
        pods = self.commands.get_pods_list()

        print(pod_name in pods)
        exit()

        return True if pod_name in pods else False

    def get_pods(self):
        pods = self.commands.get_pods_list()

        for pod in pods:
            print(pod)

    def get_pod(self, pod_name: str = ""):
        pods = self.commands.get_pods_list()

        tmp = []

        for pod in pods:
            if pod_name in pod:
                tmp.append(pod)

        for t in tmp:
            print(t)

        if not pods:
            print("No pod found.")

    def set_credentials_path(self, credentials_path: str = ""):
        print("Now checking the path you entered...")

        if isfile(credentials_path):
            print("The file you provided is valid!")
            print("Saving credentials...")

            self.__create_link(credentials_path)

            print("Done")

            self.commands.do_login()
        else:            
            print("The provided file is not valid")

    def __create_link(self, credentials_path: str = ""):
        try:
            symlink(credentials_path, f"{BASE}/.credentials")
        except FileExistsError:
            print("Configuration file already exists")
            unlink(f"{PARENT}/.credentials")
            self.__create_link(credentials_path)

    def set_host(self, host_name: str = ""):
        if not (not host_name):
            with open(f"{PARENT}/.ochost", "w") as file:
                file.write(host_name)
        else:
            print("The given host name is not valid")

    def get_host(self):
        if isfile(f"{PARENT}/.ochost"):
            with open(f"{PARENT}/.ochost", "r") as file:
                print(f"Currently using host: {file.readline()}")
        else:
            print("Missing host file. Use 'set-host {HOST}' first")

    def get_envs(self):
        for c in self.commands.get_envs():
            print(c)

    # TODO: complete these features
    def do_upload(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)

    def do_download(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)

    def do_pod2pod_transfer(self, _from: str, _to: str):
        print(_from, _to)

    def verify_xload_args(self, args: list, argslen: int, xload_type: int):
        pods = self.get_pods_list()

        if xload_type == 1:
            if argslen == 2:
                # expecting paths only
                for a in args:
                    if a in pod:
                        return False
                return True
            elif argslen == 3:
                # expecting the pod name as first parameter
                pass
            else: return False
        elif xload_type == 2:
            if argslen == 2:
                # only paths should have been passed
                pass
            elif argslen == 3:
                # expecting the pod name as first parameter
                pass
            else: return False
        elif xload_type == 3:
            if argslen == 2:
                # expected syntax: pod_name:/path/to/file for both parameters
                pass
            else: return False
