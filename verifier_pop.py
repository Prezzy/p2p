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
        self.key = None
        self.token_pubkey = None
        self.neighbours = None

        self.time = {"auth-init":[]}

        #load keys from file
        self.load_keys()

        self.threshold = threshold
        self.total = total

    def node_message(self, connected_node, message):
        
        #print("node " + self.id + " node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'token-auth'):
                self.token_auth(connected_node, message)

            if (message['_type'] == 'response'):
                self.check_response(connected_node, message)
    
    def add_local_comp_time(self, time_data):
        total = max(time_data['auth-init'])
        total += time_data["step1"]
        total += time_data["step2"]
        total += time_data["step3"]
        total += time_data["step4"]
        return total

    def load_keys(self):
        with open("token_public_key.txt".format()) as file:
            key_dict = file.read()
            self.token_pubkey = jwk.JWK.from_json(key_dict)

    def unwrap_token(self, token):
        Token = jws.JWS()
        Token.deserialize(token, key=self.token_pubkey)
        payload = json.loads(Token.payload.decode('utf-8'))

        return payload

    def received_auth_init(self, node, data):
        #Start verifier time
        tick = time.perf_counter()
        nonce = utils.rand_felement_b64str(self.key)
        self.db.store_auth_nonce(data['ssid'], self.id, nonce)
        message = {'_type': 'broadcast-nonce', 'ssid':data['ssid'], 'nonce':nonce}
        toc = time.perf_counter()
        self.time["auth-init"].append(toc-tick)
        self.send_to_nodes(message, compression=compression_algo)
        

    def received_token_auth(self, node, data):
        tick = time.perf_counter()
        ssid = data['ssid']
        if self.db.has_key(ssid):
            Enc, B, V, user_nonce = self.unwrap_auth_data(data)
            proof = data['proof']
            self.db.store_token_params(ssid, Enc, B, V, proof)
            tau = self.db.store_auth_nonce(ssid, node.id, user_nonce)
            if tau:
                self.step1(ssid, tau, Enc, B, V, proof)
                toc = time.perf_counter()
                self.time["step1"] = toc-tick
            


    def step1(self, ssid, tau, Enc, B, V, proof):
        result = NIZK.verifyQ(tau, [Enc, B, V], proof, self.key)
        if result:
            ciphertexts, randomness = DistVerify.round1(B, V, self.key)
            self.db.store_step1_params(ssid, self.id, ciphertexts[0], ciphertexts[1])
            proofR = NIZK.proveR(self.id, [B,V]+ciphertexts, randomness, self.key)

            serialized_ciphers = self.wrap_ciphers(ciphertexts)
            response = {'_type':'bc-step1-res', 'ssid':ssid, 'ciphers': serialized_ciphers, 'proofR': proofR}
            self.send_to_nodes(response, compression=compression_algo)
