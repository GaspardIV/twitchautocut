import json
import datetime

from moviepy.editor import VideoFileClip


# video = VideoFileClip("Twitch.mp4")
# v1 = video.subclip(6336, 7000)
# v1 = video.subclip(start, end)
# out_name = "out/{}__{}-{}__{}-{}.mp4".format(f_name, start, end, prev_kda, kda)
# v1.write_videofile(out_name)
# v1.to_videofile("test5614.mp4", codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True,
#                 audio_codec='aac')

class QualityContentMaker:
    def __init__(self, vid_id) -> None:
        super().__init__()
        self.vid_id = vid_id
        self.video_info = self.readVideoInfo()
        self.messages = self.readMessages()
        self.stream_start = self.parseTime(self.video_info['created_at'])
        self.stream_duration = int(self.video_info['length'])
        self.timeToMessages = self.generateTimeToMessagesDict()
        self.timeToXDCount = self.getTimeToCount("xd")
        self.timeToPogCount = self.getTimeToCount("pogchamp")
        self.kdaList = self.getKdaList()

        print(self.kdaList)
        print(self.timeToXDCount)
        print(self.timeToPogCount)
        

    def readVideoInfo(self):
        file_name = "{}__vid_info.txt".format(self.vid_id)
        with open(file_name) as json_file:
            return json.load(json_file)

    def readMessages(self):
        file_name = "{}__messages.txt".format(self.vid_id)
        with open(file_name) as json_file:
            return json.load(json_file)

    def generateTimeToMessagesDict(self):
        m_bodies = []
        m_created = []
        for message in self.messages:
            m_bodies.append(message["message"]["body"])
            m_created.append(self.parseTime(message["created_at"]))
        second_to_messages = {new_list: [] for new_list in range(self.stream_duration + 2)}

        for i in range(len(m_created)):
            time = int((m_created[i] - self.stream_start).total_seconds())
            second_to_messages[time].append(m_bodies[i])
        return second_to_messages

    @staticmethod
    def parseTime(str_rep):
        try:
            return datetime.datetime.strptime(str_rep, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            return datetime.datetime.strptime(str_rep, "%Y-%m-%dT%H:%M:%SZ")

    def getTimeToCount(self, pattern):
        pattern = pattern.lower()
        return {sec: sum(1 if pattern in m.lower() else 0 for m in self.timeToMessages[sec]) for sec in
                self.timeToMessages}

    def getKdaList(self):
        file_name = "{}_kda.txt".format(self.vid_id)
        with open(file_name) as json_file:
            return json.load(json_file)


if __name__ == '__main__':
    # 506496104
    vid_id = "591019733"
    maker = QualityContentMaker(vid_id)
    # download_info_and_messages_to_files(vid_id)
    # start, second_to_messages = preprocess(vid_id + '__messages.txt')
    # second_to_xdcount = convert_to_count(second_to_messages, "xd")
    # second_to_pogcount = convert_to_count(second_to_messages, "pogchamp")
    # print(second_to_messages)
    # print(second_to_xdcount)
    # print(second_to_pogcount)

# if __name__ == '__main__':
#     v_id = "591019733"
#     with open(file_name) as json_file:
#     messages = json.load("{}__messages.txt".format(v_id))
#     info = json.load("{}__vid_info.txt".format(v_id))
#     kda = json.load("{}__kda.txt".format(v_id))
#     print(messages)
#     print(info)
#     print(kda)
