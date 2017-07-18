import requests
import re
import json

SD_ROOT = "http://www.spanishdict.com/"
SD_API_ROOT = "http://translate1.spanishdict.com/api/v1/verb"

def get_english_verb(text):
    match = re.search(r"window.SD_QUICKDEF\s+=\s*'(.*)'", text)
    if match:
        return match.group(1)
    raise Exception("blah")

def get_conj_data(verb, lang):
    url = SD_API_ROOT + "?q=%s&source=%s" % (verb, lang)
    result = requests.get(url)
    result = json.loads(result.text)
    return result

def get_conj(spanish_verb):
    subjects = ("yo", "tú", "él/ella", "nosotros", "vosotros", "ellos")
    url = SD_ROOT + "conjugate/" + spanish_verb
    r = requests.get(url)
    r.raise_for_status()
    page = r.text
    english_verb = get_english_verb(page)
    spanish_conj = get_conj_data(spanish_verb, "es")
    english_conj = get_conj_data(english_verb, "en")
    words = []
    spanish_para = spanish_conj['data']['paradigms']
    english_para = english_conj['data']['paradigms']
    for form, vals in english_para.items():
        if not vals or not spanish_para[form]: continue
        translations = []
        for s, e in zip(spanish_para[form], vals):
            if not (s and e): continue
            translations.append(
                    (("spanish" , s['word']),
                     ("english" , e['word']),
                     ("tense" , form),
                    # ("subject" , "yo"),
                    ))
        words.append(translations)


    return words
