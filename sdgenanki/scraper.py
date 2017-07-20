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

hard_translations = {
        "presentSubjunctive" : { "english" : "It is good that 'he speak'" },
        "imperfectIndicative" : { "english" : "he used to speak" },
        "imperfectSubjunctive" : { "english" : "It made me happy that 'he spoke'" },
        "imperfectSubjunctive2" : { "english" : "It made me happy that 'he spoke'" },
        "futureSubjunctive" : { "english" : "it is possible 'he will speak'" },

        "presentPerfectSubjunctive" : { "english" : "I doubt 'he has spoken'" },
        "pastPerfectSubjunctive" : { "english" : "she did not believe 'he had spoken'" },
        "futurePerfectSubjunctive" : { "english" : "it is possible 'he will have spoken'" },

        "futurePerfectContinuous" : { "spanish" : "futurePerfect" },
        "pastPerfectContinuous" : { "spanish" : "preteritPerfect" },
        "presentPerfectContinuous" : { "spanish" : "presentPerfect" },

        "preteritPerfect" : { "english" : "pastPerfect" },
        "conditionalPerfect" : {"english" : "he 'would have spoken', but he was sick" },

        "conditionalIndicative" : { "english" : "he 'would speak'" },

        "pastContinuous" : { "spanish" : "preteritContinuous" },
        "preteritContinuous" : { "english" : "pastContinuous" },
        "conditionalContinuous" : { "english" : "you 'would be speaking' if you hadn't gotten sick" },
        "imperfectContinuous" : { "english" : "I have not clue what 'he was speaking' about"},

        "imperative" : { "english" : "speak!" },
        "negativeImperative" : { "english" : "don't speak!" },
        }
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
    forms = set([x for x in spanish_para] + [x for x in english_para])
    for form in forms:
        print(form)
        translations = []
        if not form in spanish_para or not spanish_para[form]:
            spanish_para[form] = len(subjects)  * [None]
        if not form in english_para or not english_para[form]:
            english_para[form] = len(subjects) * [None]
        for i, item in enumerate(zip(spanish_para[form], english_para[form])):
            s, e = item
            if not (s or e):
                #print("No spanish or english for %s:%s" % (form, subjects[i]))
                continue
            if not s:
                s = {}
                s['word'] = hard_translations[form]['spanish']
                if s['word'] in spanish_para[form]:
                    s['word'] = hard_translations[s['word']]['spanish']
            if not e:
                e = {}
                e['word'] = hard_translations[form]['english']
                if e['word'] in spanish_para[form]:
                    e['word'] = hard_translations[e['word']]['spanish']
            translations.append(
                    (("spanish" , s['word']),
                     ("english" , e['word']),
                     ("tense" , form),
                     ("subject" , subjects[i]),
                    ))
        words.append(translations)

    return words
