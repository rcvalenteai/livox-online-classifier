from flask import Flask, request, render_template
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS
from api.imagedber import get_image
from api.entityparser import parse_phrase
from api.entityparser import offline_parse_phrase
from api.entityparser import model
from api.phraseparser import phrase_split
import mysql.connector

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
                         default=2, help='limit for ngrams to check for "hot dog" is a bi-gram; n=2')

invocation_phrase = reqparse.RequestParser()
invocation_phrase.add_argument('phrase', type=str, required=True,
                               default='what would you like for dinner dog or cat', help='entire phrase to parse')

toggler = reqparse.RequestParser()
toggler.add_argument('toggle', type=bool, required=True,
                     default=True, help='used to load word2vec into and out of memory for entity parsing')

#api.namespaces.clear()
api.namespaces[0].name = 'Livox API'
api.namespaces[0].description = 'API methods for Livox List Classifier'
#web = api.namespace(name='Analysis API', description='API methods for the AxonBeats website', path=None)


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
        resp = parse_phrase(phrase, n)
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
        return resp


@api.route("/question_img_parser")
class QuestionImageParser(Resource):

    @api.expect(invocation_phrase)
    def get(self):
        """
        given a phrase return the links to the image urls
        """
        args = invocation_phrase.parse_args(request)
        phrase = args.get('phrase')
        resp = phrase_split(phrase)
        entities = offline_parse_phrase(resp[1], 2)
        urls = list()
        for entity in entities:
            print(entity)
            print(get_image(entity))
            urls.append(get_image(entity))
        return urls


@api.route("/toggle")
class ToggleWordEmbedding(Resource):

    @api.expect(toggler)
    def get(self):
        """
        toggle word2vec into and out of memory

        Word2Vec takes up 3.5 GB of memory, used for resource management on AWS
        """
        args = toggler.parse_args(request)
        toggle = args.get('toggle')
        resp = model.toggle_word_embedding(toggle)
        return resp


if __name__ == '__main__':
    application.run()
