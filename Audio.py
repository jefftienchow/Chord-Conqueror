from common.mixer import *
from common.wavegen import *
from common.wavesrc import *


# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_name):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.bg = WaveGenerator(WaveFile(song_name + ".wav"),False)
        self.mixer.add(self.bg)
        self.audio.set_generator(self.mixer)
        self.buffers = []

    # start / stop the song
    def toggle(self):
        self.bg.play_toggle()

    def reset(self):
        self.bg.reset()

    def set_start(self, start):
        self.bg.set_start(int(start * 44100))

    def set_stop(self, stop):
        if stop == None:
            self.bg.set_stop(None)
        else:
            self.bg.set_stop(int(stop * 44100))

    # mute / unmute the solo track
    def set_mute(self, mute):
        pass

    # play a sound-fx (miss sound)
    def play_sfx(self):
        gen = WaveGenerator(WaveFile("music/Miss_sound.wav"))
        self.mixer.add(gen)
        gen.play_toggle()



    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        return self.bg.get_frame()