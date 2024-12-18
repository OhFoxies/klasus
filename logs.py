import os
from typing import TextIO
from datetime import datetime


class Logs:
    def __init__(self) -> None:
        self.time_format = "%d.%m.%Y %H:%M:%S"
        self.time_format_file = "%d.%m.%Y %H-%M-%S"
        self.logs_file = self.create_logs()

    def create_logs(self) -> TextIO:
        """
        Creates new logs file, and moves old logs to folders.
        :return: Writeable file for logging.
        """
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        if "latest.log" in os.listdir("logs/"):
            time = datetime.now().strftime(self.time_format_file)
            os.mkdir(f"logs/{time}")
            os.rename(f"logs/latest.log", f"logs/{time}/logs {time}.log")
        logs_file = open(f"logs/latest.log", 'w', encoding="UTF-8")
        return logs_file

    def log(self, text: str, is_error: bool = False) -> None:
        """
        Method to save logs with current time.

        :param str text: Text to save in log file
        :param bool is_error: if set to True then creates ERROR instead of log.
        """
        formatted = f"[{'ERROR' if is_error else 'LOG'}] [{datetime.now().strftime(self.time_format)}]: {text}"
        self.logs_file.write(f"{formatted}\n")
        print(formatted)


logs_ = Logs()
