from datetime import datetime
import subprocess
from pathlib import Path


OP_DEFAULT_COLOR: tuple = (0.67, 0.67, 0.67)


def update_custom_str_par(targetOp: OP, par: callable, value: str, par_label: str = "Temp", order=0, newSection=False):

    # if the target op is valid, just update the par
    if targetOp.par[par] != None:
        targetOp.par[par] = value

    #  if there's no par, create the par and set the value
    else:
        about_page: Page = targetOp.appendCustomPage("About")
        new_par: Par = about_page.appendStr(par, label=par_label, order=order,)
        new_par.startSection = newSection
        targetOp.par[par] = value

    # ensure par is set to read only
    targetOp.par[par].readOnly = True


# NOTE gemini generated function
def get_pretty_timestamp():
    """Returns the current time formatted as YYYY-MM-DD | HH:MM:SS"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d | %H:%M:%S")


def msg_formatter(msg: str, indent: int = 0, displayInTextport: bool = True) -> str:
    '''Prints and returns a string with a time stamp and indent - suitable for logs
    and the textport
    '''
    indentText = f"{'--' * indent}> "
    formattedMsg = f"{get_pretty_timestamp()} [~] {indentText if indent>0 else ''}{msg}"
    if displayInTextport:
        print(formattedMsg)
    return formattedMsg


def log_event_to_file(msg: str, tox_name: str, log_file: Path) -> None:
    output_msg = f'TD {tox_name} {msg}'
    try:
        with open(log_file, "a") as file:
            file.write(f"{output_msg}\n")
    except Exception as e:
        pass


def get_semver() -> str:
    '''Returns a semver based on tags, and number of commits to a repo
    '''
    semver = "v0.1"

    if has_tags():
        return get_version_info()
    else:
        return semver


def has_tags() -> bool:
    '''Checks repo for existing tags - this will tell us if we can increment our semver
    '''
    tag_cmd = [
        "git",
        "tag"
    ]
    results = subprocess.check_output(tag_cmd, text=True).strip()
    if len(results) > 0:
        return True
    else:
        return False


def get_version_info() -> str:
    """Pulls version info from the latest version tag off of the repo itself"""

    # 1. Get the latest tag name (matching your vX.Y pattern)
    # Using the same logic as your GitHub Action
    tag_cmd = [
        "git",
        "describe",
        "--tags",
        "--abbrev=0",
        "--match",
        "v[0-9]*.[0-9]*",
    ]
    latest_tag = result_from_subprocess(tag_cmd)

    major_minor_patch = latest_tag.split(".")
    major_minor = ".".join([major_minor_patch[0], major_minor_patch[1]])

    # 2. Get the count of commits from that tag to the current HEAD
    count_cmd = ["git", "rev-list", "--count", f"{major_minor}..HEAD"]
    num_commits = result_from_subprocess(count_cmd)

    # get the branch
    branch_cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    branch = result_from_subprocess(branch_cmd)

    commit_cmd = ["git", "rev-parse", "--short", "HEAD"]
    commit = result_from_subprocess(commit_cmd)

    semver = f"{major_minor}.{num_commits}"
    return semver


def result_from_subprocess(cmdList: list[str]) -> str:
    """
    """
    result = subprocess.run(
        cmdList, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True)
    result_str = result.stdout.strip()
    return result_str
