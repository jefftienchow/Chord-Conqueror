# holds data for gems and barlines.
class SongData(object):
    def __init__(self, gem_annotation, bar_annotation):
        super(SongData, self).__init__()
        self.gems = self.read_gems(gem_annotation)
        self.bars = self.read_bars(bar_annotation)

    def get_gems(self):
        return self.gems

    def get_bars(self):
        return self.bars

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
        gems = []
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            gems.append((float(tokens[0]), int(tokens[1])))
        return gems

    def read_bars(self,filename):
        bars = []
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            bars.append(float(tokens[0]))
        return bars