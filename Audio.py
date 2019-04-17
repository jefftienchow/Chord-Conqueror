from common.mixer import *
from common.wavegen import *
from common.wavesrc import *


# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_name, data):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.solo = WaveGenerator(WaveFile(song_name + "_solo.wav"), False)
        self.bg = WaveGenerator(WaveFile(song_name + "_bg.wav"),False)
        self.mixer.add(self.solo)
        self.mixer.add(self.bg)

        self.audio.set_generator(self.mixer)

    # start / stop the song
    def toggle(self):
        self.solo.play_toggle()
        self.bg.play_toggle()

    def reset(self):
        self.solo.reset()
        self.bg.reset()

    # mute / unmute the solo track
    def set_mute(self, mute):
        self.solo.set_mute(mute)

    # play a sound-fx (miss sound)
    def play_sfx(self):
        gen = WaveGenerator(WaveFile("music/Miss_sound.wav"))
        self.mixer.add(gen)
        gen.play_toggle()


    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        return self.solo.get_frame()