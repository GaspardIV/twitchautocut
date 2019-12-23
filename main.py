import json
from main_download import download_info_and_messages_to_files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def preprocess(file_name):
    m_bodies = []
    m_created = []
    with open(file_name) as json_file:
        messages = json.load(json_file)
        for message in messages:
            m_bodies.append(message["message"]["body"])
            try:
                m_created.append(datetime.datetime.strptime(message["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            except:
                m_created.append(datetime.datetime.strptime(message["created_at"], "%Y-%m-%dT%H:%M:%SZ"))
    start = min(m_created)
    end_of_stream = max(m_created)
    stream_duration = int((end_of_stream - start).total_seconds()) + 2
    second_to_messages = {new_list: [] for new_list in range(stream_duration)}

    for i in range(len(m_created)):
        time = int((m_created[i] - start).total_seconds())
        second_to_messages[time].append(m_bodies[i])
    return start, second_to_messages


def get_statistics():
    messages_count = sum(len(second_to_messages[i]) for i in second_to_messages)
    duration = len(second_to_messages)
    return duration, messages_count


def convert_to_count(second_to_messages, pattern):
    pattern = pattern.lower()
    return {sec: sum(1 if pattern in m.lower() else 0 for m in second_to_messages[sec]) for sec in second_to_messages}


if __name__ == '__main__':
    # 506496104
    vid_id = "523163459"
    # download_info_and_messages_to_files(vid_id)
    start, second_to_messages = preprocess(vid_id + '__messages.txt')
    second_to_xdcount = convert_to_count(second_to_messages, "xd")
    second_to_pogcount = convert_to_count(second_to_messages, "pogchamp")
    print(second_to_messages)
    print(second_to_xdcount)
    print(second_to_pogcount)
