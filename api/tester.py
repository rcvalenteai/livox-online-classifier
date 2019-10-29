import csv
from api.entityparser import offline_parse_phrase
from api.entityparser import model
from api.phraseparser import phrase_split
from api.imagedber import get_image


def load_csv(filename):
    loaded_csv = list()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            loaded_csv.append(row)
    return loaded_csv


class Test:

    def __init__(self, row):
        self.full_phrase = row[0]
        self.innvocation = row[1]
        self.list_phrase = row[2]
        self.entities = row[3].split("_")
        self.title = row[4]
        self.description = row[5]
        self.question_words = row[6]

    def report(self):
        resp = phrase_split(self.full_phrase)
        n = 3
        detected_entities = offline_parse_phrase(resp[1], n)
        result = all(elem in self.entities for elem in detected_entities)
        print(str(result).upper())
        print('Invocation:          ', resp[0])
        print('List:                ', resp[1])
        print('Entities:            ', self.entities)
        print('Detected Entities:   ', detected_entities)
        for entity in detected_entities:
            print(get_image(entity))
        return result


def test_cases():
    loaded_csv = load_csv('test-cases.csv')[1:]
    size = len(loaded_csv)
    count = 0
    count_corr = 0
    count_err = 0
    for row in loaded_csv:
        case = Test(row)
        print("**************************************************************")
        print(str(count+1) + ".", case.full_phrase)
        try:
            result = case.report()
            if result:
                count_corr += 1
        except Exception:
            print("ERROR")
            count_err += 1
        count += 1
    print('Correct:', count_corr, "of", size)
    print('Wrong  :', size - count_err - count_corr, "of", size)
    print('Errored:', count_err, "of", size)


test_cases()


