#!/usr/bin/python

from subprocess import Popen, run, PIPE, CalledProcessError
from os.path import dirname, isfile
from os import symlink, unlink
from typing import Union
from re import search, sub
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
                set-host: Save the host to login to
                currhost: Show the current host
                login: Log in using your saved credentials (required before executing other commands)
                upload: Upload a file to a specified pod
                download: Download a file from a specified pod
                upload-pod2pod: Move a file from one pod to another
                find: Locate a pod
                logs: Show logs from a pod in real time
                use-env: Switch between work environments
                currenv: Show the current working environment
                enter: Access a specified pod

            For more details, use: help {COMMAND}
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
                --pod {POD}[optional] or default (uses the last accessed pod)
                --from {path/to/file}, the path to the file you want to upload
                --to {path/to/destination}, the destination path in the pod

            Example:
                upload --from /path/to/somefile.pdf --to /path/to/destination
                upload --pod default --from /path/to/somefile.pdf --to /path/to/destination
        """,
        "download": """Download a file from a specified pod.
            Usage:
                --pod {POD}[optional] or default (uses the last accessed pod)
                --from {path/to/file}, the path to the file in the pod
                --to {path/to/destination}, the local destination path for the downloaded file

            Example:
                download --from /path/to/somefile.pdf --to ~/Downloads
                download --pod default --from /path/to/somefile.pdf --to ~/Downloads
        """,
        "upload-pod2pod": """Move a file from a {POD} to another
            Usage:
                --from {POD}:{path/to/file}
                --to {POD}:{path/to/destination}

            Example:
                upload-pod2pod --from pod-name-1:/path/to/file.php --to pod-name-2:/path/to/destination/
        """
    }

    POD_AND_FILE_REGEX = r"([\w\/-]+):([\w\/-]+)(\.[\w]{1,5})*"
    FILE_REGEX = r"([\w\/-]+)(\.[\w]{1,5})*"
    POD_REGEX = r"([\w\/-]+):"

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
                row += cmd + " " + " ".join(args)

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

    def get_currpod(self):
        with open(f"{PARENT}/.currpod", "r") as currpod:
            return currpod.readline()

    def do_upload(self, _from: str, _to: str, pod_name: str = "default"):
        try:
            if pod_name == "default":
                pod_name = self.get_currpod()

            if not pod_name:
                print("No valid pod to upload to.\nPlease specify one")
                return

            print(f"Now uploading: {_from}...\n")
            run(["oc", "cp", _from, f"{pod_name}:{_to}"])
        except Exception as e:
            print(e)
        finally:
            print("Process completed\n\n")

    def do_download(self, _from: str, _to: str, pod_name: str = "default"):
        try:
            if pod_name == "default":
                pod_name = self.get_currpod()

            if not pod_name:
                print("No valid pod to download from.\nPlease specify one")
                return

            print(f"Now downloading: {_from} to {_to}...\n")
            run(["oc", "rsync", f"{pod_name}:{_from}", _to])
        except Exception as e:
            print(e)
        finally:
            print("Process completed\n\n")

    def do_pod2pod_transfer(self, _from: str, _to: str):
        print(f"Starting transfer from {_from} to {_to}")
        pod1 = search(self.POD_REGEX, _from).group(0).replace(":", "")
        pod2 = search(self.POD_REGEX, _to).group(0).replace(":", "")

        path1 = sub(self.POD_REGEX, "", _from)
        # extract filename
        file1 = path1.split("/")[-1]
        path2 = sub(self.POD_REGEX, "", _to)

        print(f"Downloading {_from} locally...\n")
        """ example usage:
                upload-pod2pod --from pod-name-1:/path/to/file.php --to pod-name-2:/path/to/destination/
        """
        self.do_download(path1, ".", pod1)
        print(f"Uploading {_from} to {_to}...\n")
        self.do_upload(file1, path2, pod2)

        # deleting the downloaded file
        try:
            print("Deleting locally downloaded files...")
            unlink(file1)
        except FileNotFoundError:
            print(f"File not found: {file1}.\nMaybe it wasn't downloaded?")
        finally:
            print("Process completed\n\n")

    def verify_xload_args(self, args: list, argslen: int, xload_type: int):
        pods = self.commands.get_pods_list()

        if xload_type == 1 or xload_type == 2:
            if argslen == 2:
                # expecting paths only
                for a in args:
                    file = search(self.FILE_REGEX, a)

                    if a in pods:
                        return False
                    elif not file.group(0):
                        return False
                return True
            elif argslen == 3:
                # expecting the pod name as first parameter
                if args[0] in pods:
                    # expected syntax: /path/to/file for both parameters
                    """ examples:
                            /upload/path/to/file.pdf
                            /upload/path/to/file.tar.gz.zip
                    """
                    file1 = search(self.FILE_REGEX, args[1])
                    file2 = search(self.FILE_REGEX, args[2])

                    if file1.group(0) and file2.group(0):
                        return True
            return False
        elif xload_type == 3:
            if argslen == 2:
                # expected syntax: pod_name:/path/to/file for both parameters
                """ examples:
                        pod-name-randnum1234155:/upload/path/to/file.pdf
                        pod-name-randnum1234155:/upload/path/to/file.tar.gz.zip
                """
                pod1 = search(self.POD_AND_FILE_REGEX, args[0])
                pod2 = search(self.POD_AND_FILE_REGEX, args[1])

                if pod1.group(0) in pods and pod2.group(0) in pods:
                    return True
            return False
