import requests
from bs4 import BeautifulSoup

class NewsArchiveGrabber():

    def __init__(self, mainlink:str, archlink:str, mod:str, step:int, stop:int):
        self.archive_link = archlink
        self.mainlink = mainlink
        self.modifier = mod
        self.step = step
        self.stop = stop
        self.links = []
        self.articles = []
        self.grab_article_links()
        self.grab_link_contents()
        self.print_texts()

    def grab_article_links(self):
        for i in range(0, self.stop, self.step):
            page = requests.get(self.mainlink, self.archive_link + modifier + str(i))
            soup = BeautifulSoup(page.text)
            headers = soup.find_all("h2", {'class':'zag'})
            cur_links = [x.a["href"] for x in headers]
            self.links.extend(cur_links)


    def grab_link_contents(self):
        for link in self.links:
            page = requests.get(self.mainlink + link)
            soup = BeautifulSoup(page.text)
            col = soup.find("div", {"class": "meedcol"})
            text = "\n".join([x.string for x in col.find_all("p") if x.string])
            title = soup.find("title").string
            date = soup.find("div", {"class":"bottomNews"}).span.string
            self.articles.append({"\n": text, "@da": date, "@ti": title, "@au": "Noname", "@url": link})

    def print_texts(self):
        for i in range(len(self.articles)):
            with open(str(i) + ".txt", "w") as writefile:
                for key in ["@ti", "@au", "@da", "@url","\n"]:
                    writefile.write("%s %s\n"%(key, self.articles[i][key]))





if __name__ == "__main__":
    mainlink = "http://m-v-news.ru/"
    archlink = "novosti/"
    modifier = "?curPos="

    grabber = NewsArchiveGrabber(mainlink, archlink, modifier, 10, 1320)