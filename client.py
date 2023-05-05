import json
import time
from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, NistKey, DistVerify, utils, User
from jwcrypto import jwk, jws


compression_algo = 'bzip2'

class Client(Node):

    def __init__(self, host, port, threshold, total, id=None, callback=None, max_connections=4):
        super(Client, self).__init__(host, port, id, callback, max_connections)
        self.db = {}
        self.result = {}
        self.key = None
        self.token = None
        self.token_key = None
        self.server_set = None
        self.neighbours = None
        self.threshold = threshold
        self.total = total
        self.start_time = None
        self.end_local_comp_time = None
        self.end_time = None

        self.fetch_keys()


    def node_message(self, connected_node, message):

        #print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'auth-response'):
                self.received_result(connected_node, message)


    def fetch_keys(self):
        '''This function is called as part of the init
        for user node. read key files and create the key
        objects'''
        with open("token_key.txt", "r") as file:
            key_dict = file.read()
            self.token_key = jwk.JWK.from_json(key_dict)

        with open("ver_keys_for_user.txt") as file:
            ver_key = NistKey.Key()
            key_dict = file.read()
            ver_key.from_json(json.loads(key_dict))
            self.key = ver_key

    def initiate_auth(self):
        self.token = User.make_token(self.key, self.token_key, 'JohnDoe', 'P@ssword!')

        self.server_set = ['1', '2']
        
        nonce = utils.rand_felement_b64str(self.key)

        #print("CREATED NONCE {} and type {}".format(nonce, type(nonce)))
        self.db[nonce] = []
        self.result[nonce] = {}
        message = {'_type': 'auth-init', 'ssid': nonce, 'server_set': self.server_set}

        #start user timing
        self.start_time = time.perf_counter()
        self.send_to_nodes(message, compression=compression_algo)
        

    def received_broadcast_nonce(self, node, data):
        idx = node.id
        ssid = data['ssid']
        nonce = data['nonce']
        self.db[ssid].append((int(idx), nonce))

        if len(self.db[ssid]) == self.threshold:
            nonces = self.db[ssid]
            nonces.sort()
            user_nonce = utils.rand_felement_b64str(self.key)
            tau = user_nonce
            for tup in nonces:
                tau += tup[1]
            public, private = User.prep_token(self.token, self.key, 'P@ssword!')
            proofQ = NIZK.proveQ(tau, public, private, self.key)

            #if(NIZK.verifyQ(tau, public, proofQ, self.key)):
                #print("VERIFYQ locally worked")
            #else:
                #print("DID NOT PASS")

            message = {'_type': 'token-auth', 'ssid': ssid, 'token': self.token, 'B': public[1].export_b64str(), 'V': public[2].export_b64str(), 'proof': proofQ, 'user-nonce': user_nonce}
            self.end_local_comp_time = time.perf_counter()
            self.send_to_nodes(message, compression=compression_algo)


    def received_result(self, node, data):
        ssid = data['ssid']
        self.result[ssid][node.id] = data['result']
        if len(self.result[ssid]) == self.threshold and 'DENY' not in self.result[ssid].values():
            #end user timing
            self.end_time = time.perf_counter()
            with open("total_run_time", "a+") as file:
                file.write("{}\n".format(self.end_time - self.start_time))
            with open("client_time", "a+") as file:
                file.write("{}\n".format(self.end_local_comp_time - self.start_time))
        self.stop()




        


