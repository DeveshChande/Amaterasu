import utils.helpers as utils
import utils.infrastructurefeeds as infrastructurefeeds
import utils.threatfeeds as threatfeeds
import time

def get_threat_feeds():
    threatfeeds.get_binary_defense_artillery_threat_feed()
    threatfeeds.get_ci_army_bad_ips_threat_feed()
    threatfeeds.get_feodo_tracker_botnet_c2_ip_blocklist_threat_feed()
    threatfeeds.get_proofpoint_emerging_threats_compromised_ips_threat_feed()


def get_infrastructure_feeds():
    infrastructurefeeds.get_tor_exit_nodes_infrastructure_feed()


def main():
    is_initial_run = utils.initialize_database()
    if is_initial_run == 0:
        get_threat_feeds()
        get_infrastructure_feeds()

        with open("initialize.txt", "w") as fd:
            fd.write("1")
            fd.close()
    else:
        threatfeeds.archive_threat_feeds()
        get_threat_feeds()
        infrastructurefeeds.archive_infrastructure_feeds()
        get_infrastructure_feeds()


if __name__ == "__main__":
    main()
