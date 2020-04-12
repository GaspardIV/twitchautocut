from moviepy.editor import *
import cv2
import pytesseract

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
            time_in_sec = frame_num/fps
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
    subimage = frame[5:25,width-370:width]
    # cv2.rectangle(frame, (width-370, 5), (width, 25), (255, 255, 255), -1)
    cv2.imshow('Frame', frame)
    cv2.imshow('Frame2', subimage)
    print(pytesseract.image_to_string(subimage))



for frame, frame_time in every_n_frame("out.mp4", 10):
    # if frame_num < 5000:
    #     continue


    # cv2.putText(frame, str(frame_num), (15, 15),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    print(get_score_from_frame(frame))
    key = cv2.waitKey(30)

# vidPath = 'out.mp4'

# source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)
# # need ffmpeg codec http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ and avbin on windows!!
# player.queue(MediaLoad)
# player.play()
