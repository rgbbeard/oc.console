#!/usr/bin/python

from datetime import datetime
import json
from re import sub


class Formatter:
    indentation_level: int = 3

    @staticmethod
    def normalize_date(date:str):
        dt = None
        try:
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except Exception as e:
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def format_log(log: str) -> str:
        try:
            # can this be useful for something?
            pod_name = log[0:log.index("{")]
            data = log[log.index("{"):]

            # sanitize missing data
            data = sub(r": -", ": null", data)

            data = json.loads(data);
            keys = list(data.keys())

            if keys[0] == "message":
                return Formatter._format_500_log(data)

            l = {}

            time = Formatter.normalize_date(data["time"])

            l["time"] = time
            l["status-code"] = data.get("level", data.get("status", "unknown"))
            l["server-ip"] = data.get("local-ip-address", "unknown")
            l["remote-ip"] = data.get("remoteIP", "unknown")
            l["call"] = data.get("host", "") + data.get("request", "")
            l["caller"] = data.get("referer", "")
            l["path"] = data.get("filename", "")
            l["request-method"] = data.get("method", "")
            l["parameters"] = data.get("query", "").replace("?", "").split("&")
            l["user-agent"] = data.get("userAgent", "")

            return json.dumps(l, indent=Formatter.indentation_level)
        except Exception as e:
            return f"Error: {e}:\n{log}\n{'-'*50}"

    @staticmethod
    def _format_500_log(log: dict) -> str:
        l = {}

        time = Formatter.normalize_date(log["datetime"])

        l["time"] = time
        l["status-code"] = log.get("level", "(assuming it was 500)")
        l["error-message"] = log.get("message", "")
        l["context"] = log.get("context", "")
        l["extras"] = log.get("extra", "")

        return json.dumps(l, indent=Formatter.indentation_level)