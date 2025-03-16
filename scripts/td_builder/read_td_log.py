import os


def write_log_to_cloud(log_path: str) -> None:
    try:
        with open(log_path, 'r') as target_file:
            for line in target_file:
                # Print each line
                print(f"--> {line.strip()}")

        # deletes file after reading it
        print(f"--> Cleaning up log")
        os.remove(log_path)
    except Exception as e:
        print("NO TD Log file present")
