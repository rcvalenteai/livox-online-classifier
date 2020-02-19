def clean_question_words(filename, output_filename):
    raw_responses = online_api.helpers.io.load_csv(filename)
    new_responses = list()
    for row in raw_responses:
        words = row[0].split()
        first_word = words[0]
        cleaned_word = clean_word(first_word)
        words[0] = cleaned_word
        question = " ".join(words)
        new_responses.append([question, row[1], row[2]])
    online_api.helpers.io.write_list_csv("cleaned", output_filename, new_responses)


def clean_word(first_word):
    first_word = first_word.replace("'s", "")
    first_word = first_word.replace("’s", "")
    first_word = first_word.replace("n't", "")
    if first_word == "whom":
        first_word = "who"
    return first_word


clean_question_words("./cleaned/mturk.csv", "mturk-clean.csv")
