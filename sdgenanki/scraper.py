import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

SD_ROOT = "http://www.spanishdict.com/"

def get_conj(verb):
    url = SD_ROOT + "conjugate/" + verb
    r = requests.get(url)
    r.raise_for_status()
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    word_divs = soup.find_all("div", class_="vtable-word-contents")
    words = {}
    for word_div in word_divs:
        form = word_div.parent.parent("td")[0].text
        word_text = word_div.find("div", class_="vtable-word-text")
        if not word_text: continue
        word = "".join(word_text(string=True))
        conjugation = word_text["data-tense"]
        if not conjugation in words:
            words[conjugation] = { form : word }
        else:
            words[conjugation][form] = word
    return words
