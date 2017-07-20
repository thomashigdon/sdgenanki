from context import sdgenanki
import sdgenanki.scraper as scraper

import os
import pytest
import conftest

test_data = \
{
    "tener" :
    [
        (("spanish" , "tengo"),
         ("english" , "I have"),
         ("tense" , "presentIndicative"),
         ("subject" , "yo"),
        ),
    ]
}

def test_get_english_verb(mock_request):
    with mock_request:
        text = conftest.get_test_text("tenertest.html")
        assert scraper.get_english_verb(text) == "to have"

def test_conj(mock_request):
    with mock_request:
        result = scraper.get_conj("tener")
        assert test_data["tener"][0] in [x[0] for x in result]
