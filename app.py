from moviepy.editor import *
import cv2
import pytesseract
import numpy as np
import random as rng
rng.seed(12345)


# video = VideoFileClip("Twitch.mp4")
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


def get_score_from_frame(frame):
    width = len(frame[0])
    subimage = frame[0:30, width - 257:width - 155]

    gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, 63, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = []

    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        parent = hierarchy[0][i][3]
        if parent != -1 and hierarchy[0][parent][3] == -1: #it has parent, but does not have a grandpa
            boundRect.append(cv2.boundingRect(contours_poly[i]))

    for i in range(len(boundRect)):
        color = (0, rng.randint(0, 256), rng.randint(0, 256))
        cv2.rectangle(subimage, (int(boundRect[i][0]), int(boundRect[i][1])), (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)

    cv2.imshow('aa', subimage)
    text = pytesseract.image_to_string(th2)
    # cv2.imshow("aa", subimage)
    # todo findcountures i pojedynczo rozpoznowac z opcja single character moze???

    if text.count("/") == 2:
        kills, deads, assists = text.split("/")
        if kills.isdigit() and deads.isdigit() and assists.isdigit():
            return int(kills), int(deads), int(assists)
    return None

for frame, frame_time in every_n_frame("out.mp4", 10):
    get_score_from_frame(frame)
    key = cv2.waitKey(30)

# vidPath = 'out.mp4'

# source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)
# # need ffmpeg codec http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ and avbin on windows!!
# player.queue(MediaLoad)
# player.play()
