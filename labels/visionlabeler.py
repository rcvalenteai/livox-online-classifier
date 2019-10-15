import io
import os
from labels import MySQLDB
import requests
import io
#from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


# Assign client specific credientials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\rcval\\Desktop\\WPI\\livox\\livox-google-api-key.json"


# db = MySQLDB.init_db()

# Instantiates a client
client = vision.ImageAnnotatorClient()


# initiates the database connection

# interacts with Google's Vision API, to request labels for a single image
def label_image(file, id=None):
    file_name = os.path.abspath(file)
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return id, labels


def label_image_online(url):
    """
    takes the url of an image and sends it to google vision API to annotate
    :param url: url of image
    :param id: id of the image
    :return: id of image and the labels response of the image
    """
    response = requests.get(url)
    img = types.Image(content=response.content)
    vision_response = client.label_detection(image=img)
    labels = vision_response.label_annotations
    return labels


def label_image_online_batch(url, id=None):
    """
    takes the url of an image and sends it to google vision API to annotate
    :param url: url of image
    :param id: id of the image
    :return: id of image and the labels response of the image
    """
    response = requests.get(url)
    img = types.Image(content=response.content)
    vision_response = client.label_detection(image=img)
    labels = vision_response.label_annotations
    return (id, labels)


# interacts with Database to store image labels
def record_labels(id, labels, db, insert=True):
    infos = []
    for i in range(len(labels)):
        info = (id, labels[i].description, labels[i].score)
        infos.append(info)
        #print(str(info))
        if insert:
            stmt = "INSERT INTO Labels(image_id, label, confidence) VALUES( %s, %s, %s)"
            db.insert(stmt, info)
    return infos


# run an entire folder of images
def label_folder(folder):
    images = os.listdir(folder)
    size = len(images)
    count = 0
    for image in images:
        count += 1
        id, labels = label_image(folder + "/" + image, id=image)
        record_labels(id, labels)
        print("Labeled " + str(count) + " of " + str(size) + " images")


# label_folder("resources")