
from common.clock import TempoMap

# holds data for gems and barlines.
class SongData(object):
    def __init__(self, gem_annotation, regions):
        super(SongData, self).__init__()
        self.chords = []
        self.bars = []
        self.gems = []
        self.regions = []
        self.sections = []

        self.read_gems(gem_annotation)
        self.regions_from_file(regions)

    def get_sections(self):
        return self.sections

    def get_gems(self):
        return self.gems

    def get_bars(self):
        return self.bars

    def get_chords(self):
        return self.chords

    def get_regions(self):
        return self.regions

    def lines_from_file(self, filepath):
        with open(filepath) as file:
            return file.readlines()

    def tokens_from_line(self,line):
        new_str = line.strip()
        new_str = new_str.strip("\n")
        return new_str.split("\t")

    # read the gems and song data. You may want to add a secondary filepath
    # argument if your barline data is stored in a different txt file.
    def read_gems(self, filename):
        if filename == 'annotations/BrownEyedGirlAnnotationFull.txt':

            lines = self.lines_from_file(filename)

            last_chord = None
            for line in lines:
                tokens = self.tokens_from_line(line)
                if tokens[1] == "1":
                    self.bars.append(float(tokens[0]))
                else:
                    self.gems.append((float(tokens[0]), tokens[1]))
                    if tokens[1] not in self.chords:
                        self.chords.append(tokens[1])
                    if tokens[1] != last_chord:
                        self.sections.append((float(tokens[0]), tokens[1]))
                        last_chord = tokens[1]
        else:
            print('nope')
            self.read_gems_riptide(filename)

    def regions_from_file(self, filename):
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            self.regions.append((float(tokens[0]), float(tokens[2])))

    # updated method of reading data using tempo map, strumming patterns
    def read_gems_riptide(self, filename):
        # all strumming patterns used in Riptide (in eighth notes)
        strumming_patterns = [[1], [1,3,6,7,8],[1,4,6,7,8],[1,4,6,7],[2,4,5,6,7,8]]
        lines = self.lines_from_file(filename)
        data = [(0,0)]
        patterns = []
        chords = []
        tick = 0
        for index, line in enumerate(lines):

            tokens = self.tokens_from_line(line)
            barline_time = float(tokens[0])

            # case where there is a strumming pattern and a chord
            try:
                strum_pattern, chord = tokens[1].split(',')
                if chord not in self.chords:
                    self.chords.append(chord)
                if strum_pattern == 'single':
                    strum_pattern = 0
                else:
                    strum_pattern = int(strum_pattern)
            # case where there chord, strumming pattern are None
            except ValueError:
                strum_pattern, chord = (None, None)
            
            data.append((barline_time, tick))
            patterns.append(strum_pattern)
            chords.append(chord)
            tick += 1920
        print(self.chords)
        riptide_gems = []
        tempo_map = TempoMap(data)
        assert(len(patterns) == len(chords))
        assert(len(patterns) == len(data) - 1)
        for i in range(len(patterns)):
            barline_time, barline_tick = data[i + 1]
            self.bars.append(barline_time)
            for j in range(1, 4):
                self.bars.append(tempo_map.tick_to_time(barline_tick + 480 * j))
            if patterns[i] is not None:
                for j in strumming_patterns[patterns[i]]:
                    tick = barline_tick + (j - 1) * 240
                    time = tempo_map.tick_to_time(tick)
                    self.gems.append((time, chords[i]))

