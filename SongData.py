
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

        # self.read_gems(gem_annotation)
        # self.regions_from_file(regions)

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

    def regions_from_file(self, filename):
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            self.regions.append((float(tokens[0]), float(tokens[2])))

    # updated method of reading data using tempo map, strumming patterns
    def read_gems_riptide(self, filename):

        strumming_patterns = [[1,3,6,7,8],[1,4,6,7,8],[1,4,6,7],[2,4,5,7,8]]

        lines = self.lines_from_file(filename)
        data = [(0,0)]
        tick = 0
        for line in lines:
            tokens = self.tokens_from_line(line)
            barline_time = float(tokens[0])
            # case where there is a strumming pattern and a chord
            try:
                strum_pattern, chord = tokens[1].split(',')
            # case where there chord, strumming pattern are None
            except ValueError:
                strum_pattern, chord = (None, None)
            data.append((barline_time, tick))
            tick += 1920
        print(data)
        tempo_map = TempoMap(data)

        riptide_gems = []


    # def read_bars(self,filename):
    #     bars = []
    #     lines = self.lines_from_file(filename)
    #     for line in lines:
    #         tokens = self.tokens_from_line(line)
    #         bars.append(float(tokens[0]))
    #     return bars


filename = "C:/Users/Ian McNally/Documents/Chord-Conqueror/annotations/RiptideBarlinesFull.txt"
x = SongData(filename, None)
x.read_gems_riptide(filename)