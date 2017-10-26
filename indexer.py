import pymorphy2
import re, string, pickle, os, math

class ReverseIndex:
    pregex = re.compile('[%s]' % re.escape(string.punctuation))
    #stoppos = ["PREP", "CONJ"]
    def __init__(self, stoppos:list):
        self.stoppos = stoppos
        self.words = {}
        self.length = 0
        self.analyzer = pymorphy2.MorphAnalyzer()

    def add(self, text:str):
        textpart = text.split("\n\n")[-1]
        tokens = [self.analyzer.normal_forms(self.pregex.sub('', x)) for x in textpart.split() if not any([tag._POS in self.stoppos for tag in self.analyzer.tag(x)])]
        tokens = [token for toklist in tokens for token in toklist]
        for token in tokens:
            self.words.setdefault(token, set()).add(self.length)
        self.length += 1
        print("Added a text")

    def get_idf(self, term):
        termlist = self.words.get(term, [])
        df = len(termlist) + 1

        return math.log(self.length / df)

    def load(self, name="index.pkl"):
        if name:
            with open(name, 'rb') as loadfile:
                tmp_dict = pickle.load(loadfile)

            self.__dict__.update(tmp_dict)

    def save(self, name="index.pkl"):
        with open(name, 'wb') as savefile:
            pickle.dump(self.__dict__, savefile, 2)

if __name__ == "__main__":
    paths = [x for x in os.listdir('.') if x.endswith(".txt")]
    index = ReverseIndex([])
    for path in paths:
        with open(path) as text:
            content = text.read()
            index.add(content)

    index.save()

    test_in = ReverseIndex([])
    test_in.load()

    print("done")