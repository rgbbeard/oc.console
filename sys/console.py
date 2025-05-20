#!/usr/bin/python

from subprocess import Popen, run, PIPE, CalledProcessError
from os.path import dirname, isfile
from os import symlink, unlink
from typing import Union
from re import search, sub
from oc_deps_manager import OCDepsManager

BASE = dirname(__file__)
PARENT = f"{BASE}/.."
FILE_REGEX = r"([\w\/-]+)(\.[\w]{1,5})*"
POD_REGEX = r"([\w\/-]+):"
POD_AND_FILE_REGEX = POD_REGEX + FILE_REGEX

# load the Formatter class
fmttr = OCDepsManager.module_from_path(f"{BASE}/formatter.py")
Formatter = fmttr.Formatter

# load the Commands class
cmds = OCDepsManager.module_from_path(f"{BASE}/commands.py")
Commands = cmds.Commands


class Console:
    commands: Commands = None

    __manuel: dict = {
        "help": """Displays details about this program.
            You can also use `help {command}` to get more information on a specific command.
        """,
        "manuel": "Alias of help",
        "manuel!": "Alias of help",
        "login": """Log into OpenShift using your credentials.
            A `.host` file with the host address is required. Use `set-host` to create it.
        """,
        "set-credentials": """Save your login credentials.
            This command requires the path to the file containing the login credentials.
            The file should contain only the username and password, each on a separate line.

            Usage:
                set-credentials /path/to/credentials.txt
        """,
        "set-credentials-path": "Alias of set-credentials.",
        "set-host": """Save the host to login to.

            Usage:
                set-host http(s)://domain.example
        """,
        "currhost": "Displays the host that's currently in use.",
        "host?": "Alias of currhost.",
        "host": "Alias of currhost.",
        "find": "Find a pod by full or partial name.",
        "ls": "Alias of find.",
        "logs": """Displays the logs for the requested pod.

            Usage:
                logs {pod-name} [--debug] [--save-logs] [--since 1h2m3s] [--search filter1 filter2 ...]

            Notes:
                --since defaults to 30m if not provided.
                --search must be used at the end.
                --save-logs is currently disabled.
        """,
        "enter": """Enter the pod's console.

            Usage:
                enter pod-name

            Notes:
                The accessed pod is saved inside the `.currpod` file.
        """,
        "envs": "List all available OpenShift projects (requires `oc projects` or `login`).",
        "use-env": """Switch to the requested OpenShift project.

            Usage:
                use-env project-name

            Notes:
                Automatically detects work environment if name ends with `dev` or `prod`.
        """,
        "currenv": "Displays the current work environment.",
        "env?": "Alias of currenv.",
        "env": "Alias of currenv.",
        "upload": """Uploads a file to a pod.

            Method 1:
                upload /path/to/source/file /path/to/destination/folder

            Method 2:
                upload pod-name /path/to/source/file /path/to/destination/folder

            Notes:
                If pod is not specified, the `.currpod` file will be used.
        """,
        "download": """Downloads a file from a pod.

            Method 1:
                download /path/to/source/file /path/to/destination/folder

            Method 2:
                download pod-name /path/to/source/file /path/to/destination/folder

            Notes:
                If pod is not specified, the `.currpod` file will be used.
        """,
        "upload-pod2pod": """Copy a file from one pod to another.

            Usage:
                upload-pod2pod pod1:/path/to/file pod2:/path/to/destination/
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
                row += cmd + " " + " ".join(args)

            history.write(row)

    def get_help_for(self, cmd: str = ""):
        if not (not cmd) and self.__manuel.get(cmd):
            print(f"Manual for {cmd}:")
            print(self.__manuel.get(cmd))

    def get_logs(
        self, 
        pod_name: str = None, 
        since: str = "30m", 
        save_logs: bool = False,
        search: Union[str, list] = None,
        debug: bool = False
    ):
        if not since:
            since = "30m"
        
        # Ensure pod_name is valid
        if pod_name and self.__is_pod(pod_name):
            cmd = ["stern", pod_name, "--since", since]
            
            # Debug output
            if debug:
                print(
                    f"Query: {' '.join(cmd)}\n",
                    "Params:\n",
                    f"pod_name: {pod_name}\n",
                    f"since: {since}\n",
                    f"save_logs: {save_logs}\n",
                    f"search: {[type(search), search]}\n"
                )
                pass

            try:
                process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=False)
                output = process.stdout

                # filter with one or more keywords
                if search is not None and (isinstance(search, str) or len(search) > 0):
                    for line in output:
                        line = line.decode('utf-8').strip()

                        if isinstance(search, str):
                            if search in line:
                                print(Formatter.format_log(line))

                        # filter by multiple keywords   
                        elif isinstance(search, list):
                            if all(keyword in line for keyword in search):
                                print(Formatter.format_log(line))
                else:
                    # Output the logs directly if no search filter
                    for line in process.stdout:
                        l = line.decode('utf-8').strip()
                        print(Formatter.format_log(l))
            except CalledProcessError as e:
                print(f"Error occurred: {e}")
            except KeyboardInterrupt:
                print("\n\nOkay, bye!")
        else:
            print("Invalid pod name")

    def __is_pod(self, pod_name: str = "") -> bool:
        pods = self.commands.get_pods_list()

        for pod in pods:
            if pod_name in pod:
                return True
        return False

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

    def do_upload(
        self, 
        _from: str, 
        _to: str, 
        pod_name: str = "default"
    ):
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

    def do_download(
        self, 
        _from: str, 
        _to: str, 
        pod_name: str = "default"
    ):
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
        pod1 = search(POD_REGEX, _from).group(0).replace(":", "")
        pod2 = search(POD_REGEX, _to).group(0).replace(":", "")

        path1 = sub(POD_REGEX, "", _from)
        # extract filename
        file1 = path1.split("/")[-1]
        path2 = sub(POD_REGEX, "", _to)

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

    def verify_xload_args(
        self, 
        args: list, 
        argslen: int, 
        xload_type: int
    ) -> bool:
        valid = False
        pods = self.commands.get_pods_list()

        # upload and download
        if xload_type == 1 or xload_type == 2:
            if argslen == 2:
                # expecting paths only
                for a in args:
                    file = search(FILE_REGEX, a)

                    if a in pods:
                        valid = False
                    elif not file.group(0):
                        valid = False
                valid = True
            elif argslen == 3:
                # expecting the pod name as first parameter
                if args[0] in pods:
                    # expected syntax: /path/to/file for both parameters
                    """ examples:
                            /upload/path/to/file.pdf
                            /upload/path/to/file.tar.gz.zip
                    """
                    file1 = search(FILE_REGEX, args[1])
                    file2 = search(FILE_REGEX, args[2])
                    print(file1.group(0))
                    print(file2.group(0))
                    if file1.group(0) and file2.group(0):
                        valid = True
        # upload-pod2pod
        elif xload_type == 3:
            if argslen == 2:
                # expected syntax: pod_name:/path/to/file for both parameters
                """ examples:
                        pod-name-randnum1234155:/upload/path/to/file.pdf
                        pod-name-randnum1234155:/upload/path/to/file.tar.gz.zip
                """
                pod1 = search(POD_AND_FILE_REGEX, args[0])
                pod2 = search(POD_AND_FILE_REGEX, args[1])

                if pod1.group(0) in pods and pod2.group(0) in pods:
                    valid = True
        return valid
