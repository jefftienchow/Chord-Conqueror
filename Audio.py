from common.mixer import *
from common.wavegen import *
from common.wavesrc import *


# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_name, regions):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.bg = WaveGenerator(WaveFile(song_name + ".wav"),False)
        self.mixer.add(self.bg)
        self.audio.set_generator(self.mixer)
        self.regions_data = regions
        self.buffers = []

        for region in self.regions_data:
            start_frame = int(region[0] * Audio.sample_rate)
            num_frames = int(region[1] * Audio.sample_rate)
            self.buffers.append(WaveBuffer(song_name + ".wav", start_frame, num_frames))
            print(start_frame)
            print(num_frames)
        self.cur_region = WaveGenerator(self.buffers[0])
        self.cur_region_idx = 0
        self.mixer.add(self.cur_region)


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

    def replay_region(self):
        self.cur_region.release()
        self.cur_region = WaveGenerator(self.buffers[self.cur_region_idx])
        self.mixer.add(self.cur_region)
        self.cur_region.play_toggle()

    def next_region(self):
        self.cur_region.release()
        self.cur_region_idx += 1

        #wrap around regions when they run out
        try:
            self.cur_region = WaveGenerator(self.buffers[self.cur_region_idx])
        except:
            self.cur_region_idx = 0
            self.cur_region = WaveGenerator(self.buffers[self.cur_region_idx])
        self.mixer.add(self.cur_region)

    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        return self.bg.get_frame()