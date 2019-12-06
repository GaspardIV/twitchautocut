import json
from main_download import download_info_and_messages_to_files
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# download_info_and_messages_to_files()

m_bodies = []
m_created = []
with open('506496104__messages.txt') as json_file:
    messages = json.load(json_file)
    for message in messages:
        m_bodies.append(message["message"]["body"])
        m_created.append(message["created_at"])
df = pd.DataFrame({"time": m_created, "mess": m_bodies})
df.time = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S.%f')
df.set_index(["time"], inplace=True)
print(df.index)
df.groupby([df.index.year, df.index.month, df.index.day, df.index.hour, df.index.minute, df.index.second]).count().plot(kind="bar")
plt.show()
print(df.head())
print(df.tail())
