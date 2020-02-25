from online_api.api.question_phrase_parser import question_parser
from online_api.api.entity_phrase_parser.EntityPhrase import parse
from online_api.api import imagedber
from online_api.helpers import load_csv
import json
import evaluation.plots as plotter
import evaluation.plots as cl


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
        return parse(self.list_phrase, ngram_threshold)

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
        entity_report['ngram_perf'] = self.n_gram_performance(found_entities)
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
        conditions['found_percent'] = self.found_percent_entities(found_entities)
        return conditions

    def found_percent_entities(self, found_entities):
        results = dict()
        for correct in self.entities:
            results[correct] = found_entities.count(correct)
        try:
            percent_found = (float(sum(results.values())) / float(len(results)))
        except ZeroDivisionError:
            percent_found = 0
        return percent_found

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
        return 0 < percent_found <= .5

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
        return all(correct in found_entities for correct in self.entities)

    def correct_entities(self, found_entities):
        return all(found in self.entities for found in found_entities) and \
               all(correct in found_entities for correct in self.entities)

    def n_gram_performance(self, found_entities):
        ngram_perf = dict()
        for entity in self.entities:
            size = len(entity.split(" "))
            ngram_perf.setdefault(size, dict())
            ngram_perf[size].setdefault("count", 0)
            ngram_perf[size]['count'] += 1
            if any(found in [entity] for found in found_entities):
                ngram_perf[size].setdefault("correct", 0)
                ngram_perf[size]['correct'] += 1
        return ngram_perf


def test_all_examples(filename):
    examples = load_csv(filename)
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
    summary['found_percent'] = 0
    summary['categories'] = dict()
    summary['ngrams'] = dict()
    summary['ngrams_category'] = dict()
    for example in examples:
        question = TestQuestion.from_db(example)
        result = question.parsers_eval(ngram_threshold=4)
        results.append(result)
        # print(result)
        for ngram_size, ngram_dict in result['entity_classification']['ngram_perf'].items():
            summary['ngrams'].setdefault(ngram_size, dict())
            for key, value in ngram_dict.items():
                summary['ngrams'][ngram_size].setdefault(key, 0)
                summary['ngrams'][ngram_size][key] += value

        for ngram_size, ngram_dict in result['entity_classification']['ngram_perf'].items():
            summary['ngrams_category'].setdefault(ngram_size, dict())
            summary['ngrams_category'][ngram_size].setdefault(result['category'], dict())
            for key, value in ngram_dict.items():
                summary['ngrams_category'][ngram_size][result['category']].setdefault(key, 0)
                summary['ngrams_category'][ngram_size][result['category']][key] += value
        summary['categories'].setdefault(result['category'], dict())
        summary['categories'][result['category']].setdefault('count', 0)
        summary['categories'][result['category']]['count'] += 1
        if result['question_classification']:
            summary['recognized'] += 1
            summary['categories'][result['category']].setdefault('recognized', 0)
            summary['categories'][result['category']]['recognized'] += 1
        for key, value in result['entity_classification']['results'].items():
            if value:
                summary[key] += 1
                summary['categories'][result['category']].setdefault(key, 0)
                summary['categories'][result['category']][key] += 1
    print(summary)
    temp_ngrams = dict()
    for ngram_size, ngram_dict in summary['ngrams'].items():
        temp_ngrams[ngram_size] = ngram_dict.get("correct", 0) / ngram_dict['count']
    plotter.plot_horizontal_dictionary_counter(temp_ngrams, "Ngram Detection Performance")

    temp_ngrams_categories = dict()
    for ngram_size, ngram_categories in summary['ngrams_category'].items():
        temp_ngrams_categories.setdefault(ngram_size, dict())
        for category, ngram_dict in summary['ngrams_category'][ngram_size].items():
            temp_ngrams_categories[ngram_size][category] = ngram_dict.get("correct", 0) / ngram_dict['count']

    for key, ngram_dict in temp_ngrams_categories.items():
        plotter.plot_horizontal_dictionary_counter(ngram_dict, str(key) + "-gram performance by category")
    print(temp_ngrams_categories)

    print(summary['ngrams'])
    # print(results)
    json_form = json.dumps(results)
    json_form = json.loads(json_form)
    correct = list()
    found_all = list()
    reference = dict()
    categorical = dict()
    categorical_found_all = dict()
    grouped_vals = dict()
    for category, results2 in summary['categories'].items():
        for result in results2.keys():
            categorical.setdefault(result, dict())
            categorical[result].setdefault(category, 0)
            categorical[result][category] = results2[result] / results2['count']
    for key, value in categorical.items():
        plotter.plot_horizontal_dictionary_counter(value, str(key) + " across Entity types")
        if key in ["extra", "none", "minority", "correct", "majority"]:
            grouped_vals.setdefault(key, dict())
            for category, percent in value.items():
                grouped_vals[key][category] = percent
        # categorical[category] = results['correct'] / results['count']
        # categorical_found_all[category] = results['found_all'] / results['count']
    print(grouped_vals)
    plotter.plot_clustered_bar(grouped_vals, "Clustered Performance")
    for result in results:
        # print(result)
        if result['entity_classification']['results']['correct']:
            # print(result['phrase'])
            # print(result['entities'])
            correct.append(result['phrase'])
        if result['entity_classification']['results']['found_all']:
            found_all.append(result['phrase'])
        reference[result['phrase']] = [result['entities'], result['entity_classification']['found']]

    with open("results-testing.json", "w") as estimate_report_file:
        json.dump(json_form, estimate_report_file, indent=4, sort_keys=True)


test_all_examples("./mturk.csv")
