from moviepy.editor import *
import cv2
import pytesseract
import numpy as np


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


def recognizedigit(src):
    # cdst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
    global knn
    ret, result, neighbours, dist = knn.find_nearest([src], k=5)
    return result[0]


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
    for i in range(1, len(bound_rect)):  # check if y's are the same
        if not abs(bound_rect[i][1] - bound_rect[i - 1][1]) < 5 or not abs(bound_rect[i][3] - bound_rect[i - 1][3]) < 5:
            return None
    return bound_rect


def get_score_from_frame(frame):
    score_gray = get_score_area(frame)
    bound_rect = get_letters_bounding(score_gray)
    global i

    if bound_rect:
        cv2.imshow('aa', score_gray)

    for rect in bound_rect:
        letterimage = score_gray[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
        cv2.imshow("letter", letterimage)
        letter = recognizedigit(letterimage)
        print(letter, end="")
    print(i)
    # cv2.imshow("aa", score_area)
    # if text.count("/") == 2:
    #     kills, deads, assists = text.split("/")
    #     if kills.isdigit() and deads.isdigit() and assists.isdigit():
    #         return int(kills), int(deads), int(assists)
    # return None

labels = []
train_data = []
for i in range(10):
    td = cv2.imread('train_data/{}.jpg'.format(i))
    train_data.append(np.float32(td))
    labels.append(i)
td = cv2.imread('train_data/_.jpg')
train_data.append(td)
labels.append(10)

knn = cv2.ml.KNearest_create()
# traindata = np.array(train_data, dtype=np.float32)
labels= np.array(labels, dtype=np.float32)
knn.train(train_data, cv2.ml.ROW_SAMPLE, labels)


for f_name in ["out.mp4", "8.mp4", "56.mp4", "349.mp4"]:
    for frame, frame_time in every_n_frame(f_name, 60):
        get_score_from_frame(frame)
        key = cv2.waitKey(1000)
