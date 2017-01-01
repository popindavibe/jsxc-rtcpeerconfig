#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import time
import Crypto.Hash.SHA
from Crypto.Hash import HMAC
from base64 import b64encode

def sign_request(key, data):

    hmac = HMAC.new(key, data, Crypto.Hash.SHA)
    signature = b64encode(hmac.digest())
    return signature

def turn_request_handler(json_data):

    data = json.load(json_data)
    # 1 day
    tokenlife = 86400
    timestamp = int(time.time()) + tokenlife
    fullresult = dict()
    fullresult['ttl'] = tokenlife
    fullresult['iceServers'] = list()

    for key in data["servers"]:
        tempresult = dict()

        if 'username' in key and 'secret' in key: 
            user = str(timestamp) + ":" + key["username"]
            secret = sign_request(str(key["secret"]), str(user))
            tempresult['username'] = user
            tempresult['credential'] = secret

        # Fill the dictionnary
        tempresult['urls'] = key["urls"]

        # insère dans la liste
        fullresult['iceServers'].append(tempresult)


    # export the dict
    jsonExport = (json.dumps(fullresult))
    return jsonExport

# Exécuté seulement si le fichier du module est appelé directement
if __name__ == "__main__": 
    print "called directly"

## Pour appeler en direct
#json_file = 'turnConf.inc'
#json_data = open(json_file)
#result = turn_request_handler(json_data)
#json_data.close()
#print result

