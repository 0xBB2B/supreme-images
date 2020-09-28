import requests, re, os, time
from bs4 import BeautifulSoup

BASE_URL = "https://www.supremenewyork.com"
PATH = "./jpg/"

def safe_name(str):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    s = re.sub(rstr, " ", str)
    return s

def detail(path, url):
    r = requests.get(BASE_URL + url)
    bs = BeautifulSoup(r.content, "html.parser")
    img = bs.find("img", id="img-main")['src']
    print(img)
    title = bs.find("h1", itemprop="name")
    color = bs.find("p", itemprop="model")
    r = requests.get("https:"+img)
    name = title.contents[0] + " - " + color.contents[0] + ".jpg"
    filename = safe_name(name)
    with open(path + filename, "wb") as fout:
        fout.write(r.content)

def nav(link):
    if link.text == "all" or link.text == "new":
        return
    name = safe_name(link.text)
    path = PATH+name+"/"
    if not os.path.exists(path):
        os.mkdir(path, 0o755)
    r = requests.get(BASE_URL + link['href'])
    bs = BeautifulSoup(r.content, "lxml")
    urls = bs.find_all("div", class_="inner-article")
    for url in urls:
        detail(path, url.a['href'])

def main():
    if not os.path.exists(PATH):
        os.mkdir(PATH, 0o755)
    r = requests.get(BASE_URL + "/shop/all")
    bs = BeautifulSoup(r.content, "lxml")
    links = bs.select("ul[id='nav-categories'] li a")
    for link in links:
        nav(link)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    used_time = round(end - start)
    hours = used_time // 3600
    minutes = (used_time - (hours * 3600)) // 60
    seconds = (used_time - (hours * 3600) - (minutes * 60))
    print("Used {} h {} m {} s".format(hours, minutes, seconds))
