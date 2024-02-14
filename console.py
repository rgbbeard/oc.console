#!/usr/bin/python

from printc import PrintC
from subprocess import Popen, PIPE
from app_utils import is_file


class Console:
    # TODO: make manuals more descriptive
    __help_for: dict = {
        "help": "Interactive console interface to make it easier to use Openshift Client",
        "upload": "Upload a file to a specified POD",
        "find": "Find a POD",
        "enter": "Enter into a specified POD",
        "switch": "Switch working environment (development or production)",
        "login": "Log in to Openshift Client with your credentials",
        "set-credentials": "Set your login credentials"
    }

    def __init__(self):
        pass

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
        # made extra verbose name to prevent this variable from being overwritten
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

    # TODO: spawn bash
    def spawn_bash(self, pod_name: str = ""):
        pass

    def do_login(self):
        process = Popen("./commands/oc.login.sh", stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        for line in lines:
            print(line)
