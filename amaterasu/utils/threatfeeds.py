import datetime
import pymongo
import utils.helpers as utils

def archive_threat_feeds():
    threat_feed_collections = ["binary_defense_artillery", "ci_army", "feodo_tracker_botnet_c2", "proofpoint_emerging_threats"]
    client = pymongo.MongoClient()
    for collection_name in threat_feed_collections:
        live_db = client["threat_feeds"]
        live_collection = live_db[collection_name]
        archive_db = client["archived_threat_feeds"]
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
    
    client.drop_database("threat_feeds")


def get_binary_defense_artillery_threat_feed():
    BINARY_DEFENSE_ARTILLERY_THREAT_FEED_URL = "https://www.binarydefense.com/banlist.txt"
    binary_defense_artillery_threat_feed = utils.get_threat_data(BINARY_DEFENSE_ARTILLERY_THREAT_FEED_URL)

    threat_feed = binary_defense_artillery_threat_feed.text.split("\n")[13:-1]

    for ip in threat_feed:
        utils.insert_atomic_ip("threat_feeds", "binary_defense_artillery", "ip", ip)

def get_ci_army_bad_ips_threat_feed():
    CI_ARMY_BAD_IPS_URL = "https://cinsscore.com/list/ci-badguys.txt"
    ci_army_bad_ips_threat_feed = utils.get_threat_data(CI_ARMY_BAD_IPS_URL)

    threat_feed = ci_army_bad_ips_threat_feed.text.split("\n")[:-1]

    for ip in threat_feed:
        utils.insert_atomic_ip("threat_feeds", "ci_army", "ip", ip)


def get_feodo_tracker_botnet_c2_ip_blocklist_threat_feed():
    FEODO_TRACKER_BOTNET_C2_IP_BLOCKLIST_URL = "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt"
    feodo_tracker_botnet_c2_ip_blocklist_threat_feed = utils.get_threat_data(FEODO_TRACKER_BOTNET_C2_IP_BLOCKLIST_URL)

    threat_feed = feodo_tracker_botnet_c2_ip_blocklist_threat_feed.text.split("\n")[9:-1]

    for ip in threat_feed:
        utils.insert_atomic_ip("threat_feeds", "feodo_tracker_botnet_c2", "ip", ip)


def get_proofpoint_emerging_threats_compromised_ips_threat_feed():
    PROOFPOINT_EMERGING_THREATS_COMPROMISED_IPS_URL = "https://rules.emergingthreats.net/blockrules/compromised-ips.txt"
    proofpoint_emerging_threats_compromised_ips_threat_feed = utils.get_threat_data(PROOFPOINT_EMERGING_THREATS_COMPROMISED_IPS_URL)

    threat_feed = proofpoint_emerging_threats_compromised_ips_threat_feed.text.split("\n")[:-1]

    for ip in threat_feed:
        utils.insert_atomic_ip("threat_feeds", "proofpoint_emerging_threats", "ip", ip)