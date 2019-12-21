import pyglet
# from pyglet.media import *
# from pyglet.window import *

window = pyglet.window.Window()
# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=window.width // 2, y=window.height // 2,
#                           anchor_x='center', anchor_y='center')

vidPath = 'Twitch.mp4'
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad = pyglet.media.load(vidPath)

player.queue(MediaLoad)
player.play()

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