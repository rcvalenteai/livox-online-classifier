import json


def create_yes_no_argus_csv(filename="./data/argus_yes_no_train.csv"):
    argus = online_api.helpers.io.load_csv(filename)[1:]
    yes_nos = dict()
    final_yes_nos = list()
    for example in argus:
        cleaned = example[0].replace(" ' ", "").replace(" ?", "").lower()
        yes_nos[cleaned] = 1
    for question, value in yes_nos.items():
        row = [question, [], "", 0]
        final_yes_nos.append(row)
    online_api.helpers.io.write_list_csv("cleaned", "argus.csv", final_yes_nos[:500])


def create_boolq_yes_no_csv(filename="./data/boolq_yes_no.jsonl"):
    result = list()
    with open(filename, "r", encoding='utf-8') as file:
        print(file)
        for line in file:
            result.append(json.loads(line)['question'])
    final_results = list()
    for res in result:
        row = [res, [], "", 0]
        final_results.append(row)
    online_api.helpers.io.write_list_csv("cleaned", "boolq.csv", final_results[:500])


create_boolq_yes_no_csv()
