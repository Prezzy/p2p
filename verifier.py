import json
import time
from p2pnetwork.node import Node
from db import Database, User
from patetokens.Cipher import Cipher
from patetokens import NIZK, NistKey, DistVerify, utils
from jwcrypto import jwk, jws




class Verifier (Node):

    def __init__(self, host, port, threshold, total, id=None, callback=None, max_connections=4):
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
            if (message['_type'] == 'auth-init'):
                self.received_auth_init(connected_node, message)

            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'token-auth'):
                self.received_token_auth(connected_node, message)

            if (message['_type'] == 'bc-step1-res'):
                self.step2(connected_node, message)

            if (message['_type'] == 'bc-step2-res'):
                self.step3(connected_node, message)

            if (message['_type'] == 'bc-step3-res'):
                self.step4(connected_node, message)
    
    def add_local_comp_time(self, time_data):
        total = max(time_data['auth-init'])
        total += time_data["step1"]
        total += time_data["step2"]
        total += time_data["step3"]
        total += time_data["step4"]
        return total

    def load_keys(self):
        with open("veri_key_{}".format(self.id)) as file:
            self.key = NistKey.DistributedKey()
            key_dict = file.read()
            self.key.from_json(json.loads(key_dict))

        with open("token_public_key.txt".format()) as file:
            key_dict = file.read()
            self.token_pubkey = jwk.JWK.from_json(key_dict)

    def unwrap_token(self, token):
        Token = jws.JWS()
        Token.deserialize(token, key=self.token_pubkey)
        payload = json.loads(Token.payload.decode('utf-8'))

        Enc = Cipher.from_b64str(payload['Enc'],self.key)

        return Enc

    def wrap_ciphers(self, ciphers):
        wrapped = []
        for ciph in ciphers:
            wrapped.append(ciph.export_b64str())
        return wrapped

    def unwrap_ciphers(self, ciphers):
        unwrapped = []
        for ciph in ciphers:
            unwrapped.append(Cipher.from_b64str(ciph, self.key))
        return unwrapped

    def check_last(self, view):
        ''' Takes in a view of objects from a dictionary. Outputs if the calling
        thread is the not the last, the last and all checks passed, or last and a check passed'''
        if len(view) < self.threshold:
            return 0
        elif False not in view:
            return 1
        else:
            return -1


    def unwrap_auth_data(self, data):
        '''Parses the initial authentication message
        recieved from the user. takes as input message
        json data and outputs unwrapped objects'''

        Enc = self.unwrap_token(data['token'])
        ciphertexts = self.unwrap_ciphers([data['B'], data['V']])
        return Enc, ciphertexts[0], ciphertexts[1], data['user-nonce']


    def received_auth_init(self, node, data):
        #Start verifier time
        tick = time.perf_counter()
        nonce = utils.rand_felement_b64str(self.key)
        self.db.new_auth_nonce(data['ssid'], self.id, nonce)
        #print("node {} got request for nonce and made {}".format(self.id, nonce))
        message = {'_type': 'broadcast-nonce', 'ssid':data['ssid'], 'nonce':nonce}
        toc = time.perf_counter()
        self.time["auth-init"].append(toc-tick)
        self.send_to_nodes(message)


    def received_broadcast_nonce(self, node, data):
        self.db.new_auth_nonce(data['ssid'], node.id, data['nonce'])
        #print("node {} got nonce {} from node {}".format(self.id, data['nonce'], node.id))


    def received_token_auth(self, node, data):
        tick = time.perf_counter()
        ssid = data['ssid']
        if self.db.has_key(ssid):
            Enc, B, V, user_nonce = self.unwrap_auth_data(data)
            self.db.store_token_params(ssid, Enc, B, V)

            tau = self.db.store_authentication_nonce(ssid, user_nonce)
            #if not tau:
                #print("Recieved auth token before receiving all nonces")

            proof = data['proof']

            result = NIZK.verifyQ(tau, [Enc, B, V], proof, self.key)
            #print("NODE {} result of proof is {}".format(self.id, result))
            if result:
                ciphertexts, randomness = DistVerify.round1(B, V, self.key)
                self.db.store_step1_params(ssid, self.id, ciphertexts[0], ciphertexts[1])
                proofR = NIZK.proveR(self.id, [B,V]+ciphertexts, randomness, self.key)
                
                #self_test = NIZK.verifyR(self.id, [B,V]+ciphertexts, proofR, self.key)
                #print("Node {} verfied self proof as {}".format(self.id, self_test))


                serialized_ciphers = self.wrap_ciphers(ciphertexts)
                #TODO: remove below, packed into the function call above
                #serialized_ciphers = []
                #for cipher in ciphertexts:
                #    serialized_ciphers.append(cipher.export_b64str())
                response = {'_type':'bc-step1-res', 'ssid':ssid, 'ciphers': serialized_ciphers, 'proofR': proofR}
                toc = time.perf_counter()
                self.time["step1"] = toc-tick 
                self.send_to_nodes(response)

    def step2(self, node, data):
        tick = time.perf_counter()
        ssid = data['ssid']
        if self.db.has_key(ssid):
            B, V = self.db.get_BV(ssid)
            ciphertexts = self.unwrap_ciphers(data['ciphers'])
            proofR = data['proofR']

            if NIZK.verifyR(node.id, [B,V] + ciphertexts, proofR, self.key):
                tau, ciphers = self.db.store_step1_params(ssid, node.id, ciphertexts[0], ciphertexts[1])
                if ciphers:
                    (yg, tau2, ai, C_bar, zeta, Ri_dict, C_dict) = DistVerify.round2(self.id, tau, ciphers, B, V, self.key)
                    self.db.store_step2_params(self.id, ssid, yg, tau2, ai, C_bar, zeta, Ri_dict, C_dict)
                    proofS = NIZK.proveS(self.id, tau2, C_dict[self.id], Ri_dict[self.id], [ai, zeta], self.key)

                    #result = NIZK.verifyS(self.id, tau2, C_dict[self.id], Ri, proofS, self.key)
                    #print("result of self verifyS {}".format(result))

                    response = {'_type': 'bc-step2-res', 'ssid': ssid, 'Rj': Ri_dict[self.id].export_b64str(), 'proofS': proofS}
                    toc = time.perf_counter()
                    self.time["step2"] = toc-tick
                    self.send_to_nodes(response)

    def step3(self, node, data):
        tick = time.perf_counter()
        ssid = data['ssid']
        if self.db.has_key(ssid):
            Rj = Cipher.from_b64str(data['Rj'], self.key)
            tau2, Cj = self.db.get_step3_verify_params(ssid, node.id)
            proofS = data['proofS']
            if NIZK.verifyS(node.id, tau2, Cj, Rj, proofS, self.key):
                flag = self.db.store_step3_params(ssid, node.id, Rj)
                if flag:
                    g_bar, C_bar, Ci, ai, zeta, Ri = self.db.get_step3_proof_params(ssid, self.id)
                    proofT = NIZK.proveT(self.id, tau2, g_bar, C_bar, Ci, Ri, [ai, zeta], self.key)
                    #result = NIZK.verifyT(self.id, tau2, g_bar, C_bar, Ci, Ri, proofT, self.key)
                    response = {'_type': 'bc-step3-res', 'ssid': ssid, 'C_bar': utils.gmp_to_b64str(C_bar), 'proofT':proofT}
                    toc = time.perf_counter()
                    self.time["step3"] = toc-tick
                    self.send_to_nodes(response)

    def step4(self, node, data):
        tick = time.perf_counter()
        ssid = data['ssid']
        if self.db.has_key(ssid):
            C_bar = utils.b64str_to_gmp(data['C_bar'])
            proofT = data['proofT']
            tau2, g_bar, Ci, Ri = self.db.get_step4_params(ssid, node.id)
            if NIZK.verifyT(node.id, tau2, g_bar, C_bar, Ci, Ri, proofT, self.key):

                flag = self.db.store_C_bar(ssid, node.id, C_bar)
                if flag:
                    C_bar_arr, y_bar = self.db.get_C_bar_arr(ssid)
                    result = DistVerify.round4(self.key, C_bar_arr, y_bar)
            
                    response = {'_type':'auth-response', 'ssid': ssid, 'result':'ACCEPT'}
                    toc = time.perf_counter()
                    self.time["step4"] = toc - tick
                    self.send_to_nodes(response)
                    local_comp_time = self.add_local_comp_time(self.time)
                    with open("verifier_{}_time".format(self.id), "a+") as file:
                        file.write("{}\n".format(local_comp_time))
