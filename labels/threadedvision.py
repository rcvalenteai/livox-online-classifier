from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import threading
import labels.visionlabeler
import time
import random
import labels.imageconnector as imgc


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def return_after_5_secs(num):
    time.sleep(random.randint(1, 5))
    return "Return of {}".format(num)


def download_all_sites(urls):
    futures = []
    labeled = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for url in urls:
            futures.append(executor.submit(labels.visionlabeler.label_image_online_batch, imgc.get_full_url(url[1]), url[0]))

        for x in as_completed(futures):
            label = labels.visionlabeler.record_labels(x.result()[0], x.result()[1], None, False)
            for lab in label:
                labeled.append(lab)
    return labeled