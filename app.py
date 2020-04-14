from moviepy.editor import *
import cv2
import pytesseract
import numpy as np
import random as rng

rng.seed(12345)


# 0, 1, 2, 7 -> out.mp4.
# 3, 4, 9 -> 42;33
# 5, 6 -> 2;14;30
# 8 -> 2;18;30

# video = VideoFileClip("Twitch.mp4")
# v1 = video.subclip(42 * 60 + 30, 42 * 60 + 35)
# v1.write_videofile("349.mp4")
#
# v1 = video.subclip(2 * 60 * 60 + 14 * 60 + 25, 2 * 60 * 60 + 14 * 60 + 30)
# v1.write_videofile("56.mp4")
#
# v1 = video.subclip(2 * 60 * 60 + 18 * 60 + 25, 2 * 60 * 60 + 18 * 60 + 30)
# v1.write_videofile("8.mp4")


# v1 = video.subclip(745,761)
# v2 = video.subclip(12352, 12368)
# result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
# v2.write_videofile("out.mp4") # Many options...
# v1.write_videofile("out1.mp4") # Many options...


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
    cdst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

    cv2.imshow('linesDetected.jpg', cdst)
    cv2.waitKey(3000)


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


i = 0


def get_score_from_frame(frame):
    score_gray = get_score_area(frame)
    bound_rect = get_letters_bounding(score_gray)
    global i

    if bound_rect:
        cv2.imshow('aa', score_gray)

    for rect in bound_rect:
        letterimage = score_gray[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
        cv2.imwrite("train_data/" + str(i) + ".jpg", letterimage)
        i += 1
        # letter = recognizedigit(letterimage)
        # print(letter, end="")
    print(i)
    # cv2.imshow("aa", score_area)
    # if text.count("/") == 2:
    #     kills, deads, assists = text.split("/")
    #     if kills.isdigit() and deads.isdigit() and assists.isdigit():
    #         return int(kills), int(deads), int(assists)
    # return None


for f_name in ["out.mp4", "8.mp4", "56.mp4", "349.mp4"]:
    for frame, frame_time in every_n_frame(f_name, 60):
        get_score_from_frame(frame)
#     key = cv2.waitKey(30)
