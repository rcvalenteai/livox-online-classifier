from api.question_phrase_parser import question_parser
from api.entity_phrase_parser import EntityPhrase
from api import imagedber
import helpers.io
import json


class TestQuestion(object):

    def __init__(self, question, entities, category, question_type):
        self.question = question
        self.entities = entities
        self.category = category
        self.question_type = question_type
        self.invocation_phrase = question_parser.phrase_split(question)[0]
        self.list_phrase = question_parser.phrase_split(question)[1]

    @classmethod
    def from_db(cls, csv_line):
        question = csv_line[0]
        entities = csv_line[1].split(",")
        category = csv_line[2]
        question_type = 1
        return cls(question, entities, category, question_type)

    def is_list_question(self):
        return question_parser.question_classifier(self.question)

    def get_entities(self, ngram_threshold=2):
        return EntityPhrase.parse(self.list_phrase, ngram_threshold)

    def get_images(self, entities=None, db=None):
        if entities is None:
            entities = self.get_entities(ngram_threshold=2)
        images = list()
        for entity in entities:
            image = dict()
            image[entity] = imagedber.get_image(entity, db)
            images.append(image)
        return images

    def eval_list_question_classification(self):
        return self.is_list_question() == self.question_type

    def eval_entities(self, ngram_threshold=2):
        found_entities = self.get_entities(ngram_threshold)
        entity_report = dict()
        entity_report['answer'] = self.entities
        entity_report['found'] = found_entities
        entity_report['results'] = self.eval_entity_conditions(found_entities)
        return entity_report

    def parsers_eval(self, ngram_threshold, get_images=False):
        parse_report = dict()
        parse_report['phrase'] = self.question
        parse_report['entities'] = self.entities
        parse_report['category'] = self.category
        parse_report['is_question'] = self.question_type
        parse_report['question_classification'] = self.eval_list_question_classification()
        parse_report['entity_classification'] = self.eval_entities(ngram_threshold)
        if get_images:
            parse_report['images'] = self.get_images()
        return parse_report

    def eval_entity_conditions(self, found_entities):
        conditions = dict()
        conditions['correct'] = self.correct_entities(found_entities)
        conditions['extra'] = self.extra_entities(found_entities)
        conditions['none'] = self.no_entities(found_entities)
        conditions['minority'] = self.minority_entities(found_entities)
        conditions['majority'] = self.majority_entities(found_entities)
        conditions['found_all'] = self.found_all_entities(found_entities)
        conditions['found_all_fuzzy'] = self.found_all_fuzzy_match(found_entities)
        return conditions

    def majority_entities(self, found_entities):
        results = dict()
        for correct in self.entities:
            results[correct] = found_entities.count(correct)
        try:
            percent_found = (float(sum(results.values())) / float(len(results)))
        except ZeroDivisionError:
            percent_found = 0
        return 1 > percent_found > .5

    def minority_entities(self, found_entities):
        results = dict()
        for correct in self.entities:
            results[correct] = found_entities.count(correct)
        try:
            percent_found = (float(sum(results.values())) / float(len(results)))
        except ZeroDivisionError:
            percent_found = 0
        return percent_found <= .5

    def found_all_fuzzy_match(self, found_entities):
        fuzzy_found = True
        for entity in self.entities:
            words = entity.split(" ")
            local_fuzzy_found = False
            if any(found in words for found in found_entities) or any(found in [entity] for found in found_entities):
                local_fuzzy_found = True
            fuzzy_found = local_fuzzy_found
        return fuzzy_found

    def no_entities(self, found_entities):
        return not any(found in self.entities for found in found_entities)

    def extra_entities(self, found_entities):
        return any(found not in self.entities for found in found_entities)

    def found_all_entities(self, found_entities):
        return all(found in self.entities for found in found_entities)

    def correct_entities(self, found_entities):
        return all(found in self.entities for found in found_entities) and \
               all(correct in found_entities for correct in self.entities)


def test_all_examples(filename):
    examples = helpers.io.load_csv(filename)[1:]
    results = list()
    summary = dict()
    summary['examples'] = len(examples)
    summary['recognized'] = 0
    summary['correct'] = 0
    summary['extra'] = 0
    summary['none'] = 0
    summary['minority'] = 0
    summary['majority'] = 0
    summary['found_all'] = 0
    summary['found_all_fuzzy'] = 0
    for example in examples:
        question = TestQuestion.from_db(example)
        result = question.parsers_eval(ngram_threshold=4)
        results.append(result)
        if result['question_classification']:
            summary['recognized'] += 1
        for key, value in result['entity_classification']['results'].items():
            if value:
                summary[key] += 1
    print(summary)
    print(results)
    json_form = json.dumps(results)
    json_form = json.loads(json_form)
    with open("results-testing.json", "w") as estimate_report_file:
        json.dump(json_form, estimate_report_file, indent=4, sort_keys=True)
                

test_all_examples("./mturk.csv")
