import subprocess
import os
import shutil


import td_builder.build_settings
import td_builder.env_var_utils
import td_builder.gitVersion
import td_builder.read_td_log

artifact_dir_name = "artifacts"
targets_dir_name = "targets"
dist_info_name = "dist_info.json"
build_settings_file = "buildSettings.json"

dist_info: dict = {}


def main():
    print('> creating release...')

    build_settings = td_builder.build_settings.settings()
    build_settings.load_from_json(build_settings_file)

    # Verify dist directory exists
    dist_dir = f"{build_settings.dest_dir}/"
    print('> verifying output directories are created...')
    if not os.path.isdir(dist_dir):
        print('-> creating directories...')
        os.makedirs(dist_dir, exist_ok=True)

    print("> Starting deploy process...")

    print("-> Finding Version Info...")
    dist_info = td_builder.gitVersion.distInfo()

    print(
        f"--> Creating build {dist_info.major}.{dist_info.minor}.{dist_info.patch}")

    # set up env vars
    td_builder.env_var_utils.set_env_vars(
        build_settings=build_settings.env_vars, dist_info=dist_info.asDict)

    # run td project
    print("--> Starting TouchDesigner")
    td_version = f"C:/Program Files/Derivative/TouchDesigner.{build_settings.td_version}/bin/TouchDesigner.exe"
    subprocess.call([td_version, build_settings.project_file])

    td_builder.read_td_log.write_log_to_cloud(
        build_settings.log_file)

    print("--> Zipping package")
    shutil.make_archive(
        build_settings.package_dir, 'zip', root_dir=build_settings.package_dir)

    # cleanup environment variable keys
    td_builder.env_var_utils.clear_env_vars(
        build_settings=build_settings.env_vars)


if __name__ == "__main__":
    main()
