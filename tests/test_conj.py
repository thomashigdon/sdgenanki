from context import sdgenanki
import sdgenanki.scraper as scraper

import os
import pytest
import requests_mock

test_data = \
{
    "tener" :
    [
        (("spanish" , "tengo"),
         ("english" , "I have"),
         ("tense" , "presentIndicative"),
#         ("subject" , "yo"),
        ),
    ]
}

def get_test_text(filename):
    with open(os.path.join("tests", filename)) as f:
        text = f.read()
        return text

@pytest.fixture
def mock_request():
    m = requests_mock.mock()
    verb = "tener"

    urls = [ ("http://www.spanishdict.com/conjugate/{}".format(verb),
             "tenertest.html"),
             ("http://translate1.spanishdict.com/api/v1/verb?q=tener&source=es",
              "verb_english.json"),
             ("http://translate1.spanishdict.com/api/v1/verb?q=to%20have&source=en",
              "verb_english.json"),
             ]
    for url in urls:
        text = get_test_text(url[1])
        m.get(url[0], text=text)
    return m

def test_get_english_verb(mock_request):
    text = get_test_text("tenertest.html")
    assert scraper.get_english_verb(text) == "to have"

def test_conj(mock_request):
    result = scraper.get_conj("tener")
    assert test_data["tener"][0] in [x[0] for x in result]
