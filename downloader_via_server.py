import subprocess
import os
import requests  # Import the requests library for making HTTP requests

SERVER_IP = "1.1.1.1"  # Placeholder IP, replace with the actual server IP when available


def fetch_name():
    """Fetch a name from the server."""
    response = requests.get(f"http://{SERVER_IP}/get_name")
    if response.status_code == 200:
        return response.json().get("name")
    else:
        print("Failed to fetch name or no names left.")
        return None


def notify_name_finished(name):
    """Notify the server that processing for a name has finished."""
    response = requests.post(f"http://{SERVER_IP}/name_finished", json={"name": name})
    if response.status_code == 200:
        print(f"Successfully notified server that {name} is finished.")
    else:
        print(f"Failed to notify server that {name} is finished. Status Code: {response.status_code}")


def call_script_with_name():
    name = fetch_name()  # Fetch a name from the server
    if name:
        name_dir_string = name.replace(" ", "_")
        dir_path = f"./images/{name_dir_string}"

        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            print(f"Directory for {name} is empty, deleting and proceeding...")
            os.rmdir(dir_path)
        elif os.path.isdir(dir_path):
            print(f"Directory for {name} already exists and is not empty, skipping...")
            notify_name_finished(name)
            return

        command = f"python3 ./google-image-scraper/src/main.py '\"{name}\" ceramics OR pot OR pottery OR pots -portrait -book -person -dealer' --count 30 -d {dir_path}"
        print("command is", command)

        try:
            subprocess.run(command, shell=True, timeout=60)
            notify_name_finished(name)  # Notify the server that processing for the name has finished
        except subprocess.TimeoutExpired:
            print(f"Command '{command}' timed out after 60 seconds")


if __name__ == "__main__":
    while True:  # Keep fetching and processing names until there are no names left
        call_script_with_name()
