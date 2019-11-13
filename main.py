import sys
from rechatdl import download_messages_from_twitch, download_vid_info

vid_id = "506496104"
vid_info = download_vid_info(vid_id)
messages = download_messages_from_twitch(vid_id)
print(vid_info)
for message in messages:
    print(message["commenter"]["display_name"] + ": " + message["message"]["body"])
# print(messages)
