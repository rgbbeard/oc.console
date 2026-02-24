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
            Displays general help for the console or the manual for a specific command. 
            Aliases: **manuel**, **manuel!**

            **Usage:**
                * `help`
                * `help <command_name>`

            **Arguments:**
                * **<command_name>**: Optional. The command to explain.
        """,
        "clear": """
            Clears the terminal screen.
            Aliases: **cls**

            **Usage:**
                * `clear`
        """,
        "purge": """
            Deletes stored data based on the argument provided.

            **Usage:**
                * `purge history`

            **Arguments:**
                * **history**: Clears the command history file.
        """,
        "reload-config": """
            Reloads the configuration file and refreshes global settings.

            **Usage:**
                * `reload-config`
        """,
        "show": """
            Displays connection details or resource explanations.

            **Usage:**
                * `show config`
                * `show config <key>`
                * `show pod` (In Development)

            **Arguments:**
                * **config**: Shows the current configuration.
                * **pod**: Explains pod details (currently a placeholder).
        """,
        "set": """
            Updates configuration parameters or the working environment.

            **Usage:**
                * `set host <value>`
                * `set credentials <user> <password>`
                * **Aliases for credentials**: `username`, `password`
                * `set namespace <value>` (Alias: **env**)

            **Arguments:**
                * **host**: The target server URL.
                * **namespace**: The target environment/namespace.
        """,
        "login": """
            Authenticates the user using current host and credentials and fetches environments.

            **Usage:**
                * `login`
        """,
        "logout": """
            Invalidates the current session and logs the user out.
            Aliases: **exit**

            **Usage:**
                * `logout`
        """,
        "status": """
            Checks the current connection and user authentication status.

            **Usage:**
                * `status`
        """,
        "envs": """
            Lists all available namespaces/environments.
            Aliases: **envs?**, **namespaces**

            **Usage:**
                * `envs`
        """,
        "ls": """
            Lists all available pods in the current namespace.
            Aliases: **pods**

            **Usage:**
                * `ls`
        """,
        "find": """
            Searches for a specific pod by name.

            **Usage:**
                * `find <pod_name>`
        """,
        "enter": """
            Starts an interactive bash session inside the requested pod.

            **Usage:**
                * `enter <pod_name>`
        """,
        "logs": """
            Streams logs from a pod. Uses 'stern' notation and supports JSON formatting.

            **Usage:**
                * `logs <pod_name> [options]`

            **Options:**
                * `--since`, `-t`: Duration (e.g., 1h24m10s).
                * `--search`, `-R`: Filter terms.
                * `--save-logs`, `>`: Save output to a file.
                * `--debug`, `-D`: Enable debug mode.
        """,
        "upload": """
            Uploads a file to a pod.

            **Usage:**
                * `upload <local_path> <remote_path>`
                * `upload <pod_name> <local_path> <remote_path>`
        """,
        "download": """
            Downloads a file from a pod.

            **Usage:**
                * `download <remote_path> <local_path>`
                * `download <pod_name> <remote_path> <local_path>`
        """,
        "upload-pod2pod": """
            Directly transfers a file from one pod to another.

            **Usage:**
                * `upload-pod2pod <source_pod> <destination_pod>`
        """
    }

    def __init__(self):
        self.oc = OpenShift()
        self.jsm = JSONMaid(CFGFILE)
        self.kt = Krypto()

        cfg = self.get_config()
        self.cfg = cfg

        # Capture host
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
                print(247)
                print(e)

        # Capture credentials
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

    # -------------------------
    # ACTIONS
    # -------------------------
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

    def _save_env(self, e: str) -> True:
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

    def _save_pod(self, p: str) -> True:
        cfg = self.get_config()
        cfg["pod"] = p
        self.save_and_reload(cfg)

        return True

    # -------------------------
    # SETTERS
    # -------------------------
    def set_credentials(self, username: str, password: str) -> bool:
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

    def set_username(self, username: str) -> bool:
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

    def set_password(self, password: str) -> bool:
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

    def set_host(self, host: str) -> bool:
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

    def set_namespace(self, e: str) -> bool:
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

    def set_pod(self, p: str) -> Union[bool, str]:
        found = False

        if is_empty(p):
            printerr("No pod name passed")
            return False

        if is_empty(self.oc.get_pods_list()):
            printalr("No pods found, try logging in first")
            return False

        p = p.strip()
        pods = self.oc.get_pods_list()
        matches = []

        for pod in pods:
            # Matched at least one entry
            if p in pod:
                found = True
                matches.append(pod)

        if not found:
            printerr("No pod found")
            print("Use 'pods' to list the available pods")
            return False

        if len(matches) == 1:
            p = matches[0]
        if len(matches) > 1:
            print(f"For name {p} were found {len(matches)} pods:")

            for x in range(len(matches)):
                print(f"{x+1}) {matches[x]}")

            choice = input(f"Please choose a number between 1 and {len(matches)}: ")
            choice = int(choice)

            try:
                p = matches[choice-1]
            except IndexError:
                printerr("There was an errore trying to select the chosen pod, please retry")
                return False

        self._save_pod(p)

        return p

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

                        if bd is not None:
                            print(printstr + str(bd))
                        else:
                            print(printstr + b)
                else:
                    v = self.get_cleanvalue(v)

                    if v is not None:
                        v = config.get(a)

                    print(printstr + str(v))

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

            # Partial name
            if not self.oc.is_pod(pod_name):
                # Try to automatically find one match
                pod_name = self.set_pod(pod_name)

                if is_empty(pod_name):
                    printerr("No pod found")
                    return

            self.oc.start_session(pod_name)
        except Exception as e:
            print(e)
            printerr(f"An unexpected error occurred while accessing pod {pod_name}")

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

    # -------------------------
    # VALIDATORS
    # 
    # Arguments validation for download and upload
    # -------------------------
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
