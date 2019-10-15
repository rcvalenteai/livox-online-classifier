from labels import MySQLDB
import uuid
import json
import labels.visionlabeler
import numpy
import math
import labels.threadedvision
import time

db = MySQLDB.init_db()


def json_db_connector(path, insert=True):
    """
    used to generate a 32-character UUID for an image-file and insert it into the database
    :param path: the local path of the image file
    :return: returns a tuple of the (image_id, path) (UUID, String)
    """
    image_id = str(uuid.uuid4())
    info = (image_id, path)
    if insert:
        stmt = "INSERT INTO Images(image_id, location) VALUES( %s, %s)"
        db.insert(stmt, info)
    return info


def get_full_url(path):
    """
    Converts local paths stored in the database are converted to full paths on from their host API's
    :param path: the local path of the image file
    :return: returns the full url path for the local image
    """
    api_path = "https://storage.googleapis.com/livox-images/full/"
    return api_path + path


def run_json(json_path):
    """
    runs the json formatted with the local paths on the google storage, sends to vision api and adds to database
    :param json_path: local path to json file
    :return:
    """
    count = 0
    with open(json_path, 'r', encoding='utf-8') as f:
        loaded_json = json.load(f)
    size = len(loaded_json["items"])
    print('loads json' + str(size))
    for items in loaded_json["items"]:
        count += 1
        path = items['file']
        #print('read json line')
        info = json_db_connector(path)
        full_path = get_full_url(path)
        #print('adds to database')
        id, annotations = labels.visionlabeler.label_image_online(full_path, info[0])
        #print('labels image')
        labels.visionlabeler.record_labels(id, annotations, db)
        db.conn.commit()
        #print('adds labels to database')
        print("Labeled " + str(count) + " of " + str(size) + " images")


def run_json_tags(json_path):
    """
    runs the json formatted with the local paths to get tag metadata
    :param json_path: local path to json file
    :return:
    """
    count = 0
    with open(json_path, 'r', encoding='utf-8') as f:
        loaded_json = json.load(f)
    size = len(loaded_json["items"])
    print('loads json' + str(size))
    infos = []
    size = len(loaded_json['items'])
    for items in loaded_json["items"]:
        count += 1
        tags = items['tags']
        path = items['file']
        id = ""
        stmt = "SELECT image_id FROM Images WHERE location = %s"
        cur = db.insert(stmt, (path,))
        results = list(cur.fetchall())
        for result in results:
            id = result[0]
        tags = tags.split()
        stmt = "INSERT INTO Tags(image_id, tag) VALUES (%s, %s)"
        for tag in tags:
            infos.append((id, tag))
            db.insert(stmt, (id, tag))
            db.conn.commit()
            if count % 500 == 1:
                print(infos)
        if (count % 500 == 0) or count == size:
            stmt = "INSERT INTO Tags(image_id, tag) VALUES (%s, %s)"
            #cur = db.insertmany(stmt, infos)
            #db.conn.commit()
            infos = []
            print("Labeled " + str(count) + " of " + str(size) + " images")


def run_json_batched(json_path, batch_size):
    """
    json ran halfway before timing out, this function will run only the remaining images, as
    well as running in batches
    :param json_path: the path to the json file
    :param batch_size: size of batch_size/ threading
    :return:
    """
    stmt = "SELECT location FROM Images"
    cur = db.query(stmt)
    results = list(cur.fetchall())
    with open(json_path, 'r', encoding='utf-8') as f:
        loaded_json = json.load(f)
    size = len(loaded_json["items"])
    print('JSON: ' + str(size))
    print('QUERY: ' + str(len(results)))
    json_items = loaded_json["items"]
    json_items = [item['file'] for item in json_items]
    results = [item[0] for item in results]
    db_query = set(results)
    json_paths = set(json_items)
    remaining = json_paths.difference(db_query)
    print('REMAINING: ' + str(len(remaining)))
    total = len(remaining)
    split = math.ceil(len(remaining) / batch_size)
    remaining = numpy.array_split(numpy.array(list(remaining)), split)

    count = 0
    for batch in remaining:
        size = len(batch)
        batch_thread_db(batch.tolist())
        count += size
        print("Labeled " + str(count) + " of " + str(total) + " Images")
        time.sleep(60)


def run_json_batched2(batch_size):
    """
    json ran halfway before timing out, this function will run only the remaining images, as
    well as running in batches
    :param json_path: the path to the json file
    :param batch_size: size of batch_size/ threading
    :return:
    """
    stmt = "SELECT image_id, location FROM Images WHERE image_id NOT IN (SELECT DISTINCT image_id FROM Labels)"
    cur = db.query(stmt)
    remaining = list(cur.fetchall())
    print('REMAINING: ' + str(len(remaining)))
    # stmt3 = "SELECT location FROM Images WHERE image_id = %s"
    # cur = db.insertmany(stmt3, remaining)
    # remaining = set(cur.fetchall())
    total = len(remaining)
    split = math.ceil(len(remaining) / batch_size)
    remaining = numpy.array_split(numpy.array(list(remaining)), split)

    count = 0
    batch_count = 1
    for batch in remaining:
        print("Starting Batch", (batch_count), "of", len(remaining))
        print("Google Image Labeling")
        size = len(batch)
        batch_thread_db(batch.tolist())
        count += size
        print("Labeled " + str(count) + " of " + str(total) + " Images")
        if batch_count != len(remaining):
            time.sleep(15)
        batch_count += 1


def batch_thread_db(paths):
    infos = paths
    # for path in paths:
    #     infos.append(json_db_connector(path, False))
    #stmt = "INSERT INTO Images(image_id, location) VALUES( %s, %s)"
    #db.insertmany(stmt, infos)
    lbls = labels.threadedvision.download_all_sites(infos)
    # split into individual threads
    # on google apis
    # collect label_image_online results -> record labels ->
    # send back list of tuples
    # combine into one
    stmt = "INSERT IGNORE INTO Labels(image_id, label, confidence) VALUES( %s, %s, %s)"
    db.insertmany(stmt, lbls)
    db.conn.commit()

def tester():
    keyword = 'pizza'
    stmt = "SELECT image_id FROM Tags WHERE tag = %s"
    cur = db.insert(stmt, (keyword,))
    rez = list(cur.fetchall())
    print(rez[0])



if __name__ == "__main__":
    # sites = [["https://storage.googleapis.com/livox-images/full/symbol00000997.png", "test"],
    #          ["https://storage.googleapis.com/livox-images/full/hot_dogs.png", 'yeet']] * 8
    # print(sites)
    start_time = time.time()
    run_json_batched2(400)
    #run_json_tags('image-paths.json')
    #tester()
    duration = time.time() - start_time
    print(f"Downloaded in {duration} seconds")


# add images from json to database
# load file paths to json, create threads for each image
# run_json('image-paths.json')
# print(get_full_url('dog_treats.png'))
# dont redo
# batch process json
# thread google interactions
# batch input google interactions
