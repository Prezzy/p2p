import json
from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, NistKey, DistVerify, utils, User
from jwcrypto import jwk, jws


class Client(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(Client, self).__init__(host, port, id, callback, max_connections)
        self.db = {}
        self.key = None
        self.token = None
        self.token_key = None
        self.neighbours = None

        self.fetch_keys()


    def node_message(self, connected_node, message):

        print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'result'):
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

        nonce = utils.rand_felement_b64str(self.key)
        self.db[nonce] = []
        message = {'_type': 'auth-init', 'ssid': nonce}

        self.send_to_nodes(message)
        

    def received_broadcast_nonce(self, node, data):
        idx = data['id']
        nonce = data['nonce']
        self.database['ssid'].append((int(idx), nonce))

        if len(self.database['ssid']) == THRESHOLD:
            nonces = self.database[self.ssid]
            nonces.sort()
            user_nonce = rand_felement_b64str(self.key)
            tau = user_nonce
            for tup in nonces:
                tau += tup[1]
            public, private = User.prep_token(self.token, self.key, 'P@ssword!')
            proofQ = NIZK.proveQ(tau, public, private, key)

            message = {'_type': 'auth-init', 'token': token, 'B': public[1].export_b64str(), 'V': public[2].export_b64str(), 'proof': proofQ, 'user-nonce': user_nonce}

            send_to_nodes(message)


    def received_result(self, node, data):
        result = data['result']
        pass
    ## do something with result.







        


