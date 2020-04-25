import cv2
import numpy as np
import os
import json
from datetime import datetime


class KDAMomentsExtractor:
    EVERY_NTH_FRAME = 20
    MODEL_PATH = None

    # MODEL_PATH = "./models/digit_model_1587679271.840106.xml"

    def __init__(self, vid_path) -> None:
        self.vid_path = vid_path
        if self.MODEL_PATH is not None:
            self.svm = cv2.ml.SVM_load(self.MODEL_PATH)
        else:
            self.svm = cv2.ml.SVM_create()
            self.svm.setType(cv2.ml.SVM_C_SVC)
            self.svm.setKernel(cv2.ml.SVM_LINEAR)
            # self.svm.
            self.train()

    def train(self):
        digits = []
        labels = []
        for i in range(11):
            dirdigits = self.readFolder("train_data/{}/".format(i))
            digits.extend(dirdigits)
            labels.extend([i] * len(dirdigits))
        digits = np.array(digits, np.float32)
        labels = np.array(labels, np.int)
        self.svm.trainAuto(digits, cv2.ml.ROW_SAMPLE, labels)
        self.svm.save("models/digit_model_{}.xml".format(datetime.now().timestamp()))

    def searchForMoreSamples(self):
        for frame, frame_time in self.every_n_frame(self.vid_path, self.EVERY_NTH_FRAME):
            letters = self.get_letters(frame)
            if letters:
                self.cutoutSamples(letters)

    def searchForKDAMoments(self):
        prev_kda = 0, 0, 0
        result = []
        for frame, frame_time in self.every_n_frame(self.vid_path, self.EVERY_NTH_FRAME):
            letters = self.get_letters(frame)
            if letters:
                kda = self.recognizeScore(letters)
                if kda is not None and kda != prev_kda:
                    print(frame_time, prev_kda, kda)
                    result.append((frame_time, prev_kda, kda))
                    prev_kda = kda

                    # start = max(int(frame_time) - 5, 0)
                    # end = min(int(frame_time) + 2, int(video.duration))
                    # v1 = video.subclip(start, end)
                    # out_name = "out/{}__{}-{}__{}-{}.mp4".format(f_name, start, end, prev_kda, kda)
                    # # v1.write_videofile(out_name)
                    # v1.to_videofile(out_name, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True,
                    #                 audio_codec='aac')
        return result

    @staticmethod
    def frames(file, do_print=False):
        capture = cv2.VideoCapture(file)
        frame_num = 0
        percent = 0
        total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        while True:
            ret, frame = capture.read()
            if frame is not None:
                frame_num += 1
                time_in_sec = frame_num / fps
                if do_print:
                    if frame_num >= total / 100 * percent:
                        print("[{}] {}% done".format(datetime.now(), percent))
                        percent += 1
                yield frame, time_in_sec
            else:
                print("[{}] FINISHED".format(datetime.now()))
                break

    def every_n_frame(self, file, n):
        i = 0
        for frame, frame_time in self.frames(file, True):
            if i == 0:
                yield frame, frame_time
            i += 1
            i %= n

    def recognizeDigit(self, src):
        try:
            arr = [self.get_feature(src)]
            arr = np.array(arr, np.float32)
            result = self.svm.predict(arr)[1]
        except:
            result = [[-1]]  # ERROR
        return self.digitToLabel(result[0][0])

    @staticmethod
    def get_score_area(frame):
        width = len(frame[0])
        subimage = frame[0:30, width - 257:width - 155]
        gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
        _, th2 = cv2.threshold(gray, 63, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return th2

    @staticmethod
    def get_letters_bounding(score_gray):
        contours, hierarchy = cv2.findContours(score_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_poly = [None] * len(contours)
        bound_rect = []

        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            parent = hierarchy[0][i][3]
            if parent != -1 and hierarchy[0][parent][3] == -1:  # it has parent, but does not have a grandpa
                rect = cv2.boundingRect(contours_poly[i])
                width = rect[2]
                height = rect[3]
                if height > 5 and width > 2:
                    bound_rect.append(rect)
        bound_rect = sorted(bound_rect)
        return bound_rect

    @staticmethod
    def areBoundingsFine(bound_rect):
        if len(bound_rect) < 5:
            return False

        for i in range(1, len(bound_rect)):  # check if y's are the same
            if not abs(bound_rect[i][1] - bound_rect[i - 1][1]) < 5 or not abs(
                    bound_rect[i][3] - bound_rect[i - 1][3]) < 5:
                return False
        return True

    def get_letters(self, frame):
        letters = []
        score_gray = self.get_score_area(frame)
        bound_rect = self.get_letters_bounding(score_gray)
        if self.areBoundingsFine(bound_rect):
            for rect in bound_rect:
                letterimage = score_gray[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
                letters.append(letterimage)
            return letters

    @staticmethod
    def get_feature(image):
        bordered = np.zeros([20, 20], dtype=np.uint8)
        bordered.fill(255)
        bordered[0:image.shape[0], 0:image.shape[1]] = image
        ret = bordered.astype(np.float32)
        ret = 255 - ret
        return ret.ravel()

    def addFileData(self, file):
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.get_feature(image)

    def readFolder(self, folder_name):
        res = []
        for file in os.listdir(folder_name):
            res.append(self.addFileData(folder_name + file))
        return res

    @staticmethod
    def digitToLabel(label):
        return {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "/", -1: "ERR"}[
            label]

    @staticmethod
    def labelToDigit(digit):
        return {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "/": 10, "ERR": -1}[
            digit]

    def recognizeScore(self, letters):
        score = ''.join([self.recognizeDigit(letter) for letter in letters])
        try:
            if score.count("/") == 2:
                kills, deads, assists = score.split("/")
                return int(kills), int(deads), int(assists)
        except:
            return None
        return None

    def cutoutSamples(self, letters):
        for letter in letters:
            result = self.recognizeDigit(letter)
            filename = './more_labels/{}/{}.jpg'.format(self.labelToDigit(result), datetime.now().timestamp())
            print("writing label:", filename)
            cv2.imwrite(filename, letter)


if __name__ == '__main__':
    v_id = "591019733"
    kdaMomentsExtractor = KDAMomentsExtractor(v_id + ".mp4")
    res = kdaMomentsExtractor.searchForKDAMoments()
    with open("{}_kda.txt".format(v_id), 'w') as file:
        json.dump(res, file)

    # kdaMomentsExtractor.searchForMoreSamples()

    exit(0)

#     TODO WIECEJ SAMPLI 9 !!!!!!!!!!!!!!!!! BO MYLI SIE Z 0 CZASAMI
# todo jak sample z każdego kilka zbierać, ale bez '/' może
# todo inny filmik pobrac :0
# jask jest jkis wynik pozniej inny pozniej znowu tamten to ten po srodku moze sie nie lcizyc
# https://github.com/EnterGin/Twitch-VOD-Downloader/blob/master/Twitch_VOD_Downloader.py
# to wyglada prosto
# https://github.com/0xf77/twitch-dl
# todo
