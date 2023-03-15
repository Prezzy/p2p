from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, DistVerify, utils

class Verifier (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(Verifier, self).__init__(host, port, id, callback, max_connections)

        self.db = Database()
        self.key = None
        self.token_pubkey = None
        self.neighbours = None

    def node_message(self, connected_node, message):
        
        print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'auth-init'):
                self.received_auth_init(connected_node, message)

            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'token-auth'):
                self.received_token_auth(connected_node, message)

            if (message['_type'] == 'broadcast-step1-result'):
                self.step2(connected_node, message)

            if (message['_type'] == 'broadcast-step2-result'):
                self.step3(connected_node, message)

            if (message['_type'] == 'broadcast-step3-result'):
                self.step4(connected_node, message)
    

    def load_key(self):
        with open("key_ver_{}".format(self.id)) as file:
            key_dict = file.read()
            key_dict

    def unwrap_token(self, token):
        Token = jws.JWS()
        Token.desreialize(token, key=self.token_key)
        payload = json.loads(Token.payload.decode('utf-8'))

        Enc = Cipher.from_b64str(payload['Enc'],self.key)

        return Enc

    def unwrap_ciphers(self, ciphers):
        unwrapped = []
        for ciph in ciphers:
            unwrapped.append(Cipher.from_b64str(ciph, key))
        return unwrapped

    def unwrap_auth_data(self, data):
        '''Parses the initial authentication message
        recieved from the user. takes as input message
        json data and outputs unwrapped objects'''

        Enc = self.unwrap_token(ssid, data['token'])
        ciphertexts = self.unwrap_ciphers(token['ciphers'])
        return Enc, ciphertexts[0], ciphertexts[1], data['user-nonce']


    def received_auth_init(self, node, data):
        nonce = rand_felement_b64str(self.key)
        self.db.new_auth_nonce(data['ssid'], self.id, nonce)

    def received_broadcast_nonde(self, node, data):
        self.db.new_auth_nonce(data['ssid'], data['id'], data['nonce'])

    def received_token_auth(self, node, data):
        ssid = data['ssid']
        if ssid in self.db:
            Enc, B, V, user_nonce = self.unwrap_auth_data(ssid, data)
            self.db.store_token_params(Enc, B, V)

            tau = self.db.store_authentication_nonce(ssid, user_nonce)

            proof = data['proof']

            if NIZK.verifyQ(tau, [Enc, B, V], proof, key):
                ciphertexts, randomness = DistVerify.round1(B, V, key)
                seld.db.store_step1_params(self.id, ssid, ciphertexts)
                proofR = NIZK.proveR(self.id, ciphertexts, randomness, key)
                
                serialized_ciphers = []
                for cipher in ciphertexts:
                    serialized_ciphers.append(cipher.export_b64str())
                response = {'ciphers': serialized_ciphers, 'proofR': proofR}
                # possibly thread this
                self.send_to_nodes(response)

    def step2(self, node, data):
        #ssid = data['ssid']
        #if ssid in self.db:
        #    B = self.db[ssid].B
        #    V = self.db[ssid].V
        #    ciphertexts = self.unwrap_ciphers(data['ciphers'])
        #    proof = data['proof']
        #    if NIZK.verifyR(node.id, ciphertexts, proof, self.key):
                #print a debug message if the thing didn't work
                #gotta do something here then check if I'm the last thread
                #if check:
        #        tau2, C, Ri, ai, zeta, yg, Cbar = DistVerify.round2(self.id, tau, B, V, self.key)
                #TODO: get Ci quickly
         #       proof = NIZK.proveS(self.id, tau2, Ci, Ri, [ai, zeta], self.key)
          #      response = {'Ri': Ri, 'proof': proof}
           #     self.send_to_nodes(response)
        pass

    def step3(self, node, data):
        #ssid = data['ssid']
        #if data['ssid'] in self.db:
        #    tau2 = self.db[data['ssid']].tau2
        #    Cj = self.db[data['ssid']].#TODO
        #    Rj = data['Rj']
        #    proof = data['proof']
         #   if NIZK.verifyS(node.id, tau2, Cj, Ri, proof, self.key):
                #check that I'm the last one
                    #proof = NIZK.proveT(self.id, tau2, gbar, Cbar, Ci, Ri, [ai, zeta], self.key)
                    #response = {'Cbar': Cbar, 'proof':proof}
                    #self.send_to_nodes(response)
        pass

    def step4(self, node, data):
        #ssid = data['ssid']
        #if ssid in self.db:
        #    tau2 = self.db[ssid].tau2
        #    gbar = self.db[ssid].gbar
        #    Cbar = data['Cbar']
        #    Cj = self.db[ssid].
        #    Rj = self.db[ssid].
        #    proof = self.db[ssid]
        #    if NIZK.verify(node.id, tau2, gbar, Cbar, Cj, Rj, proof, self.key):
                #check i'm the last thread to update
                    # response = {'result': 'ACCEPT'}
                    #self.send_to_nodes(response)
        pass
