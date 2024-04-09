#!/usr/bin/python

class PrintC:
    COLORS = {
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m"
    }
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    @staticmethod
    def printc_bold(string: str = "", cname: str = ""):
        color = PrintC.COLORS.get("CYAN")

        if not (not cname):
            color = PrintC.COLORS.get(cname.upper())

        print(f"{PrintC.BOLD} {color}{string}{PrintC.END}")

    @staticmethod
    def printc_underline(string: str = "", cname: str = ""):
        color = PrintC.COLORS.get("CYAN")

        if not (not cname):
            color = PrintC.COLORS.get(cname.upper())

        print(f"{PrintC.UNDERLINE} {color}{string}{PrintC.END}")

    @staticmethod
    def printc(string: str = "", cname: str = ""):
        color = PrintC.COLORS.get("CYAN")

        if not (not cname):
            color = PrintC.COLORS.get(cname.upper())

        print(f"{color}{string}{PrintC.END}")
