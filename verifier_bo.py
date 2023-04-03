import json
import time
from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, NistKey, DistVerify, utils
from jwcrypto import jwk, jws

compression_algo = 'bzip2'


class Verifier (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(Verifier, self).__init__(host, port, id, callback, max_connections)

        self.db = Database()
        self.token_pubkey = None
        self.neighbours = None

        #load keys from file
        self.load_keys()

    def node_message(self, connected_node, message):
        
        #print("node " + self.id + " node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'auth-init'):
                self.received_auth_init(connected_node, message)

    def load_keys(self):
        with open("token_public_key.txt".format()) as file:
            key_dict = file.read()
            self.token_pubkey = jwk.JWK.from_json(key_dict)

    def unwrap_token(self, token):
        Token = jws.JWS()
        Token.deserialize(token, key=self.token_pubkey)
        payload = json.loads(Token.payload.decode('utf-8'))

        return payload

    def received_token_auth(self, node, data):
        tick = time.perf_counter()
        payload = self.unwrap_token(data)
        #check things in payload
        toc = time.perf_counter()
        message = {"result": "Accept"}
        self.send_to_nodes(message, compresion=compresion_algo)
        with open("client_time_bo", "a+") as file:
            file.write("{}\n".format(toc-tick))
