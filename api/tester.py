import csv
from api.entityparser import offline_parse_phrase
from api.entityparser import model
from api.phraseparser import phrase_split
from api.imagedber import get_image
from api.imagedber import get_image_test
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


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
        response = dict()
        resp = phrase_split(self.full_phrase)
        n = 3
        detected_entities = offline_parse_phrase(resp[1], n)
        result = all(elem in detected_entities for elem in self.entities)
        print(str(result).upper())
        response['invocation'] = resp[0]
        response['list'] = resp[1]
        response['entities'] = self.entities
        response['detect entities'] = detected_entities
        print('Invocation:          ', resp[0])
        print('List:                ', resp[1])
        print('Entities:            ', self.entities)
        print('Detected Entities:   ', detected_entities)
        imgs = []
        db = None
        for entity in detected_entities:
            temp = get_image_test(entity, db)
            imgs.append(temp[0])
            db = temp[1]
            print(temp[0])
        response['images'] = imgs
        response['result'] = result
        return response

def threaded_helper(row):
    case = Test(row)
    rep_dict = dict()
    rep_dict['phrase'] = case.full_phrase
    try:
        text = case.report()
        rep_dict['report'] = text
        # rep_dict['report']['result'] = True
    except Exception as e:
        print(case.full_phrase, e)
        rep_dict['error'] = True
        rep_dict['report'] = dict()
        rep_dict['report']['result'] = False
    return rep_dict


def threaded_test_cases():

    futures = []
    labeled = []
    urls = load_csv('./resources/test-cases.csv')[1:]
    with ThreadPoolExecutor(max_workers=8) as executor:
        for url in urls:
            futures.append(
                executor.submit(threaded_helper, url))

        list_report = list()
        count_corr = 0
        count_wrong = 0
        count_err = 0
        for x in as_completed(futures):
            list_report.append(x.result())
            try:
                if x.result()['report']['result']:
                    count_corr += 1
                else:
                    count_wrong += 1
            except Exception as e:
                print(e)
                count_err += 1
        final_report = dict()
        final_report['cases'] = list_report
        final_report['summary'] = dict()

        final_report['summary']['correct'] = count_corr
        final_report['summary']['wrong'] = count_wrong
        final_report['summary']['err'] = count_err
        final_report = json.dumps(final_report)
        final_report = json.loads(final_report)
        return final_report





def test_cases():
    report = ""
    report_list = []
    loaded_csv = load_csv('./resources/test-cases.csv')[1:]
    size = len(loaded_csv)
    count = 0
    count_corr = 0
    count_err = 0

    for row in loaded_csv:
        case = Test(row)
        report += ("**************************************************************\n")
        print("**************************************************************")
        rep_dict = dict()
        rep_dict['phrase'] = case.full_phrase
        report += (str(count+1) + ". " + case.full_phrase + "\n")
        print(str(count+1) + ".", case.full_phrase)
        try:
            result, text = case.report()
            rep_dict['report'] = text
            if result:
                count_corr += 1
        except Exception:
            report += ("ERROR\n")
            rep_dict['error'] = True
            rep_dict['report']['result'] = False
            print("ERROR")
            count_err += 1
        count += 1
        report_list.append(rep_dict)
    final_report = dict()
    final_report['cases'] = report_list
    final_report['summary'] = dict()

    final_report['summary']['correct'] = count_corr
    final_report['summary']['wrong'] = size - count_err - count_corr
    final_report['summary']['error'] = count_err
    report += 'Correct: ' + str(count_corr) + " of " + str(size) + "\n"
    print('Correct:', count_corr, "of", size)
    report += 'Wrong  : ' + str(size - count_err - count_corr) + " of " + str(size) + "\n"
    print('Wrong  :', size - count_err - count_corr, "of", size)
    report += 'Errored: ' + str(count_err) + " of " + str(size) + "\n"
    print('Errored:', count_err, "of", size)
    final_report = json.dumps(final_report)
    final_report = json.loads(final_report)
    return final_report


# test_cases()
# threaded_test_cases()