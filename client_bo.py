import json
import time
from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, NistKey, DistVerify, utils, User
from jwcrypto import jwk, jws


compression_algo = 'bzip2'

class Client(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(Client, self).__init__(host, port, id, callback, max_connections)
        self.db = {}
        self.result = {}
        self.key = None
        self.token = None
        self.token_key = None
        self.neighbours = None
        self.start_time = None
        self.end_local_comp_time = None
        self.end_time = None

        self.fetch_keys()


    def node_message(self, connected_node, message):

        #print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'auth-response'):
                self.received_result(connected_node, message)


    def fetch_keys(self):
        '''This function is called as part of the init
        for user node. read key files and create the key
        objects'''
        with open("token_key.txt", "r") as file:
            key_dict = file.read()
            self.token_key = jwk.JWK.from_json(key_dict)

    def initiate_auth(self):
        nonce = utils.rand_felement_b64str(self.key)
        payload = {'username':username,'nonce':nonce}
        payload = json.dumps(payload)
        Token = jws.JWS(payload.encode('utf-8'))
        Token.add_signature(self.token_key, None, json_encode({"alg": "RS256"}))
        token = Token.serialize()

        message = {"_type":}

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

            message = {'_type': 'token-auth', 'ssid': ssid, 'token': self.token}
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




        


