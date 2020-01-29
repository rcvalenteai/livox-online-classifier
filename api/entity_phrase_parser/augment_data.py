import api.entity_phrase_parser.vocab_generator as vocab_gen
import helpers.io


def augment_celeb_vocabulary(augment_file, filename='./resources/vocabulary.json', ):
    vocabulary = vocab_gen.load_ngram_dict(filename)
    celebs = helpers.io.load_csv(augment_file)[1:]
    for celeb in celebs:
        cleaned = celeb[1].replace("_", " ").lower()
        cleaned = cleaned.split("(")[0]
        cleaned = cleaned.strip()
        vocabulary[cleaned] = 0
    vocab_gen.save_dict_as_json(vocabulary, filename)
    return vocabulary


def augment_cities_vocabulary(augment_file, filename='./resources/vocabulary.json'):
    vocabulary = vocab_gen.load_ngram_dict(filename)
    cities = helpers.io.load_csv(augment_file)[1:]
    for city in cities:
        cleaned_city = city[0].lower()
        cleaned_country = city[1].lower()
        cleaned_state = city[2].lower()
        vocabulary[cleaned_city] = 0
        vocabulary[cleaned_country] = 0
        vocabulary[cleaned_state] = 0
    vocab_gen.save_dict_as_json(vocabulary, filename)


def augment_organizations_vocabulary(augment_file, filename="./resources/vocabulary.json"):
    vocabulary = vocab_gen.load_ngram_dict(filename)
    companies = helpers.io.load_csv(augment_file)[1:]
    for company in companies:
        cleaned = company[2].lower()
        vocabulary[cleaned] = 0
    vocab_gen.save_dict_as_json(vocabulary, filename)


def augment_embedding_vocabulary(augment_file, filename="./resources/vocabulary.json"):
    vocabulary = vocab_gen.load_ngram_dict(filename)
    word_embed = vocab_gen.load_ngram_dict(filename)
    for word in word_embed.keys():
        vocabulary[word] = 0
    vocab_gen.save_dict_as_json(vocabulary, filename)


augment_celeb_vocabulary("./resources/data-augment/male-21st.csv")
augment_celeb_vocabulary("./resources/data-augment/female-21st.csv")
augment_cities_vocabulary("./resources/data-augment/world-cities.csv")
augment_organizations_vocabulary("./resources/data-augment/forbes-2000.csv")
augment_embedding_vocabulary("./resources/data-augment/word_embedding_augment.json")
