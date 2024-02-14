#!/usr/bin/python

import os
from datetime import datetime
from time import ctime
import re


def str_split(string: str):
    return [char for char in string]


def is_dir(target: str):
    return os.path.isdir(target)


def is_file(target: str):
    return os.path.isfile(target)


# File/folder size
def fsize(target: str):
    if is_file(target) or is_dir(target):
        return os.stat(target).st_size
    return None


# Date last modified
def fmdate(target: str):
    if is_file(target) or is_dir(target):
        return os.path.getmtime(target)
    return None


# Date creation
def fcdate(target: str):
    if is_file(target) or is_dir(target):
        return ctime(fmdate(target))
    return ""


def fname(target: str):
    if is_file(target):
        name, ext = os.path.splitext(target)
        return name
    return ""


def fext(target: str):
    if is_file(target):
        name, ext = os.path.splitext(target)
        # Remove the leading dot
        return ext[1::]
    return ""


def is_xml(target: str):
    # Validate the file extension
    if is_file(target) and "xml" in fext(target):
        with open(target, "r") as tmp_xml:
            for line in tmp_xml:
                # Verify header
                if re.match(r"(<\?xml version=\".+\" encoding=\".+\"\?>)", line.strip()):
                    return True
    return False


def is_pdf(target: str):
    # Validate the file extension
    if is_file(target) and fext(target) == "pdf":
        tmp_pdf = open(target, "rb")
        pdf = tmp_pdf.read(8).decode("utf-8")
        # Verify header
        if re.match(r"^\%PDF\-\d", pdf.strip()):
            return True
    return False


def frecent(target: str):
    ts = datetime.fromtimestamp(fmdate(target))
    y = int(ts.strftime("%Y"))
    mm = int(ts.strftime("%m"))
    d = int(ts.strftime("%d"))

    h = int(ts.strftime("%H"))
    mn = int(ts.strftime("%I"))
    s = int(ts.strftime("%S"))

    then = datetime(y, mm, d, h, mn, s)
    now = datetime.now()

    duration = now - then
    seconds = duration.total_seconds()
    days = datetime.fromtimestamp(seconds).strftime("%d")

    return int(days) <= 1


def abspath(target: str):
    if is_file(target) or is_dir(target):
        return os.path.abspath(target)
    return ""


def get_path(from_filename: str, path_format: str = "lunix"):
    curdir = ""

    if path_format in ("unix", "linux", "lunix"):
        curdir = os.path.realpath(from_filename).replace("\\", "/")
        curdir = curdir.split("/")
        curdir.pop()
        curdir = "/".join(curdir)

    elif path_format in ("nt", "windows", "win"):
        curdir = curdir.split("\\")
        curdir.pop()
        curdir = "\\".join(curdir)

    return curdir
