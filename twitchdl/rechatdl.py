from __future__ import print_function

import requests
import sys
import calendar
import time
import math
import json

CHUNK_ATTEMPTS = 6
CHUNK_ATTEMPT_SLEEP = 10
CLIENT_ID = "isaxc3wjcarzh4vgvz11cslcthw0gw"


def download_from_twitch_to_file(vid_id, file_name=None):
    if file_name is None:
        file_name = "vid_" + vid_id
    messages = download_messages_from_twitch(vid_id)
    print()
    print("saving to " + file_name)

    f = open(file_name, "w")
    f.write(json.dumps(messages))
    f.close()

    print("done!")


def download_vid_info(vid_id):
    print("downloading vid info for vod " + vid_id + "...")
    vid_info = requests.get("https://api.twitch.tv/kraken/videos/v" + vid_id,
                            headers={"Client-ID": CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}).json()
    if "error" in vid_info:
        sys.exit("got an error in vod info response: " + str(vid_info))
    print("done")
    return vid_info


def download_messages_from_twitch(vid_id):
    messages = []
    response = None
    print("downloading chat messages for vod " + vid_id + "...")
    while response is None or '_next' in response:
        query = ('cursor=' + response[
            '_next']) if response is not None and '_next' in response else 'content_offset_seconds=0'

        for i in range(0, CHUNK_ATTEMPTS):
            error = None
            try:
                response = requests.get("https://api.twitch.tv/v5/videos/" + vid_id + "/comments?" + query,
                                        headers={"Client-ID": CLIENT_ID}).json()
            except requests.exceptions.ConnectionError as e:
                error = str(e)
            else:
                if "errors" in response or "comments" not in response:
                    error = "error received in chat message response: " + str(response)

            if error is None:
                messages += response["comments"]
                break
            else:
                print("\nerror while downloading chunk: " + error)

                if i < CHUNK_ATTEMPTS - 1:
                    print("retrying in " + str(CHUNK_ATTEMPT_SLEEP) + " seconds ", end="")
                    print("(attempt " + str(i + 1) + "/" + str(CHUNK_ATTEMPTS) + ")")
                    time.sleep(CHUNK_ATTEMPT_SLEEP)
                else:
                    sys.exit("max retries exceeded.")

    print("done!")
    return messages
