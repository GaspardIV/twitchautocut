import json
from rechatdl import download_messages_from_twitch, download_vid_info


def download_info_and_messages_to_files():
    vid_id = "506496104"  # todo from args
    vid_info = download_vid_info(vid_id)
    messages = download_messages_from_twitch(vid_id)

    with open(vid_id + '__vid_info.txt', 'w') as outfile:
        json.dump(vid_info, outfile)

    with open(vid_id + '__messages.txt', 'w') as outfile:
        json.dump(messages, outfile)


if __name__ == '__main__':
    download_info_and_messages_to_files()
