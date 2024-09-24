
import os
import time
import subprocess
import requests

# Set the path to the blockchain node executable
NODE_EXECUTABLE = 'docker run --env-file validator.env --platform linux/amd64 -p 17690:17690 elixirprotocol/validator:v3'

# Set the time interval for checking the terminal output (in seconds)
INTERVAL = 65

# Telegram Bot API token and chat ID
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'

def send_telegram_alert(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'reply_markup': {
            'inline_keyboard': [
                [
                    {'text': 'Restart Validator', 'callback_data': 'restart_validator'},
                    {'text': 'Update Validator', 'callback_data': 'update_validator'}
                ]
            ]
        }
    }
    requests.post(url, json=data)

def restart_validator():
    try:
        subprocess.check_output('docker ps --filter "name=validator" --format "{{.Names}}"', shell=True)
        subprocess.run('docker stop validator && docker rm validator', shell=True)
        subprocess.run(NODE_EXECUTABLE, shell=True)
    except subprocess.CalledProcessError:
        print("Validator is not running.")

def update_validator():
    try:
        subprocess.check_output('docker ps --filter "name=validator" --format "{{.Names}}"', shell=True)
        subprocess.run('docker pull elixirprotocol/validator:v3 --platform linux/amd64', shell=True)
        subprocess.run('docker stop validator && docker rm validator', shell=True)
        subprocess.run(NODE_EXECUTABLE, shell=True)
    except subprocess.CalledProcessError:
        print("Validator is not running.")

def monitor_terminal_output():
    # Run the blockchain node executable and capture its output
    process = subprocess.Popen(NODE_EXECUTABLE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while True:
        # Read the output of the process
        output = process.stdout.readline().decode('utf-8')

        # Check if the output contains specific keywords or patterns
        if 'validator online' in output.lower() or '**** VALIDATOR ONLINE ****' in output:
            print("Node is online and validator is online.")
        else:
            print("Node is not online or validator is not online.")
            # Send an alert to Telegram
            send_telegram_alert("Node is not online or validator is not online. Please choose an action:")

        # Check for a new version of the validator image
        try:
            current_version = subprocess.check_output('docker images elixirprotocol/validator:v3 --format "{{.Tag}}"', shell=True).decode('utf-8').strip()
            new_version = subprocess.check_output('docker pull elixirprotocol/validator:v3 --platform linux/amd64 && docker images elixirprotocol/validator:v3 --format "{{.Tag}}"', shell=True).decode('utf-8').strip()
            if current_version != new_version:
                print(f"New version available: {new_version}")
                # Perform any necessary actions, such as updating the validator image
                send_telegram_alert(f"New version available: {new_version}. Please choose an action:")
        except subprocess.CalledProcessError:
            print("Failed to check for new version.")

        # Wait for the specified interval before checking again
        time.sleep(INTERVAL)

if __name__ == '__main__':
   
