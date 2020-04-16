from moviepy.editor import *
import cv2
import pytesseract
import numpy as np
import os


def frames(file, do_print=False):
    capture = cv2.VideoCapture(file)
    frame_num = 0
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(capture.get(cv2.CAP_PROP_FPS))
    while True:
        ret, frame = capture.read()
        if frame is not None:
            frame_num += 1
            time_in_sec = frame_num / fps
            if do_print:
                print('{num}/{totalnum}'.format(num=frame_num, totalnum=total))
            yield frame, time_in_sec
        else:
            break


def every_n_frame(file, n):
    i = 0
    for frame, frame_time in frames(file):
        if i == 0:
            yield frame, frame_time
        i += 1
        i %= n


def recognizedigit(src, knn):
    arr = [get_feature(src)]
    arr = np.array(arr, np.float32)
    ret, result, neighbours, dist = knn.findNearest(arr, k=5)
    return labeltodigit(result[0])


def get_score_area(frame):
    width = len(frame[0])
    subimage = frame[0:30, width - 257:width - 155]
    gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, 63, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return th2


def get_letters_bounding(score_gray):
    contours, hierarchy = cv2.findContours(score_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_poly = [None] * len(contours)
    bound_rect = []

    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        parent = hierarchy[0][i][3]
        if parent != -1 and hierarchy[0][parent][3] == -1:  # it has parent, but does not have a grandpa
            bound_rect.append(cv2.boundingRect(contours_poly[i]))
    bound_rect = sorted(bound_rect)
    return bound_rect


def boundings_fine(bound_rect):
    for i in range(1, len(bound_rect)):  # check if y's are the same
        if not abs(bound_rect[i][1] - bound_rect[i - 1][1]) < 5 or not abs(bound_rect[i][3] - bound_rect[i - 1][3]) < 5:
            return False
    return True


def get_letters(frame):
    letters = []
    score_gray = get_score_area(frame)
    bound_rect = get_letters_bounding(score_gray)
    if boundings_fine(bound_rect):
        # cv2.imshow('aa', score_gray)
        for rect in bound_rect:
            letterimage = score_gray[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
            letters.append(letterimage)
        return letters


def get_feature(image):
    bordered = np.zeros([20, 20], dtype=np.uint8)
    bordered.fill(255)
    bordered[0:image.shape[0], 0:image.shape[1]] = image
    ret = bordered.astype(np.float32)
    ret = 255 - ret
    return ret.ravel()


def addFileData(file):
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return get_feature(image)


def readFolder(folder_name):
    res = []
    for file in os.listdir(folder_name):
        res.append(addFileData(folder_name + file))
    return res


def train():
    digits = []
    labels = []
    for i in range(11):
        dirdigits = readFolder("train_data/{}/".format(i))
        digits.extend(dirdigits)
        labels.extend([i] * len(dirdigits))
    digits = np.array(digits, np.float32)
    labels = np.array(labels, np.float32)
    knn = cv2.ml.KNearest_create()
    knn.train(digits, cv2.ml.ROW_SAMPLE, labels)
    return knn


def labeltodigit(label):
    return {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "/"}[label[0]]


def recognizeScore(letters, knn):
    score = ''.join([recognizedigit(letter, knn) for letter in letters])
    if score.count("/") == 2:
        kills, deads, assists = score.split("/")
        return int(kills), int(deads), int(assists)
    return None


video = VideoFileClip("out.mp4")
# print(video.duration)
# exit(0)
if __name__ == '__main__':
    knn = train()
    # for f_name in ["out.mp4", "8.mp4", "56.mp4", "349.mp4"]:
    for f_name in ["out.mp4"]:
        prev_kda = None
        for frame, frame_time in every_n_frame(f_name, 5):
            letters = get_letters(frame)
            if letters:
                # kills, deaths, assists = recognizeScore(letters, knn)
                kda = recognizeScore(letters, knn)
                if kda != prev_kda:
                    print(prev_kda, kda, frame_time)
                    start = max(int(frame_time) - 5, 0)
                    end = min(int(frame_time) + 2, int(video.duration))
                    v1 = video.subclip(start, end)
                    v1.write_videofile("out/{}__{}-{}__{}-{}.mp4".format(f_name, start, end, prev_kda, kda))
                    v1.close()
                    prev_kda = kda
                    cv2.imshow("xd", frame)
                    cv2.waitKey(30)
    exit(0)
