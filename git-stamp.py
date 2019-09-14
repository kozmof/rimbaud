import re
import subprocess
from datetime import datetime, timezone
from typing import List, NewType
Datetime = NewType("Datetime", datetime)


def file_diff() -> str:
    cmd: str = "git diff --staged --histogram"
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return output


def changed_files() -> List[str]:
    cmd: str = "git status"
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    lines: List[str] = output.split("\n")
    files: List[str] = []
    pattern: str = "(\tmodified:|\tnew file:)"

    for line in lines:
        if re.match(pattern, line):
            file_name: str = re.sub(pattern, "", line).strip()
            if file_name not in files:
                files.append(file_name)

    return files


def time_stamp() -> str:
    now: Datetime = datetime.now()
    time: str = str(now.replace(microsecond=0))
    tzname: str = str(now.astimezone().tzname())
    return time + " " + tzname + "\n"


def stamp(file_path: str) -> None:
    stamp_text: str = "{}\n{}".format(time_stamp(), file_diff())
    with open(file_path, "a") as f:
      f.write(stamp_text)


if __name__ == "__main__":
    print(changed_files())