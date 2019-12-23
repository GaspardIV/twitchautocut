import pyglet
from moviepy.editor import *
pyglet.lib.load_library('avbin')
pyglet.have_avbin=True


video = VideoFileClip("Twitch.mp4")
v1 = video.subclip(745,761)
v2 = video.subclip(12352, 12368)
# result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
v2.write_videofile("out.mp4") # Many options...
v1.write_videofile("out1.mp4") # Many options...

vidPath = 'out.mp4'

window = pyglet.window.Window()
player = pyglet.media.Player()
# source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)
# # need ffmpeg codec http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ and avbin on windows!!
# player.queue(MediaLoad)
# player.play()

@window.event
def on_draw():
    # window.clear()
    # label.draw()
    if player.source and player.source.video_format:
        player.get_texture().blit(50, 50)

@window.event
def on_key_press(symbol, modifiers):
    if (65288, 16) == (symbol, modifiers):
        print("backspace")
    if (65293, 16) == (symbol, modifiers):
        print("enter")
    if (65361, 16) == (symbol, modifiers):
        print("left")
    if (65363, 16) == (symbol, modifiers):
        print("right")
    if (65361, 18) == (symbol, modifiers):
        print("ctrl left")
    if (65363, 18) == (symbol, modifiers):
        print("ctrl right")

pyglet.app.run()