import json


class settings:
    REQUIRED_KEYS: list = ["BUILD", "TD_VERSION",
                           "PROJECT_FILE", "REPO", "COMP_NAME"]

    def __init__(self):
        self.project_file: str
        self.td_version: str
        self.log_file: str
        self.privacy: str
        self.repo: str
        self._build: str = "TRUE"
        self._project_name: str = "TBD"
        self.release_dir: str = 'release'
        self.package_dir: str = f"{self.release_dir}/package"
        self.log_file: str = f"{self.package_dir}/log.txt"
        self.additional_keys: dict = {}

    @property
    def dest_dir(self) -> str:
        return f"{self.package_dir}/{self.project_name}"

    @property
    def td_package_file(self) -> str:
        return f"{self.dest_dir}/tdPackages.yaml"

    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def build(self) -> str:
        return self._build

    @property
    def env_vars(self) -> dict:
        # build required keys
        env_vars = {
            "SM_BUILD": self.build,
            "SM_PRIVACY": "FALSE",
            "SM_SAVE_PATH": f"../{self.dest_dir}",
            "SM_COMP_NAME": self.project_name,
            "SM_LOG_FILE": f"../{self.log_file}",
            "SM_REPO": self.repo,
            "SM_TD_PACKAGE_FILE": f"../{self.td_package_file}"
        }

        # add additional keys
        if self.additional_keys != None:
            for key, value in self.additional_keys:
                env_vars[key] = value

        return env_vars

    def load_from_json(self, src_file: str) -> dict:
        print('-> loading build settings from file...')
        try:
            with open(src_file, 'r') as file:
                data: dict = json.load(file)

                if set(settings.REQUIRED_KEYS) <= data.keys():
                    print('-> all required keys accounted for')
                    self._build = data.get("BUILD")
                    self.td_version = data.get("TD_VERSION")
                    self.project_file = data.get("PROJECT_FILE")
                    self.repo = data.get("REPO")
                    self._project_name = data.get("COMP_NAME")

                    for key, value in data.items():
                        if key in settings.REQUIRED_KEYS:
                            pass
                        else:
                            self.additional_keys[key] = str(value)

                    return data

                else:
                    print(
                        f"-> buildSettings missing required keys, {settings.REQUIRED_KEYS} must be present")
                    exit

        except Exception as e:
            print(e)
            print("-> unable to locate build settings, please ensure a 'buildSettings.json file is in the root of your project")
            exit

        return
