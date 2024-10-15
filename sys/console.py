#!/usr/bin/python

from subprocess import Popen, PIPE, check_output, CalledProcessError
from os.path import dirname, isfile, islink
from os import symlink, unlink
from sys import path
from typing import Union
from re import search
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

    def get_logs(
        self, 
        pod_name: str = None, 
        _since: str = "30m", 
        save_logs: bool = False,
        search: Union[str, list] = None,
        debug: bool = False
    ):
        if not _since:
            _since = "30m"
        
        # Ensure pod_name is valid
        if pod_name and self.__is_pod(pod_name):
            cmd = ["stern", pod_name, "--since", _since]
            
            # Debug output
            if debug:
                print(
                    f"Query: {' '.join(cmd)}\n",
                    "Params:\n",
                    f"pod_name: {pod_name}\n",
                    f"_since: {_since}\n",
                    f"save_logs: {save_logs}\n",
                    f"search: {[type(search), search]}\n"
                )
                return

            try:
                process = Popen(cmd, stdout=PIPE)
                output = process.stdout

                # filter with one or more keywords
                if search is not None and (isinstance(search, str) or len(search) > 0):
                    for line in output:
                        line = line.decode('utf-8').strip()

                        if isinstance(search, str):
                            if search in line:
                                print(line)

                        # filter by multiple keywords   
                        elif isinstance(search, list):        
                            if all(keyword in line for keyword in search):
                                print(line)
                else:
                    # Output the logs directly if no search filter
                    for line in process.stdout:
                        print(line.decode('utf-8').strip())
            except CalledProcessError as e:
                print(f"Error occurred: {e}")
            except KeyboardInterrupt:
                print("\n\nOkay, bye!")
        else:
            print("Invalid pod name")

    def __is_pod(self, pod_name: str = ""):
        pods = self.commands.get_pods_list()

        for pod in pods:
            if pod_name in pod:
                return True

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

        if xload_type == 1 or xload_type == 2:
            if argslen == 2:
                # expecting paths only
                for a in args:
                    if a in pod:
                        return False
                return True
            elif argslen == 3:
                # expecting the pod name as first parameter
                if args[0] in pods:
                    if args[1] in pods or args[2] in pods:
                        return False
                    return True
            return False
        elif xload_type == 3:
            if argslen == 2:
                # expected syntax: pod_name:/path/to/file for both parameters
                """ example:
                        pod-name-randnum1234155:/upload/path/to/file.pdf
                        pod-name-randnum1234155:/upload/path/to/file.tar.gz.zip
                """
                pod1 = search(r"([\w\/-]+):([\w\/-]+)(\.[\w]{1,5})*", args[0])
                pod2 = search(r"([\w\/-]+):([\w\/-]+)(\.[\w]{1,5})*", args[1])

                if pod1.group(0) in pods and pod2.group(0) in pods:
                    return True
            return False