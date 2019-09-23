import os
import re
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, NewType
from configure import load_config, is_active_file, Config
from pprint import pprint

Datetime = NewType("Datetime", datetime)
Diffs = NewType("Diffs", Dict[str, List[str]])
Stamps = NewType("Stamps", Dict[str, List[str]])


def git_diff() -> Diffs:
    config: Config = load_config()
    root_path = config["root_path"]
    cmd: str = "git diff --histogram"
    cwd = os.getcwd()
    os.chdir(root_path)
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    os.chdir(cwd)
    lines: List[str] = output.split("\n")
    separate_pattern: str = "diff --git "
    group: Diffs = {}
    file_name = ""

    for line in lines:
        if re.match(separate_pattern, line):
            file_name: str = re.sub("a/", "", re.sub(separate_pattern, "", line).split(" ")[0])
            group[file_name] = []

        if file_name:
            group[file_name].append(line)

    return group


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


def untraced_files() -> List[str]:
    cmd: str = "git status"
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    lines: List[str] = output.split("\n")
    files: List[str] = []
    pattern: str = "Untracked files:"
    trace_start: bool  = False
    for line in lines:
        if re.match(pattern, line):
            trace_start = True

        if trace_start and re.match("\t", line):
            file_name = line.strip()
            files.append(file_name)

    return files


def fullpath(files: List[str]) -> List[str]:
    config: Config = load_config()
    root_path: str = config["root_path"]
    return ["{}/{}".format(root_path, file_name) for file_name in files]


def make_time_stamp() -> str:
    now: Datetime = datetime.now()
    time: str = str(now.replace(microsecond=0))
    tzname: str = str(now.astimezone().tzname())
    return time + " " + tzname


def make_diff_stamp(file_name: str, diffs: Diffs, separator: str = "") -> str:
    stamp_text: str = ""

    if file_name in diffs:
        stamp_text = "\n".join(diffs[file_name])
        if separator:
            stamp_text = "{}\n{}".format(separator, stamp_text)

    return stamp_text


# Reserved
def make_sign_stamp():
    pass


def combine_stamp(enable_time_stamp: bool = True, separator: str = "=" * 8) -> Stamps:
    stamps = {}

    for file_name in changed_files():
        time_stamp = ""
        diff_stamp = ""
        if enable_time_stamp:
            time_stamp: str = make_time_stamp() + "\n"

        diffs: Diffs = git_diff()
        if is_active_file(file_name):
            diff_stamp: str = make_diff_stamp(file_name, diffs, separator=separator) + "\n"

        if diff_stamp:
            stamp: str = "{0}{1}".format(time_stamp, diff_stamp)
            stamps[file_name] = stamp

    return stamps


if __name__ == "__main__":
    config = load_config()
    root_path = config["root_path"]
    uuid = config["uuid"]
    path = "{}/docs/{}/dummy1.txt".format(root_path, uuid)
    # pprint(git_diff())
    # print(make_diff_stamp(path, git_diff()))
    print(untraced_files())
    for key, text in combine_stamp().items():
        print(key, text)
