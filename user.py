from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, DistVerify, utils, User


class User(Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(User, self).__init__(host, port, id, callback, max_connections)
        self.db = {}
        self.key = None
        self.token = None
        self.token_pubkey = None
        self.neighbours = None

    def node_message(self, connected_node, message):

        print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'result'):
                self.received_result(connected_node, message)

    def initiate_auth(self):
        self.token = User.make_token(key, token_key, 'JohnDoe', 'P@ssword!')

        nonce = rand_felement_b64str(self.key)
        self.database[nonce] = []
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







        


