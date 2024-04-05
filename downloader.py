import subprocess
import os  # Ensure os is imported


def call_script_with_name(file_path):
    with open(file_path, "r") as file:
        for line in file:
            name = line.strip()  # Remove any leading/trailing whitespace
            if name:  # If the line is not empty
                # Construct the directory name by replacing spaces with underscores
                name_dir_string = name.replace(" ", "_")
                # Construct the full path to the directory
                dir_path = f"./images/{name_dir_string}"

                # Check if the directory already exists
                if os.path.isdir(dir_path):
                    # Check if the directory is empty
                    if not os.listdir(dir_path):
                        print(f"Directory for {name} is empty, deleting and proceeding...")
                        os.rmdir(dir_path)  # Remove the directory since it's empty
                    else:
                        print(f"Directory for {name} already exists and is not empty, skipping...")
                        continue  # Skip the rest of the loop and move to the next name

                # Construct the command to call as a single string
                command = f"python3 ./google-image-scraper/src/main.py '\"{name}\" ceramics OR pot OR pottery OR pots -portrait -book -person -dealer' --count 30 -d {dir_path}"

                print("command is", command)

                try:
                    # Execute the command, using shell=True and adding a timeout of 60 seconds (1 minute)
                    subprocess.run(command, shell=True, timeout=60)
                except subprocess.TimeoutExpired:
                    print(f"Command '{command}' timed out after 60 seconds")


if __name__ == "__main__":
    names_file = "names.txt"
    call_script_with_name(names_file)
