from flask import Flask, request, render_template
from flask_restplus import Resource, Api, reqparse, fields
from flask_cors import CORS
from api.imagedber import get_image
from api.entityparser import parse_phrase
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


if __name__ == '__main__':
    application.run()
