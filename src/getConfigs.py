import yaml
import os

def getConfigs(path):
    print("Reading configs from " + path + "...")
    configs = {}
    with open(path, 'r') as stream:
        config = yaml.safe_load(stream)
        configs["recipients"] = config["cpaScraper"]["email"]["recipientList"]
    return configs

def getCreds(path):
    print("Reading creds from " + path + "...")
    creds = {}
    with open(path, 'r') as stream:
        cred = yaml.safe_load(stream)
        creds["senderAddress"] = cred["cpaScraper"]["creds"]["senderAddress"]
        creds["password"] = cred["cpaScraper"]["creds"]["password"]
    return creds