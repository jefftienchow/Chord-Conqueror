# holds data for gems and barlines.
class SongData(object):
    def __init__(self, gem_annotation):
        super(SongData, self).__init__()
        self.chords = []
        self.bars = []
        self.gems = []

        self.read_gems(gem_annotation)

    def get_gems(self):
        return self.gems

    def get_bars(self):
        return self.bars

    def get_chords(self):
        return self.chords

    def lines_from_file(self,filepath):
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

        for line in lines:
            tokens = self.tokens_from_line(line)
            if tokens[1] == "1":
                self.bars.append(float(tokens[0]))
            else:
                self.gems.append((float(tokens[0]), tokens[1]))
                if tokens[1] not in self.chords:
                    self.chords.append(tokens[1])

    # def read_bars(self,filename):
    #     bars = []
    #     lines = self.lines_from_file(filename)
    #     for line in lines:
    #         tokens = self.tokens_from_line(line)
    #         bars.append(float(tokens[0]))
    #     return bars