#!/usr/bin/python

from subprocess import Popen, PIPE, run
from re import sub, search
from os.path import dirname, isfile

BASE = dirname(__file__)
PARENT = f"{BASE}/.."
POD_REGEX = r"([\w\/-]+)\s+"

class Commands:
    envs = None

    def __init__(self):
        self.envs = self.get_envs()

    def get_pods_list(self):
        pods = []

        process = Popen(["oc", "get", "pod"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()
        if len(lines) > 0:
            # remove header
            lines.pop(0)

            for line in lines:
                if search(POD_REGEX, line) is not None:
                    pod = search(POD_REGEX, line).group(0)
                    pods.append(pod.strip())

        return pods if len(pods) > 0 else []

    def get_envs(self):
        process = Popen(["oc", "projects"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()

        if len(lines) > 0:
            tmp = []

            for line in lines:
                if not line:
                    continue
                else:
                    tmp.append(line)

            # remove first and last element
            tmp.pop(0)
            tmp.pop()

            for l in range(0, len(tmp)):
                line = tmp[l]

                line = line.replace("*", "")
                tmp[l] = sub(r"^\s+|\s+$", "", line)

            return tmp
        else:
            return []

    def set_env(self, e: str):
        if not (not e):
            e = e.strip()
        else:
            print("Environment not passed")
            return

        if e in self.envs:
            run(["oc", "project", e])

            self.__save_env(e)
        else:
            print("Environment not found")
            print("Use 'envs' to show the available environments")

    def get_env(self):
        with open(f"{PARENT}/.currenv", "r") as file:
            print(f"Currently using environment: {file.readline()}")

    def __save_env(self, e: str):
        if "dev" in e:
            env = f"{e} (DEVELOPMENT)"
        elif "preprod" in e or "test" in e:
            env = f"{e} (TEST)"
        elif "prod" in e:
            env = f"{e} (PRODUCTION)"

        with open(f"{PARENT}/.currenv", "w") as file:
            file.write(env)

        print(f"Currently using environment: {env}")

    def spawn_bash(self, pod_name: str):
        self.get_env()

        with open(f"{PARENT}/.currpod", "w") as file:
            file.write(pod_name)

        if not pod_name:
            print("No pod specified, looking for the last accessed pod..")

            with open(f"{PARENT}/.currpod", "r") as file:
                pod_name = file.readline().strip()

        if not pod_name:
            print("No pod found")
            pass

        run(["oc", "rsh", f"{pod_name}", "sh"])

    def do_login(self):
        try:
            if isfile(f"{PARENT}/.ochost"):
                with open(f"{PARENT}/.ochost", "r") as ochost:
                    host = ochost.readline().strip()

                if not host:
                    print("Host file is empty. Use 'set-host {HOST}' first")

                with open(f"{PARENT}/.credentials", "r") as credentials:
                    username, password = credentials.readlines()

                cmd = f'{{ echo "{username}"; echo "{password}"; }} | oc login {host} --insecure-skip-tls-verify'

                process = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
                output, error = process.communicate()

                lines = output.decode().splitlines()

                for line in lines:
                    print(line)
            else:
                print("Missing host file. Use 'set-host {HOST}' first")
        except Exception as e:
            print("An error occurred while logging in")
            print(e)

    def do_logout(self):
        try:
            print("Logging out...")
            run(["oc", "logout"])
            exit()
        except Exception as e:
            print("An error occurred while logging out")
            print(e)
