import yaml
import os

def getConfigs(path):
    print("Reading configs from " + path + "...")
    configs = {}
    with open(path, 'r') as stream:
        config = yaml.safe_load(stream)
        configs["senderAddress"] = config["cpaScraper"]["email"]["senderAddress"]
        configs["password"] = config["cpaScraper"]["email"]["password"]
        configs["recipients"] = config["cpaScraper"]["email"]["recipientList"]
    return configs

