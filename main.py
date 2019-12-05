import json
from main_download import download_info_and_messages_to_files
import matplotlib

# download_info_and_messages_to_files()

m_bodies = []
m_created = []
with open('506496104__messages.txt') as json_file:
    messages = json.load(json_file)
    for message in messages:
        # print(message["commenter"]["display_name"] + "\n\t " + message["message"]["body"] + "\n")
        m_bodies.append(message["message"]["body"])
        m_created.append(message["created_at"])



