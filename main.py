from main_download import download_info_and_messages_to_files
import json

# download_info_and_messages_to_files()
m_bodies = []
with open('506496104__messages.txt') as json_file:
    messages = json.load(json_file)
    for message in messages:
        print(message["commenter"]["display_name"] + "\n\t " + message["message"]["body"] + "\n")
        m_bodies.append(message["message"]["body"])




