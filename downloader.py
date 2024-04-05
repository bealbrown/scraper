import subprocess


def call_script_with_name(file_path):
    with open(file_path, "r") as file:
        for line in file:
            name = line.strip()  # Remove any leading/trailing whitespace
            if name:  # If the line is not empty
                # Construct the command to call as a single string

                name_dir_string = name.replace(" ", "_")
                command = f"python3 ./google-image-scraper/src/main.py '\"{name}\" ceramics OR pot OR pottery OR pots -portrait -book -person -dealer' --count 30 -d ./images/{name_dir_string}"

                print("command is", command)

                try:
                    # Execute the command, using shell=True and adding a timeout of 60 seconds (1 minute)
                    subprocess.run(command, shell=True, timeout=60)
                except subprocess.TimeoutExpired:
                    print(f"Command '{command}' timed out after 60 seconds")


if __name__ == "__main__":
    names_file = "names.txt"
    call_script_with_name(names_file)
