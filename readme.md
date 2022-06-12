## Twitchautocut

Get the most interesting moments of your favorite streamer without watching the whole transimission. 
Twitchautocut downloads transmission recordings of league of legends streams from twitch.tv, then automatically detects interesting moments by using computervision analysis (detecting kills) and analysis of chat messages(people reaction of what they see), and make shots of them. 



For example this is the funniest moment from a 7 hour long stream of xayoo generated automatically. It worked perfectly:
https://user-images.githubusercontent.com/30477366/173252630-fd3513b8-ddd6-4dc4-8511-19775fa23669.mp4

And this is an automatically generated compilation of the most public-entertaining kills from the same stream. It's not perfect, but the results are promising. It's not perfect because of few reasons - for example public is reacting to music(they use the same pogchamp reaction for their favorite music and for a good plays), or to cursing, and because kill streak's and teamfights are merged and their rating is summed, and this causes the video less oriented for good plays, more for long fights with public-entertaining music. However it is easy to fix.
https://www.youtube.com/watch?v=PUwyX5wwrRk








install: opecv-python tesseract

https://github.com/UB-Mannheim/tesseract/wiki

add cccc\bbb\aaa\Tesseract-OCR to path for python tesseract bindings
