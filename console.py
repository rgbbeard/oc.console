#!/usr/bin/python

from printc import PrintC
from subprocess import Popen, PIPE, run
from app_utils import is_file


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
        "find": "Locate a POD.",
        "enter": """Access a POD.
            You can specify the POD you want to enter, or if no name is provided, the last accessed POD will be used.
            Usage:
                enter {POD}
        """,
        "use-env": """Switch between work environments (development or production).
            Usage:
                use-env prod (or dev)
        """,
        "login": """Log in to the OpenShift Client using your credentials. 
            An .ochost file with the host address is required.
        """,
        "set-credentials": """Save your login credentials.
            This command requires the path to the file containing the login credentials.
            The file should contain only the username and password, each on a separate line.

            Usage:
                set-credentials /path/to/file
        """
    }

    def __init__(self):
        pass

    def get_commands(self):
        return self.__help_for.keys()

    def save_history(self, cmd, args, argsvalid):
        with open("./.sesshstr", "a") as history:
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
        process = Popen(["./commands/oc.list.pods.sh", pod_name], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        for line in lines:
            print(line)

        if len(lines) == 2:
            PrintC.printc_bold("No POD found.", "RED")

    def set_credentials_path(self, credentials_path: str = ""):
        # Made extra verbose name to prevent this variable from being overwritten
        env_var_name = "OC_INTERACTIVE_CONSOLE_CREDENTIALS_PATH"
        PrintC.printc_bold("Now checking the path you entered...", "YELLOW")

        if is_file(credentials_path):
            PrintC.printc_bold("Valid!", "GREEN")

            with open(credentials_path, "a+") as f:
                if not (env_var_name in f.read()):
                    PrintC.printc("Credentials not set, writing file...", "RED")

                    f.write(f"export {env_var_name}=\"{credentials_path}\"")

                    PrintC.printc("Variable written, now refreshing the configuration file...", "GREEN")

                    # Trying to refresh the local configuration
                    Popen(["source ~/.bashsrc"], stdin=PIPE, stderr=PIPE, stdout=PIPE)

                    PrintC.printc(f"The path you entered: {credentials_path}", "YELLOW")
                    PrintC.printc_bold("All done! You're good to go.", "GREEN")
                else:
                    PrintC.printc_bold("Credentials' file is already set in ~/.bashrc.", "RED")

    def set_env(self, environment: str = "dev"):
        process = Popen(["./commands/oc.env.sh", f"{environment}"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        for line in lines:
            print(line)

    def spawn_bash(self, pod_name: str = ""):
        run(['/bin/bash', '-c', f'./commands/oc.enter.sh {pod_name}'])

    def do_login(self):
        process = Popen("./commands/oc.login.sh", stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        for line in lines:
            print(line)

    def do_upload(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)

    def do_download(self, _from: str, _to: str, pod_name: str = "default"):
        print(pod_name, _from, _to)
