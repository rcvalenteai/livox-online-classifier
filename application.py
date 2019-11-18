from flask import Flask, request, render_template
from flask_restplus import Resource, Api, reqparse, fields
from flask_restplus import inputs
from flask_cors import CORS
from api.imagedber import get_image
from api.entityparser import parse_phrase
from api.entityparser import offline_parse_phrase
from api.entityparser import model
from api.phraseparser import phrase_split, question_classifier
import mysql.connector
from api.tester import threaded_test_cases
from api.tester import test_cases
import json
from api.logging import Logs, Entity

application = Flask(__name__)
application.config.SWAGGER_UI_DOC_EXPANSION = 'list'
api = Api(application, version='1.0', title='Livox Image API',
          description='API for image linking')
cors = CORS(application, resources={r"/*": {"origins":"*"}})

keywords = reqparse.RequestParser()
keywords.add_argument('keyword', type=str, required=True,
                      default='dog', help='keyword for image')

list_phrase = reqparse.RequestParser()
list_phrase.add_argument('phrase', type=str, required=True,
                         default='dog or cat', help='list phrase to pull entities from')
list_phrase.add_argument('ngram', type=int, required=False,
                         default=3, help='limit for ngrams to check for "hot dog" is a bi-gram; n=2')

full_phrase = reqparse.RequestParser()
full_phrase.add_argument('phrase', type=str, required=True,
                         default='what would you like for dinner pizza or pasta', help='full phrase to get image entities from')
full_phrase.add_argument('ngram', type=int, required=False,
                         default=3, help='limit for ngrams to check for "hot dog" is a bi-gram; n=2')
full_phrase.add_argument('local', type=inputs.boolean, required=False, default='false',
                         help='specify True to remove google cloud image retrieval prefix')


classifier_phrase = reqparse.RequestParser()
classifier_phrase.add_argument('phrase', type=str, required=True,
                         default='what would you like for dinner pizza or pasta', help='full phrase to get image entities from')

invocation_phrase = reqparse.RequestParser()
invocation_phrase.add_argument('phrase', type=str, required=True,
                               default='what would you like for dinner pizza or pasta', help='entire phrase to parse')


# toggler = reqparse.RequestParser()
# toggler.add_argument('toggle', type=bool, required=True,
#                      default=True, help='used to load word2vec into and out of memory for entity parsing')

#api.namespaces.clear()
api.namespaces[0].name = 'Livox API'
api.namespaces[0].description = 'API methods for Livox List Classifier'
#web = api.namespace(name='Analysis API', description='API methods for the AxonBeats website', path=None)


@api.route("/question_img_parser")
class QuestionImageParser(Resource):

    @api.expect(full_phrase)
    def get(self):
        """
        given a phrase return the links to the image urls
        """
        args = full_phrase.parse_args(request)
        n = args.get('ngram')
        phrase = args.get('phrase')
        local = args.get('local')
        resp = phrase_split(phrase)
        entities = offline_parse_phrase(resp[1], n)
        urls = list()
        log = Logs(phrase=phrase, is_list=question_classifier(phrase), question_phrase=resp[0], list_phrase=resp[1])
        for entity in entities:
            url = get_image(entity)
            print(local)
            if local:
                url = url.replace("https://storage.googleapis.com/livox-images/full/", "")
                url = url.replace(".png", "")
                #test
            log.entities.append(Entity(log.log_id, url, entity))
            # print(entity)
            # print(get_image(entity))
            urls.append({'entity': entity, 'url': url})
        print(log.entities)
        urls = json.dumps(urls)
        urls = json.loads(urls)
        log.add()
        return urls


@api.route("/image")
class ImageLink(Resource):

    @api.expect(keywords)
    def get(self):
        """
        get most closely related image

        :return: url of image
        """
        args = keywords.parse_args(request)
        keyword = args.get('keyword')
        resp = get_image(keyword)
        return resp


@api.route("/entities")
class EntityParser(Resource):

    @api.expect(list_phrase)
    def get(self):
        """
        get a list of entities from a phrase

        Parses the list portion of a sentence to determine entities (unigrams/bigrams)
        """
        args = list_phrase.parse_args(request)
        phrase = args.get('phrase')
        n = args.get('ngram')
        resp = offline_parse_phrase(phrase, n)
        return resp


@api.route("/offline_entities")
class OfflineEntityParser(Resource):

    @api.expect(list_phrase)
    def get(self):
        """
        get a list of entities from a phrase using offline model

        Parses the list portion of a sentence to determine entities (unigrams/bigrams)
        """
        args = list_phrase.parse_args(request)
        phrase = args.get('phrase')
        n = args.get('ngram')
        resp = offline_parse_phrase(phrase, n)
        return resp


@api.route("/phrase_splitter")
class PhraseSplitter(Resource):

    @api.expect(invocation_phrase)
    def get(self):
        """
        seperate the list phrases into invocation phrase and list phrase

        Parses the phrase to find where to seperate between invocation and list
        """
        args = invocation_phrase.parse_args(request)
        phrase = args.get('phrase')
        resp = phrase_split(phrase)
        resp = json.dumps({'innvocation': resp[0], 'list': resp[1]})
        resp = json.loads(resp)
        return resp


@api.route("/listclassifier")
class ListQuestionClassifier(Resource):

    @api.expect(classifier_phrase)
    def get(self):
        """
        classify if phrase is a list question

        returns true or false if phrase is a list question
        """
        args = classifier_phrase.parse_args(request)
        phrase = args.get('phrase')
        return question_classifier(phrase)


@api.route("/test")
class Benchmark(Resource):

    def get(self):
        """
        using the test cases derived from the google sheet, get performance report, this may take a few minutes
        """
        return threaded_test_cases()


if __name__ == '__main__':
    application.run()
