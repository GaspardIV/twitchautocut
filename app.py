from moviepy.editor import *
import cv2
import pytesseract
import numpy as np


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
    height = len(frame)
    width = len(frame[0])
    # subimage = frame[5:25,width-370:width]
    subimage = frame[0:30, width - 257:width - 155]
    gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, 63, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(th2)

    fgmask2 = fgbg2.apply(th2)
    fgmask3 = fgbg3.apply(th2)
    cv2.imshow("aa", fgmask2)
    cv2.imshow("bb", fgmask3)
    print(cv2.countNonZero(fgmask2), cv2.countNonZero(fgmask3),)
    # todo findcountures i pojedynczo rozpoznowac z opcja single character moze???
    if text.count("/") == 2:
        kills, deads, assists = text.split("/")
        if kills.isdigit() and deads.isdigit() and assists.isdigit():
            return int(kills), int(deads), int(assists)
    return None

# creating object
fgbg2 = cv2.createBackgroundSubtractorMOG2()
fgbg3 = cv2.createBackgroundSubtractorKNN()

for frame, frame_time in every_n_frame("out.mp4", 10):
    get_score_from_frame(frame)
    key = cv2.waitKey(30)

# vidPath = 'out.mp4'

# source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)
# # need ffmpeg codec http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ and avbin on windows!!
# player.queue(MediaLoad)
# player.play()
