#!/usr/bin/python

from typing import Union
from subprocess import run
from os.path import dirname, isfile, isdir, exists
from os import symlink, unlink, makedirs
from re import search, sub
from base64 import b64encode, b64decode
from oc_deps_manager import OCDepsManager
from utilities import (
    printerr, 
    printinf, 
    printsuc, 
    printalr, 
    is_empty,
    is_empty
)
from echo import Echo

BASE = dirname(__file__)
PARENT = f"{BASE}/.."

FILE_REGEX = r"([\w\/-]+)(\.[\w]{1,5})*"
POD_REGEX = r"([\w\/-]+):"
POD_AND_FILE_REGEX = POD_REGEX + FILE_REGEX

CFGFILE = f"{PARENT}/config.json"

SESSION_HISTORY = f"{PARENT}/.sesshstr"

# load the OpenShift class
cmds = OCDepsManager.module_from_path(f"{BASE}/openshift.py")
OpenShift = cmds.OpenShift

# load the json manager class
jsm = OCDepsManager.module_from_path(f"{PARENT}/json_maid.py")
JSONMaid = jsm.JSONMaid

# load the json manager class
kt = OCDepsManager.module_from_path(f"{PARENT}/krypto.py")
Krypto = kt.Krypto


class Console:
    _default_dirmode = 0o777
    oc: OpenShift = None
    jsm: JSONMaid = None
    kt: Krypto = None
    cfg = dict()

    _manuel: dict = {
        "help": """
            Displays general help for the console 
            or the manual for a specific command. 
            This command has aliases **manuel** and **manuel!**.

            **Usage:**
                * `help`
                * `help <command_name>`

            **Arguments:**
                * **<command_name>**: Optional. 
                The specific command to get help for.
        """,
        "clear": """
            Clears the console screen. This command has the alias **cls**.

            **Usage:**
                * `clear`
        """,
        "exit": """
            Exits the console application.

            **Usage:**
                * `exit`
        """,
        "reload-config": """
            Reloads the configuration file into the console, 
            refreshing all stored settings.

            **Usage:**
                * `reload-config`
        """,
        "show": """
            Displays various configurations or settings.

            **Usage:**
                * `show config all`
                * `show config <key1> [<key2> ...]`

            **Arguments:**
                * **config**: Keyword to indicate configuration values are requested.
                * **all**: Subcommand for 'config'. 
                Displays all available configuration values.
                * **<key1> [<key2> ...]**: Subcommands for 'config'. 
                Displays the values for the specified configuration keys.
        """,
        "set": """
            Sets configuration parameters (host, credentials) 
            or the working environment.

            **Usage:**
                * `set host <value>`
                * `set credentials <value>`
                * `set env <value>`

            **Arguments:**
                * **host <value>**: Sets the host configuration.
                * **credentials <value>**: Sets the credentials configuration.
                * **env <value>**: Sets the working environment (e.g., namespace).
        """,
        "login": """
            Authenticates the user using the configured host and credentials.

            **Usage:**
                * `login`
        """,
        "logout": """
            Invalidates the current session and logs the user out.

            **Usage:**
                * `logout`
        """,
        "envs": """
            Lists all available environments (namespaces/contexts). 
            This command has the alias **envs?**.

            **Usage:**
                * `envs`
        """,
        "ls": """
            Lists all available pods. This command has the alias **pods**.

            **Usage:**
                * `ls`
        """,
        "find": """
            Searches for and displays information about a specific pod.

            **Usage:**
                * `find <pod_name>`

            **Arguments:**
                * **<pod_name>**: The name of the pod to find.
        """,
        "enter": """
            Spawns a bash shell inside the specified pod.

            **Usage:**
                * `enter <pod_name>`

            **Arguments:**
                * **<pod_name>**: The name of the target pod.
        """,
        "logs": """
            Displays the logs for a specified pod, 
            with optional filtering and saving.

            **Usage:**
                * `logs <pod_name>`
                * `logs <pod_name> 
                    [--since <duration>] 
                    [--search <filter>] 
                    [--save-logs] 
                    [--debug]`

            **Arguments:**
                * **<pod_name>**: The name of the target pod.
                * **--since <duration>**: Optional. 
                Show logs since a relative duration (e.g., '1h24m10s').
                * **--search <filter>**: Optional. 
                Filter logs based on search terms (supports multiple terms).
                * **--save-logs**: Optional. 
                Flag to save the retrieved logs.
                * **--debug**: Optional. 
                Flag to enable debug logging.
        """,
        "upload": """
            Uploads a file from the local machine to a specified path inside a pod.

            **Usage:**
                * `upload <local_path> <remote_path>` 
                (Assumes a default/current pod context)
                * `upload <pod_name> <local_path> <remote_path>`

            **Arguments:**
                * **<pod_name>**: Optional. 
                The name of the target pod.
                * **<local_path>**: The path to the file on the local machine.
                * **<remote_path>**: The path to the destination inside the pod.
        """,
        "download": """
            Downloads a file from a specified path inside a pod to the local machine.

            **Usage:**
                * `download <remote_path> <local_path>` 
                (Assumes a default/current pod context)
                * `download <pod_name> <remote_path> <local_path>`

            **Arguments:**
                * **<pod_name>**: Optional. The name of the source pod.
                * **<remote_path>**: The path to the file inside the pod.
                * **<local_path>**: The path to the destination on the local machine.
        """,
        "upload-pod2pod": """
            Transfers a file between two different pods.

            **Usage:**
                * `upload-pod2pod <source_pod> <destination_pod>`

            **Arguments:**
                * **<source_pod>**: The name of the pod to copy the file 
                from (and likely the path within it).
                * **<destination_pod>**: The name of the pod to copy the file 
                to (and likely the path within it).
        """
    }

    def __init__(self):
        self.oc = OpenShift()
        self.jsm = JSONMaid(CFGFILE)
        self.kt = Krypto()

        cfg = self.get_config()
        self.cfg = cfg

        if is_empty(cfg.get("host", "")):
            print("No host found")

            try:
                done = False
                host: str = ""

                while not done:
                    host = input("Enter host: ")
                    if not is_empty(host):
                        host = self.kt.encrypt(host.strip())
                        host = b64encode(host).decode('utf-8')

                    done = not is_empty(host)

                cfg["host"] = host
            except KeyboardInterrupt as ki:
                printerr("Setup aborted")
                exit()
            except Exception as e:
                print(e)

        if is_empty(cfg.get("credentials", "")):
            print("No credentials found")

            try:
                done = False
                username: str = ""
                password: str = ""

                while not done:
                    username = input("Enter username: ")
                    if not is_empty(username):
                        username = self.kt.encrypt(username.strip())
                        username = b64encode(username).decode('utf-8')

                        password = input("Enter password: ")
                        if not is_empty(password):
                            password = self.kt.encrypt(password.strip())
                            password = b64encode(password).decode('utf-8')

                    done = not is_empty(username) and not is_empty(password)

                cfg["credentials"] = [username, password]
            except KeyboardInterrupt as ki:
                printerr("Setup aborted")
                exit()
            except Exception as e:
                print(e)

        self.save_and_reload(cfg)

    def save_and_reload(self, data: dict):
        self.jsm.update_record(self.cfg, data)
        self.cfg = self.get_config()

    def call_manuel(self):
        return self._manuel.keys()

    def save_history(self, cmd, args, argsvalid):
        global SESSION_HISTORY

        with open(SESSION_HISTORY, "a") as history:
            row = "\n"

            if not argsvalid:
                row += cmd
            else:
                row += cmd + " " + " ".join(args)

            history.write(row)

    def delete_history(self) -> bool:
        global SESSION_HISTORY

        try:
            with open(SESSION_HISTORY, "w") as history:
                history.write("")

            return True
        except FileNotFoundError as e:
            printerr("Unable to clear commands history")
            print(e)
            
            return False

    def _save_env(self, e: str):
        if "dev" in e:
            env = f"{e} (DEVELOPMENT)"
        elif "preprod" in e or "test" in e:
            env = f"{e} (TEST)"
        elif "prod" in e:
            env = f"{e} (PRODUCTION)"

        cfg = self.get_config()
        cfg["namespace"] = env
        self.save_and_reload(cfg)

        return True

    # -------------------------
    # SETTERS
    # -------------------------
    def set_credentials(self, username: str, password: str):
        if not is_empty(username):
            username = self.kt.encrypt(username.strip())
            username = b64encode(username).decode('utf-8')
        else:
            printerr("The given username is not valid")
            return False

        if not is_empty(password):
            password = self.kt.encrypt(password.strip())
            password = b64encode(password).decode('utf-8')
        else:
            printerr("The given password is not valid")
            return False

        cfg = self.get_config()
        cfg["credentials"] = [username, password]
        self.save_and_reload(cfg)

        return True

    def set_username(self, username: str):
        if not is_empty(username):
            username = self.kt.encrypt(username.strip())
            username = b64encode(username).decode('utf-8')
        else:
            printerr("The given username is not valid")
            return False

        cfg = self.get_config()
        cfg["credentials"][0] = username
        self.save_and_reload(cfg)

        return True

    def set_password(self, password: str):
        if not is_empty(password):
            password = self.kt.encrypt(password.strip())
            password = b64encode(password).decode('utf-8')
        else:
            printerr("The given password is not valid")
            return False

        cfg = self.get_config()
        cfg["credentials"][1] = password
        self.save_and_reload(cfg)
        
        return True

    def set_host(self, host: str):
        if not is_empty(host):
            host = self.kt.encrypt(host.strip())
            host = b64encode(host).decode('utf-8')
        else:
            printerr("The given host name is not valid")
            return False

        cfg = self.get_config()
        cfg["host"] = host
        self.save_and_reload(cfg)
        
        return True

    def set_namespace(self, e: str):
        if is_empty(e):
            printerr("No environment passed")
            return False

        if is_empty(self.oc.envs):
            printalr("No environments found, try logging in first")
            return False

        e = e.strip()

        if e in self.oc.envs:
            self.oc.set_env(e)

            self._save_env(e)
        else:
            printerr("Environment not found")
            print("Use 'envs' to show the available environments")
            return False
        
        return True

    # -------------------------
    # GETTERS
    # -------------------------
    def get_help_for(self, cmd: str = ""):
        if not is_empty(cmd) and self._manuel.get(cmd):
            print(f"Manual for {cmd}:")
            print(self._manuel.get(cmd))
        else:
            print("Manual for oc.console\n\n")
            for key in self._manuel:
                value = self._manuel.get(key)

                print(f"{key}: {value}\n")
    
    def get_config(self):
        try:
            return self.jsm.get_record(0)
        except Exception as e:
            raise e

    def show_config(self, args):
        config = self.get_config()

        if args[0] == "all":
            printinf("Current configuration is:")

            for a in config:
                v = config.get(a)

                printstr = f"Parameter {a} is: "

                if isinstance(v, list):
                    for b in v:
                        bd = self.get_cleanvalue(b)

                        if bd is None:
                            print(printstr + bd)
                        else:
                            print(printstr + b)
                else:
                    v = self.get_cleanvalue(v)

                    if v is None:
                        v = config.get(a)

                    print(printstr + v)

        # Specific values
        else:
            for a in args[0:]:
                if a in config:
                    printinf("Showing configuration for {a}:")

                    v = config.get(a)

                    if isinstance(v, list):
                        for b in v:
                            bd = self.get_cleanvalue(b)

                            if bd is None:
                                print(bd)
                            else:
                                print(b)
                    else:
                        v = self.get_cleanvalue(v)

                        if v is None:
                            v = config.get(a)

                        print(v)

    def get_cleanvalue(self, data) -> Union[str, None]:
        try:
            d = b64decode(data)
            return self.kt.decrypt(d).decode('utf-8')
        except Exception:
            return None

    def get_currhost(self) -> Union[str, None]:
        return self.get_cleanvalue(self.get_config()["host"])

    def get_user(self) -> Union[str, None]:
        return self.get_cleanvalue(self.get_config()["credentials"][0])

    def get_pasw(self) -> Union[str, None]:
        return self.get_cleanvalue(self.get_config()["credentials"][1])

    def get_currpod(self) -> Union[str, None]:
        return self.get_config()["pod"]

    def get_currns(self) -> Union[str, None]:
        ns = self.get_config()["namespace"]

        if ns is not None:
            printinf(f"Currently using namespace: {ns}")
        else:
            printint("No specific namespace used recently")

    def get_pods(self):
        pods = self.oc.get_pods_list()

        for pod in pods:
            print(pod)

    def get_pod(self, pod_name: str):
        if is_empty(pod_name):
            printalr("No pod name specified")
            return

        pods = self.oc.get_pods_list()

        tmp = []

        for pod in pods:
            if pod_name in pod:
                tmp.append(pod)

        for t in tmp:
            print(t)

        if not pods:
            printalr("No pod found.")

    def get_envs(self):
        for c in self.oc.get_envs():
            print(c)

    def get_currenv(self) -> Union[str, None]:
        env = self.get_config()["env"]

        if env is not None:
            printinf(f"Currently using environment: {env}")
        else:
            printint("Couldn't detect any recently used environment")

    # -------------------------
    # ACTIONS
    # -------------------------
    def spawn_bash(self, pod_name: str = "default"):
        try:
            if pod_name == "default":
                    pod_name = self.get_currpod()

            if is_empty(pod_name):
                printalr("No pod specified, looking for the last accessed pod..")

                pod_name = self.get_currpod()


            if is_empty(pod_name):
                printerr("No pod found")
                return

            self.oc.start_session(pod_name)
        except Exception:
            printerr(f"An unexpected error occurred while accessing pod {pod_name}")

    def do_upload(self, _from: str, _to: str, pod_name: str = "default"):
        try:
            if pod_name == "default":
                pod_name = self.get_currpod()

            if not pod_name:
                printerr("No valid pod to upload to.")
                print("Please specify one")
                return False

            printinf(f"Now uploading: {_from}...\n")
            run(["oc", "cp", _from, f"{pod_name}:{_to}"])
        except Exception as e:
            printerr(str(e))
            return False
        finally:
            printsuc("Process completed\n\n")
            return True

    def do_download(self, _from: str, _to: str, pod_name: str = "default"):
        try:
            if pod_name == "default":
                pod_name = self.get_currpod()

            if not pod_name:
                printerr("No valid pod to download from.")
                print("Please specify one")
                return False

            # Validating destination
            if not exists(_to):
                printalr("The destination does not exist")

                try:
                    printinf("Creating destination directory")
                    makedirs(_to, self._default_dirmode)

                except Exception:
                    printerr("Failed to create destination directory")
                    return False

            if not isdir(_to):
                printerr("The destination isn't a directory")
                return False

            printinf(f"Now downloading: {_from} to {_to}...\n")
            run(["oc", "rsync", f"{pod_name}:{_from}", _to])
        except Exception as e:
            printerr(e)
            return False
        finally:
            printsuc("Process completed\n\n")
            return True

    def do_pod2pod_transfer(self, _from: str, _to: str):
        printinf(f"Starting transfer from {_from} to {_to}")

        pod1 = search(POD_REGEX, _from).group(0).replace(":", "")
        pod2 = search(POD_REGEX, _to).group(0).replace(":", "")

        path1 = sub(POD_REGEX, "", _from)

        # Extract filename
        file1 = path1.split("/")[-1]
        path2 = sub(POD_REGEX, "", _to)

        printinf(f"Downloading {_from} locally...\n")
        """ Example usage:

        upload-pod2pod --from pod-name-1:/path/to/file.php --to pod-name-2:/path/to/destination/
        """
        self.do_download(path1, ".", pod1)
        printinf(f"Uploading {_from} to {_to}...\n")
        self.do_upload(file1, path2, pod2)

        # Deleting the downloaded file
        try:
            printinf("Deleting locally downloaded files...")
            unlink(file1)
        except FileNotFoundError:
            printerr(f"File not found: {file1}.")
            print("Was it downloaded beforehand?")
            return False
        finally:
            printsuc("Process completed\n\n")
            return True

    
    # Arguments validation for download and upload
    def verify_xload_args(
        self, 
        args: list, 
        argslen: int, 
        xload_type: int
    ) -> bool:
        valid = False
        pods = self.oc.get_pods_list()

        # upload = 1
        # download = 2
        if xload_type == 1 or xload_type == 2:
            """Expecting paths only

            Uses the last accessed pod

            see: config.json
            """
            if argslen == 2:
                for a in args:
                    file = search(FILE_REGEX, a)

                    if a in pods:
                        valid = False
                    elif not file.group(0):
                        valid = False
                valid = True

            # Expecting the pod name as first parameter
            elif argslen == 3:
                if args[0] in pods:
                    """Expected syntax: /path/to/file for both parameters

                    Examples:
                        /upload/path/to/file.pdf
                        /upload/path/to/file.tar.gz.zip
                    """
                    file1 = search(FILE_REGEX, args[1])
                    file2 = search(FILE_REGEX, args[2])
                    if file1.group(0) and file2.group(0):
                        valid = True
        # upload-pod2pod
        elif xload_type == 3:
            if argslen == 2:
                """Expected syntax: pod_name:/path/to/file for both parameters

                Examples:
                        pod-name-randnum1234155:/upload/path/to/file.pdf
                        pod-name-randnum1234155:/upload/path/to/file.tar.gz.zip
                """
                pod1 = search(POD_AND_FILE_REGEX, args[0])
                pod2 = search(POD_AND_FILE_REGEX, args[1])

                if pod1.group(0) in pods and pod2.group(0) in pods:
                    valid = True

        return valid
