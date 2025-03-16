import subprocess


class distInfo:

    def __init__(self):
        self.commit: str
        self.semver: str
        self.major: str
        self.minor: str
        self.patch: str
        self.branch: str

        self.GetVersioningInfo()

    def GetVersioningInfo(self) -> None:
        # grab git information...
        git_branch_process = subprocess.run(
            "git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True)
        branch = str(git_branch_process.stdout, 'utf-8').strip()
        # replace any / characters from branch
        branch = branch.replace("/", "-")
        git_tag_process = subprocess.run(
            "git describe --tags", shell=True, capture_output=True)
        last_full_tag = str(git_tag_process.stdout, 'utf-8').strip()

        tag_parts = last_full_tag.split('-')
        major_minor = tag_parts[0]
        major = major_minor.split('.')[0][1:]
        minor = major_minor.split('.')[1]

        num_commits = "0"

        current_commit_hash = None

        if len(major_minor.split('.')) > 2:
            num_commits = major_minor.split('.')[2]

        semver = f"{major_minor}.{num_commits}"

        if branch != "main":
            if current_commit_hash is not None:
                semver = f"{semver}+{branch}-{current_commit_hash}"

            else:
                semver = f"{semver}+{branch}"

        self.commit = current_commit_hash
        self.semver = semver
        self.major = major
        self.minor = minor
        self.patch = num_commits
        self.branch = branch

    @property
    def asDict(self) -> dict:
        info_dict = {
            "commit": self.commit,
            "semver": self.semver,
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "branch": self.branch
        }

        return info_dict
