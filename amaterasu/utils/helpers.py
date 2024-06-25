import datetime
import pymongo
import random
import pymongo.errors
import requests


def get_threat_data(THREAT_FEED_URL: str) -> requests.Response:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'
    ]

    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    return requests.get(THREAT_FEED_URL, headers=headers)

def initialize_database() -> int:
    check_run = 0
    with open("initialize.txt", "r") as fd:
        check_run = int(fd.readlines()[0])
        fd.close()
    
    if check_run == 0:
        return 0
    
    return 1

def insert_atomic_ip(db_name, collection_name, key_name, value):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one({key_name: value, "last_seen": datetime.datetime.now(tz=datetime.timezone.utc)})