import subprocess
import os
import shutil

import gitVersion
import build_settings
import env_var_utils
import read_td_log

artifact_dir_name = "artifacts"
targets_dir_name = "targets"
dist_info_name = "dist_info.json"

dist_info: dict = {}
project_file = build_settings.project_file


def main():
    print('> verifying output directories are created...')
    # Verify dist directory exists
    dist_dir = build_settings.dest_dir+"/"
    if not os.path.isdir(dist_dir):
        print('> creating release...')
        os.mkdir(dist_dir)

    latest_dir = build_settings.latest_dir
    if not os.path.isdir(latest_dir):
        print('> creating release/latest...')
        os.mkdir(latest_dir)

    print("> Starting deploy process...")

    print("-> Finding Version Info...")
    dist_info = gitVersion.GetVersioningInfo()

    print(f"--> Creating build {dist_info.get('major_minor')}")

    # set up env vars
    env_var_utils.set_env_vars(
        build_settings=build_settings, dist_info=dist_info)

    # run td project
    print("--> Starting TouchDesigner")
    td_version = f"C:/Program Files/Derivative/TouchDesigner.{build_settings.td_version}/bin/TouchDesigner.exe"
    subprocess.call([td_version, project_file])

    read_td_log.write_log_to_cloud(build_settings.log_file)

    print("--> Zipping package")
    shutil.make_archive(
        f"{build_settings.dest_dir}/package", 'zip', build_settings.latest_dir)

    # cleanup environment variable keys
    env_var_utils.clear_env_vars(build_settings=build_settings)


if __name__ == "__main__":
    main()
