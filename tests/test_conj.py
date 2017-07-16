from context import sdgenanki
import sdgenanki.scraper as scraper
import requests_mock

test_data = \
{
    "tener" :
    {
        "presentIndicative" :
        {
            "yo" : "tengo"
        }
    }
}

def test_conj():
    with requests_mock.mock() as m:
        verb = "tener"
        url = "http://www.spanishdict.com/conjugate/{}".format(verb)
        with open("tests/tenertest.html") as f:
            text = f.read()
        m.get(url, text=text)
        result = scraper.get_conj(verb)
        yo = result["presentIndicative"]["yo"]
        assert yo == test_data["tener"]["presentIndicative"]["yo"]
