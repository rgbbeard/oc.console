#!/usr/bin/python

from subprocess import Popen, PIPE, run
from re import search, sub
from os.path import dirname, isfile

BASE = dirname(__file__)
PARENT = f"{BASE}/.."


class Commands:
    envs = None

    def __init__(self):
        envs = self.get_envs()

    def get_pods_list(self):
        process = Popen(["oc", "get", "pod"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()
        return lines if len(lines) > 0 else []

    def get_envs(self):
        process = Popen(["oc", "projects"], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        output, error = process.communicate()

        lines = output.decode().splitlines()
        return lines if len(lines) > 0 else []

    def set_env(self, e: str):
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
            env = "DEVELOPMENT"
        elif "prod" in e:
            env = "PRODUCTION"

        with open(f"{PARENT}/.currenv", "w") as file:
            file.write(env)

        print(f"Currently using environment: {e}({env})")

    def spawn_bash(self, pod_name: str):
        self.get_env()

        if not pod_name:
            print("No pod specified, looking for the last accessed pod..")

            with open(f"{PARENT}/.currpod", "r") as file:
                pod_name = file.readline().strip()

        if not pod_name:
            print("No pod found")
            pass

        run(["oc", "rsh", f"{pod_name}", "bash"])

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
