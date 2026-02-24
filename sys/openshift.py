#!/usr/bin/python

from subprocess import Popen, PIPE, run, CalledProcessError
from typing import Union
from re import sub, search
from os.path import dirname, isfile
from oc_deps_manager import OCDepsManager
from utilities import (
    printerr, 
    printinf, 
    printsuc,
    printalr,
    is_empty
)

BASE = dirname(__file__)
PARENT = f"{BASE}/.."
POD_REGEX = r"([\w\/-]+)\s+"

# Load the Formatter class
fmttr = OCDepsManager.module_from_path(f"{PARENT}/formatter.py")
Formatter = fmttr.Formatter

class OpenShift:
    envs = None

    # -------------------------
    # VALIDATORS
    # -------------------------
    @staticmethod
    def session_is_valid() -> bool:
        process = Popen(
            ["oc", "whoami"], 
            stdin=PIPE, 
            stderr=PIPE, 
            stdout=PIPE
        )
        output, error = process.communicate()

        message = output.decode().splitlines()
        return not (not message) and "Error" not in message[0]

    def is_pod(self, pod_name: str = "") -> bool:
        pods = self.get_pods_list()

        for pod in pods:
            if pod_name == pod:
                return True

        return False

    # -------------------------
    # GETTERS
    # -------------------------
    def get_logs(
        self,
        pod_name: str = None,
        since: Union[str, None] = "30m",
        save_logs: bool = False,
        filename: Union[str, None] = None,
        search: Union[str, list, None] = None,
        debug: bool = False
    ):
        if not since:
            since = "30m"

        # Ensures pod_name is valid
        if pod_name and self.is_pod(pod_name):
            cmd = ["stern", pod_name, "--since", since]

            if debug:
                print(
                    f"Query: {' '.join(cmd)}\n",
                    "Params:\n",
                    f"pod_name: {pod_name}\n",
                    f"since: {since}\n",
                    f"save_logs: {save_logs}\n",
                    f"filename: {filename}\n"
                    f"search: {[type(search), search]}\n"
                )
                pass

            try:
                process = Popen(
                    cmd, 
                    stdout=PIPE, 
                    stderr=PIPE, 
                    shell=False
                )
                output = process.stdout

                # Filter with one or more keywords
                if search is not None and (isinstance(search, str) or len(search) > 0):
                    for line in output:
                        line = line.decode('utf-8').strip()

                        if isinstance(search, str):
                            if search in line:
                                print(Formatter.format_log(line))

                        # Filter by multiple keywords
                        elif isinstance(search, list):
                            if all(keyword in line for keyword in search):
                                print(Formatter.format_log(line))
                else:
                    # Output the logs directly if no search filter
                    for line in process.stdout:
                        l = line.decode('utf-8').strip()
                        print(Formatter.format_log(l))
            except CalledProcessError as e:
                printerr(f"Error occurred: {e}")
            except KeyboardInterrupt:
                print("\n\nOkay, bye!")
        else:
            print("Invalid pod name")

    def get_pods_list(self):
        pods = []

        process = Popen(
            ["oc", "get", "pod"], 
            stdin=PIPE, 
            stderr=PIPE, 
            stdout=PIPE
        )
        output, error = process.communicate()

        lines = output.decode().splitlines()
        if len(lines) > 0:
            # Remove header
            lines.pop(0)

            for line in lines:
                if search(POD_REGEX, line) is not None:
                    pod = search(POD_REGEX, line).group(0)
                    pods.append(pod.strip())

        return pods if len(pods) > 0 else []

    def get_envs(self):
        process = Popen(
            ["oc", "projects"], 
            stdin=PIPE, 
            stderr=PIPE, 
            stdout=PIPE
        )
        output, error = process.communicate()

        lines = output.decode().splitlines()

        if len(lines) > 0:
            tmp = []

            for line in lines:
                if not line:
                    continue
                else:
                    tmp.append(line)

            # Remove first and last element
            tmp.pop(0)
            tmp.pop()

            for l in range(0, len(tmp)):
                line = tmp[l]

                line = line.replace("*", "")
                tmp[l] = sub(r"^\s+|\s+$", "", line)

            self.envs = tmp
            return tmp
        else:
            return []
    
    def get_status(self):
        try:
            process = Popen(
                ["oc", "status"], 
                stdin=PIPE, 
                stderr=PIPE, 
                stdout=PIPE,
                shell=True
            )
            output, error = process.communicate()

            for line in output.decode().splitlines():
                print(line)
        except Exception as e:
            printerr("No host found, use 'set host {HOST}' first")
            print(e)

    # -------------------------
    # SETTERS
    # -------------------------
    def set_env(self, e: str):
        if is_empty(e):
            printerr("No environment passed")
            return

        run(["oc", "project", e])

    # -------------------------
    # ACTIONS
    # -------------------------
    def start_session(self, pod_name: str):
        if is_empty(pod_name):
            printerr("No pod passed")
            return

        run(["oc", "rsh", f"{pod_name}", "sh"])

    def do_login(self, host: str, username: str, password: str):
        try:
            if not is_empty(host):
                cmd = f'{{ echo "{username}"; echo "{password}"; }} | oc login {host} --insecure-skip-tls-verify'

                process = Popen(
                    cmd, 
                    stdin=PIPE, 
                    stderr=PIPE, 
                    stdout=PIPE, 
                    shell=True
                )
                output, error = process.communicate()

                lines = output.decode().splitlines()

                for line in lines:
                    # some replacements
                    if line.startswith("You have access to the following"):
                        print("You have access to the following namespaces and can switch between them with 'set namespace|env <namespace>':")
                        continue
                    elif "Username:" in line or "Password:" in line:
                        continue

                    print(line)

                if process.returncode == 0:
                    self.envs = self.get_envs()
                else:
                    printerr(f"Unable to login, process exited with error code: {process.returncode}")
            else:
                printerr("No host found, use 'set host {HOST}' first")
        except Exception as e:
            printerr("An error occurred while logging in")
            print(e)

    def do_logout(self):
        try:
            printinf("Logging out...")
            run(["oc", "logout"])
            exit()
        except Exception as e:
            printerr("An error occurred while logging out")
            print(e)
