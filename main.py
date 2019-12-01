from main_download import download_info_and_messages_to_files
import matplotlib
import json
import pandas as pd

# download_info_and_messages_to_files()
m_bodies = []
with open('506496104__messages.txt') as json_file:
    messages = json.load(json_file)
    for message in messages:
        print(message["commenter"]["display_name"] + "\n\t " + message["message"]["body"] + "\n")
        m_bodies.append(message["message"]["body"])

d = pd.DataFrame(messages)
d.plot(x='created_at')
# ["message"]:\
#     ["body"]
# "message": {"body": "miki sie juz nie cieszy 4Head", "emoticons": [{"_id": "354", "begin": 24, "end": 28}], "fragments": [{"text": "miki sie juz nie cieszy "}, {"text": "4Head", "emoticon": {"emoticon_id": "354", "emoticon_set_id": ""}}], "is_action": false, "user_notice_params": {}}
# https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
# print(d.describe())



