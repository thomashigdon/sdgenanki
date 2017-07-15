import ssgenanki.scraper as scraper

test_data = \
{
    "tener" :
    {
        "present" :
        {
            "yo" : "tengo"
        }
    }
}

def test_conj():
   assert (scraper.get_conj("tener") ==
           test_data["tener"])
