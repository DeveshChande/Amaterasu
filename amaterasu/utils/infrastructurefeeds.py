import datetime
import pymongo
import utils.helpers

def get_tor_exit_nodes_infrastructure_feed():
    TOR_EXIT_NODES_URL = "https://check.torproject.org/torbulkexitlist"
    tor_exit_nodes_feed = utils.helpers.get_threat_data(TOR_EXIT_NODES_URL)

    threat_feed = tor_exit_nodes_feed.text.split("\n")[:-1]
    for ip in threat_feed:
        utils.helpers.insert_atomic_ip("infrastructure_feeds", "tor_exit_nodes", "ip", ip)

def archive_infrastructure_feeds():
    infrastructure_feed_collections = ["tor_exit_nodes"]
    client = pymongo.MongoClient()
    for collection_name in infrastructure_feed_collections:
        live_db = client["infrastructure_feeds"]
        live_collection = live_db[collection_name]
        archive_db = client["archived_infrastructure_feeds"]
        archive_collection = archive_db["archive_" + collection_name]

        try:
            documents = live_collection.find()
            for doc in documents:
                archived_doc = archive_collection.find_one({"ip": doc["ip"]})
                if archived_doc:
                    archive_collection.find_one_and_update({"ip": doc["ip"]}, {'$set': {"last_seen": datetime.datetime.now(tz=datetime.timezone.utc)}}, return_document=pymongo.ReturnDocument.AFTER)
                else:
                    archive_collection.insert_one(doc)

            print(f"Successfully archived the {collection_name} collection.\n")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    client.drop_database("infrastructure_feeds")