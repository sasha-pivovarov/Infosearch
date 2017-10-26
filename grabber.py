import requests
from bs4 import BeautifulSoup
import datetime

class NewsArchiveGrabber():

    def __init__(self, mainlink:str, archlink:str, step:int, stop:int, startdate:datetime):
        self.archive_link = archlink
        self.mainlink = mainlink
        self.startdate = startdate
        self.step = step
        self.stop = stop
        self.links = []
        self.articles = []
        self.grab_article_links()
        self.grab_link_contents()
        self.print_texts()

    def grab_article_links(self):
        print("Getting links...")
        dates = [self.startdate + datetime.timedelta(days=x) for x in range(0, (datetime.datetime.today() - start).days)]
        for date in dates:
            month = str(date.month)
            day = str(date.day)
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            page = requests.get(self.mainlink + self.archive_link + "%s/%s/%s" % (date.year, month, day))
            soup = BeautifulSoup(page.text)
            headers = soup.find_all("h2", {'class':'zag'})
            cur_links = [(x.a["href"], date) for x in headers]
            self.links.extend(cur_links)


    def grab_link_contents(self):
        print("Grabbing link contents...")
        for link_and_date in self.links:
            date = link_and_date[1]
            link = link_and_date[0]
            page = requests.get(self.mainlink + link)
            soup = BeautifulSoup(page.text)
            col = soup.find("div", {"class": "meedcol"})
            text = "\n".join([x.string for x in col.find_all("p") if x.string and not len(x.contents) > 1])
            title = soup.find("title").string
            if text:
                print("Got link with address %s" % link)
                self.articles.append({"\n": text, "@da": date, "@ti": title, "@au": "Noname", "@url": link})

    def print_texts(self):
        print("Writing files...")
        for i in range(len(self.articles)):
            with open(str(i) + ".txt", "w") as writefile:
                for key in ["@ti", "@au", "@da", "@url","\n"]:
                    writefile.write("%s %s\n"%(key, self.articles[i][key]))





if __name__ == "__main__":
    mainlink = "http://m-v-news.ru/"
    archlink = "arhiv/"
    start = datetime.datetime.strptime("01-01-2014", "%d-%m-%Y")
    # modifier = "?curPos="

    grabber = NewsArchiveGrabber(mainlink, archlink, 10, 1320, start)

