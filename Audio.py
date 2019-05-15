from common.mixer import *
from common.wavegen import *
from common.wavesrc import *
from common.synth import *


# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_name):
        super(AudioController, self).__init__()
        self.set_song(song_name)

        self.audio = Audio(2)
        self.mixer = Mixer()

        self.mixer.add(self.bg)
        self.audio.set_generator(self.mixer)
        self.buffers = []
        self.synth = Synth('./data/FluidR3_GM.sf2')
        self.mixer.add(self.synth)
        self.channel = 2
        self.program =  (0, 24)
        self.synth.program(self.channel, self.program[0], self.program[1])
        self.shift = {"BrownEyedGirl": 0, "WithoutMe": -1, "Riptide": 1}

    # start / stop the song
    def set_song(self, song_name):
        self.song = song_name.split("/")[1]
        self.bg = WaveGenerator(WaveFile(song_name + ".wav"), False)
    def toggle(self):
        self.bg.play_toggle()
    def reset_synth(self):
        self.synth = Synth('./data/FluidR3_GM.sf2')
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
        pass
        # gen = WaveGenerator(WaveFile("music/Miss_sound.wav"))
        # self.mixer.add(gen)
        # gen.play_toggle()



    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        return self.bg.get_frame()

    def play_synth_note(self,note):
        if self.synth:
            self.synth.noteon(2, note + self.shift[self.song], 100)
        pass

    def note_off(self, note):
        if self.synth:
            self.synth.noteoff(2, note + self.shift[self.song])

