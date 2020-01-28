import helpers.io
import numpy as np


def reformat_two_column(filename):
    raw_responses = helpers.io.load_csv(filename)[1:]
    questions = np.ravel([response[2::3] for response in raw_responses])
    solutions = np.ravel([response[3::3] for response in raw_responses])
    categories = np.ravel([response[4::3] for response in raw_responses])
    return np.asarray(list(zip(questions, solutions, categories)))


def remove_characters(phrases, banned_characters):
    questions = ["".join(filter(lambda i: i not in banned_characters, phrase)) for phrase in phrases]
    return questions


def remove_words(phrases, banned_phrases):
    new_phrases = list()
    for phrase in phrases:
        new_phrase = list()
        words = phrase.split()
        for word in words:
            if word not in banned_phrases:
                new_phrase.append(word)
        new_phrases.append(" ".join(new_phrase))
    return new_phrases


def clean_solution_whitespace(solutions):
    solutions = [solution.strip() for solution in solutions]
    list_of_entities = [solution.split(",") for solution in solutions]
    list_of_entities = [[entity.strip() for entity in entities] for entities in list_of_entities]
    cleaned_solutions = [",".join(entities) for entities in list_of_entities]
    return cleaned_solutions


def preprocess_questions(questions):
    questions = [question.strip().lower() for question in questions]
    removed_characters = ['?', ',']
    questions = ["".join(filter(lambda i: i not in removed_characters, question)) for question in questions]
    return questions


def preprocess_solutions(solutions):
    solutions = [solution.lower() for solution in solutions]
    removed_phrases = ['a', 'an', 'the']
    solutions = remove_words(solutions, removed_phrases)
    solutions = clean_solution_whitespace(solutions)
    return solutions


def preprocess_categories(categories):
    categories = [category.lower() for category in categories]
    return categories


def clean_format_raw_mturk(filename, output_filename=None):
    reformatted = reformat_two_column(filename)
    questions = preprocess_questions(reformatted[:,0])
    solutions = preprocess_solutions(reformatted[:,1])
    categories = preprocess_categories(reformatted[:,2])
    cleaned = list(zip(questions, solutions, categories))
    if output_filename is not None:
        helpers.io.write_list_csv('cleaned', output_filename, cleaned)
    return cleaned


def load_n_batches(batches, output_filename=None):
    cleaned_batches = list()
    for batch in range(batches):
        cleaned_batch = clean_format_raw_mturk("./data/mturk-r" + str(batch+1) + ".csv")
        cleaned_batches = cleaned_batches + cleaned_batch
    if output_filename is not None:
        helpers.io.write_list_csv('cleaned', output_filename, cleaned_batches)
    return cleaned_batches


clean_format_raw_mturk('./data/mturk-r5.csv', 'mturk-r5.csv')
#load_n_batches(2, 'mturk-r4.csv')

# clean_format_raw_mturk("./data/mturk-r1.csv", 'mturk.csv')


