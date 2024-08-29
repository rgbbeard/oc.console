#!/usr/bin/python

from printc import PrintC
from subprocess import Popen, PIPE, run
from os.path import dirname, isfile, islink
from os import symlink, unlink

BASE = dirname(__file__)


class Console:
    __help_for: dict = {
        "help": """Interactive console interface for easier use of the OpenShift Client.
            Commands:
                help: Display this help message
                set-credentials: Save your login credentials (required before logging in)
                login: Log in using your saved credentials (required before executing other commands)
                upload: Upload a file to a specified POD
                download: Download a file from a specified POD
                find: Locate a POD
                use-env: Switch between work environments
                enter: Access a specified POD

            For more details use: help {COMMAND}
        """,
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
        "find": "Locate a POD.",
        "ls": "Alias of find",
        "logs": """Shows the POD logs in real time.
            Usage:
                logs {POD} --since {TIME}
        """,
        "enter": """Access a POD.
            You can specify the POD you want to enter, or if no name is provided, the last accessed POD will be used.
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
        "upload": """Upload a file to a specified POD.
            Usage:
                --pod {POD} or default (uses the last accessed POD)
                --from {path/to/file}, the path to the file you want to upload
                --to {path/to/destination}, the destination path in the POD

            Example:
                upload --pod default --from /path/to/somefile.pdf --to /path/to/destination
        """,
        "download": """Download a file from a specified POD.
            Usage:
                --pod {POD} or default (uses the last accessed POD)
                --from {path/to/file}, the path to the file in the POD
                --to {path/to/destination}, the local destination path for the downloaded file

            Example:
                download --pod default --from /path/to/somefile.pdf --to ~/Downloads
        """,
        "upload-pod2pod": """***Coming soon***
            Move a file from a POD to another
        """
    }

    def __init__(self):
        pass

    def get_commands(self):
        return self.__help_for.keys()

    def save_history(self, cmd, args, argsvalid):
        with open(f"{BASE}/.sesshstr", "a") as history:
            row = "\n"

            if not argsvalid:
                row += cmd
            else:
                row += " ".join(args)

            history.write(row)

    def get_help_for(self, cmd: str = ""):
        if not (not cmd) and self.__help_for.get(cmd):
            PrintC.printc_bold(f"Manual for {cmd}:", "YELLOW")
            print(self.__help_for.get(cmd))

    def get_pods_list(self, pod_name: str = ""):
        process = Popen([f"{BASE}/commands/oc.list.pods.sh", pod_name], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        for line in lines:
            print(line)

        if len(lines) == 2:
            PrintC.printc_bold("No POD found.", "RED")

    def set_credentials_path(self, credentials_path: str = ""):
        PrintC.printc_bold("Now checking the path you entered...", "YELLOW")

        if isfile(credentials_path):
            PrintC.printc_bold("The file you provided is valid!", "GREEN")
            PrintC.printc("Saving credentials...", "RED")

            self.__create_link(credentials_path)

            PrintC.printc_bold("Done", "GREEN")

            self.do_login()
        else:            
            PrintC.printc_bold("The provided file is not valid", "RED")

    def __create_link(self, credentials_path: str = ""):
        try:
            symlink(credentials_path, f"{BASE}/.credentials")
        except FileExistsError:
            PrintC.printc_bold("Configuration file already exists", "YELLOW")
            unlink(f"{BASE}/.credentials")
            self.__create_link(credentials_path)

    def set_env(self, environment: str = "dev"):
        run([f"{BASE}/commands/oc.switch.sh", f"{environment}"])

    def get_env(self):
        run([f"{BASE}/commands/oc.env.sh"])

    def spawn_bash(self, pod_name: str = ""):
        run(["/bin/bash", "-c", f"{BASE}/commands/oc.enter.sh", f"{pod_name}"])

    def set_host(self, host_name: str = ""):
        if not (not host_name):
            with open(f"{BASE}/.ochost", "w") as file:
                file.write(host_name)
        else:
            print("The given host name is not valid")

    def get_host(self):
        if isfile(f"{BASE}/.ochost"):
            with open(f"{BASE}/.ochost", "r") as file:
                print(f"Currently using host: {file.readline()}")
        else:
            print("Missing host file. Use 'set-host {HOST}' first")

    def do_login(self):
        try:
            if isfile(f"{BASE}/.ochost"):
                with open(f"{BASE}/.credentials", "r") as credentials:
                    username, password = credentials.readlines()

                process = Popen([f"{BASE}/commands/oc.login.sh", username, password], stdin=PIPE, stderr=PIPE, stdout=PIPE)
                output, error = process.communicate()

                lines = output.decode().splitlines()

                for line in lines:
                    print(line)
            else:
                print("Missing host file. Use 'set-host {HOST}' first")
        except Exception as e:
            print("An error occurred while logging in")
            print(e)

    # TODO: complete these features
    def do_upload(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)

    def do_download(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)

    def verify_xload_args(self, args: list):
        print(args)
