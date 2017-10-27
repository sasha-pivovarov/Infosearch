from indexer import ReverseIndex
import os, pickle, datetime



class BM25Ranking:

    def __init__(self, k:float=1.4, b:float=0.75, loadname = "index.pkl"):
        self.reverse = ReverseIndex([])
        self.reverse.load(loadname)
        self.texts = {}
        self.length = 0
        self.amount = 0
        self.k = k
        self.b = b

    def avg_freq(self):
        return self.length / self.amount

    def normalize(self, words:list):
        return [self.reverse.analyzer.normal_forms(self.reverse.pregex.sub('', x)) for x in words if not any([tag._POS in self.reverse.stoppos for tag in self.reverse.analyzer.tag(x)])]

    def get_tf(self, term:str, text:list):
        return text.count(term)

    def load_texts(self, path="."):
        texts = [x for x in os.listdir(path) if x.endswith(".txt")]
        for text in texts:
            with open(text, "r", encoding="utf-8") as io:
                frags = io.read().split("@")
                if len(frags) != 5: continue
                lfrag = frags[4].split("\n\n")
                if len(lfrag) != 2: continue
                orig_text = lfrag[1]
                tokens = self.normalize(lfrag[1].split()[1:])
                tokens = [token for tokenlist in tokens for token in tokenlist]
                title = frags[1].lstrip("ti")
                date = frags[3].lstrip("da")
                url = lfrag[0].lstrip("url")
                if title not in self.texts.keys():
                    self.texts[title] = {"tokens": tokens, "date": date, "url": url, "orig":orig_text, "title":title}
                    self.length += len(text)
                    self.amount += 1
                    print("Loaded a text")

    def load(self, name="ranker.pkl"):
        if name:
            with open(name, 'rb') as loadfile:
                tmp_dict = pickle.load(loadfile)

            self.__dict__.update(tmp_dict)

    def save(self, name="ranker.pkl"):
        with open(name, 'wb') as savefile:
            pickle.dump(self.__dict__, savefile, 2)

    def score_document(self, query:str, doc:dict):
        terms = self.normalize(query.split())
        terms = [term for termlist in terms for term in termlist]
        term_scores = []
        for term in terms:
            idf = self.reverse.get_idf(term)
            tf = doc["tokens"].count(term)
            numerator = float(tf * (self.k + 1))
            denominator = tf + self.k * (1 - self.b + self.b * (float(len(doc["tokens"])) / self.avg_freq()))
            score = idf * (numerator / denominator)
            term_scores.append(score)

        return sum(term_scores)

    def process_query(self, query:str, nresults:int=15):
        docscores = {x["title"]: self.score_document(query, x) for x in self.texts.values()}
        titles = sorted(self.texts.keys(), key=lambda x: docscores[x], reverse=True)
        return [(self.texts[title], docscores[title]) for title in titles if docscores[title]!=0.0][:nresults]


if __name__ == "__main__":
    ranking = BM25Ranking()
    ranking.load_texts()
    ranking.save()
    print("Ranker loaded")
    results = ranking.process_query("баня на севастопольской")
    print("Done")

