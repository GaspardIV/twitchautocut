import json
import datetime
import os, sys
from moviepy.editor import VideoFileClip


class InterestingMoment:
    def __init__(self, start, end) -> None:
        super().__init__()
        self.start = start
        self.end = end
        # self.from


class KDAInterestingMoment(InterestingMoment):
    def __init__(self, start, end, scores) -> None:
        super().__init__(start, end)
        self.xdPogCount = 0
        self.scores = []
        self.xdCount = 0
        self.pogCount = 0
        self.scores = scores

    def tryToMergeWith(self, other):
        if not other.scores[0] in self.scores and self.isOverlaping(other):
            self.scores.extend(other.scores)
            self.start = min(self.start, other.start)
            self.end = max(self.end, other.end)
            return True
        return False

    def isOverlaping(self, other):
        return other.start < self.start < other.end or self.start < other.start < self.end

    def __str__(self) -> str:
        return "KDAInterestingMoment: |" + str(self.start) + " -> " + str(self.end) + "| points: " + str(
            self.xdPogCount) + " scoreslen: " + str(len(self.scores))


class QualityContentMaker:
    def __init__(self, vid_id) -> None:
        super().__init__()
        self.vid_id = vid_id
        self.video_info = self.readVideoInfo()
        self.messages = self.readMessages()
        self.stream_start = self.parseTime(self.video_info['created_at'])
        self.stream_duration = int(self.video_info['length']) + 1
        self.timeToMessages = self.generateTimeToMessagesDict()
        self.timeToXDCount = self.getTimeToCount("xd")
        self.timeToPogCount = self.getTimeToCount("pogchamp")
        self.kdaList = self.getKdaList()
        self.kdaMoments = self.getMergedKdaMoments(self.kdaList)
        self.video = None
        self.timeToXDPogCount = {x: self.timeToXDCount[x] + self.timeToPogCount[x] for x in self.timeToPogCount}

        # todo top 5 momentow pogchamp oddalonych od siebie o przynajmniej tam minute i wuciac 30 sec (15, 15)
        # top 30 xd sorted ascending (or shuffled -> to test which has better views)(or one good one worse from the middle so thee best one is on the begginig)
        # top 30 pogchamp sorted ascending (or shuffled -> to test which has better views)
        # top 30 pogchamp + xd sorted scending (or shuffled -> to test which has better views)
        # top 50 kills sorted sorted ascending (or shuffled -> to test which has better views)
        # checkc for multikill?

        self.countXDPOGForKdaMoments()
        print(self.kdaList)
        print(self.timeToXDCount)
        print(self.timeToPogCount)
        self.TOPGeneralKdaMoments = sorted(self.kdaMoments, key=lambda moment: moment.xdPogCount, reverse=True)
        self.TOPxdKdaMoments = sorted(self.kdaMoments, key=lambda moment: moment.xdCount, reverse=True)
        self.TOPpogKdaMoments = sorted(self.kdaMoments, key=lambda moment: moment.xdCount, reverse=True)

        # TODO; ADD top xd moments

        # for x in self.TOPpogKdaMoments:
        #     print(x)
        # print("=========")
        # for x in self.TOPxdKdaMoments:
        #     print(x)
        # print("=========")
        # for x in self.TOPGeneralKdaMoments:
        #     print(x)

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
        second_to_messages = {new_list: [] for new_list in range(self.stream_duration)}
        print(self.stream_duration)
        for i in range(len(m_created)):
            time = int((m_created[i] - self.stream_start).total_seconds())
            if time < self.stream_duration:
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

    def getMergedKdaMoments(self, kdaList):
        res = []
        for i, el in enumerate(kdaList):
            moment = KDAInterestingMoment(el[0] - 13, el[0] + 13, [el[2]])
            merged = False
            for res_moment in res:
                if res_moment.isOverlaping(moment):
                    if res_moment.tryToMergeWith(moment):
                        print("merged", res_moment, moment)
                        merged = True
            if not merged:
                res.append(moment)
        return res

    def countXDPOGForKdaMoments(self):
        for moment in self.kdaMoments:
            for i in range(int(moment.start), int(moment.end + 1)):
                if 0 <= i < self.stream_duration:
                    moment.pogCount += self.timeToPogCount[i]
                    moment.xdCount += self.timeToXDPogCount[i]
                    moment.xdPogCount += self.timeToXDPogCount[i]

    def writeOutputToDIR(self, vid_id):
        self.video = VideoFileClip(vid_id+".mp4")
        dir_name = "out_" + vid_id
        self.mkDir(dir_name)
        self.writeMomentsList(self.TOPGeneralKdaMoments[:50], dir_name+"/Top50GenKdaMOM")
        self.writeMomentsList(self.TOPxdKdaMoments[:50], dir_name+"/Top50XdKdaMOM")
        self.writeMomentsList(self.TOPpogKdaMoments[:50], dir_name+"/Top50PogKdaMOM")

    def writeMomentsList(self, list, dir):
        for i, m in enumerate(list):
            v1 = self.video.subclip(m.start, m.end)
            out_name = dir+"/vid_top{}_t{}-{}.mp4".format(i+1, m.start, m.end)
            # v1.write_videofile(out_name)
            v1.to_videofile(out_name, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

    def mkDir(self, dir):
        try:
            os.mkdir(dir)
        except:
            pass


if __name__ == '__main__':
    # 506496104
    vid_id = "591019733"
    maker = QualityContentMaker(vid_id)

    maker.writeOutputToDIR(vid_id)
    exit()
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
