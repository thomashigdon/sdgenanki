import os
import pytest
import requests_mock

def get_test_text(filename):
    with open(os.path.join("tests", filename)) as f:
        text = f.read()
        return text

@pytest.fixture
def mock_request():
    m = requests_mock.mock()
    verb = "tener"
    api_root = "http://translate1.spanishdict.com/api/v1/verb"
    urls = [ ("http://www.spanishdict.com/conjugate/{}".format(verb),
             "tenertest.html"),
             (api_root + "?q=tener&source=es",
              "verb_spanish.json"),
             (api_root + "?q=to%20have&source=en",
              "verb_english.json"),
             ]
    for url in urls:
        text = get_test_text(url[1])
        m.get(url[0], text=text)
    return m

