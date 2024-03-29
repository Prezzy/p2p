from threading import Lock
from params import THRESHOLD

class User:

    def __init__(self, ssid=None):
        self.ssid = ssid
        self.server_set = [] #empty list for check in store...nonce
        self.user_nonde = None
        self.nonces = []
        self.step1ciphers = []
        self.Enc = None
        self.B = None
        self.V = None
        self.proofQ = None
        self.tau = None
        self.yg = None
        self.tau2 = None
        self.ai = None
        self.C_bar = None
        self.zeta = None
        self.Ri_dict = None
        self.C_dict = None
        self.C_bar_arr = []


class Database:

    def __init__(self):
        self.database = {}
        self.lock = Lock()

    def check_proceed(self, ssid, idx):
        with self.lock:
            if ssid in self.database:
                if idx in self.database[ssid].server_set:
                    return True
                else:
                    return False
            else:
                return False

    def has_key(self, key):
        '''Takes a key to the dictionary and returns True if the 
        key exits'''
        with self.lock:
            return key in self.database

    def create_context(self, ssid, idx, server_set):
        with self.lock:
            #server_set = server_set.split(',')
            if ssid in self.database:
                self.database[ssid].server_set = server_set
            else:
                self.database[ssid] = User()
                self.database[ssid].server_set = server_set


    def store_auth_nonce(self, ssid, myidx, idx, nonce):
        '''Takes in the ssid of user, idx of verifier, and string 
        representation of verifier nonce for the session. Stores
        a tuple with verifier id as int, and the nonce value'''

        with self.lock:
            if ssid in self.database:
                self.database[ssid].nonces.append((int(idx), nonce))
                nonces = self.database[ssid].nonces
                #print(nonces)
                if len(nonces) < THRESHOLD+1 or myidx not in self.database[ssid].server_set: #when we have threshold + user's nonce, we can start step 1!
                    return False
                nonces.sort()
                tau = ''
                for tup in nonces:
                    tau += tup[1]
                self.database[ssid].tau = tau
                return tau
            else:
                self.database[ssid] = User()
                self.database[ssid].nonces.append((int(idx), nonce))
                return False

    def store_token_params(self, ssid, Enc, B, V, proof):
        '''Takes in three ciphertext objects from users auth request
        and stores them'''

        with self.lock:
            user = self.database[ssid]
            user.Enc = Enc
            user.B = B
            user.V = V
            user.proofQ = proof

    
    def get_token_params(self, ssid):

        with self.lock:
            user = self.database[ssid]
            return user.Enc, user.B, user.V, user.proofQ

    #def store_authentication_nonce(self, ssid, idx, user_nonce):
    #    '''Takes a user supplies nonce, stores it, and generates
    #    the tau string of all session nonces, returns tau'''

    #    with self.lock:
    #        tau = user_nonce
    #        nonces = self.database[ssid].nonces
    #        if len(nonces) != THRESHOLD:
    #            return False
    #        nonces.sort()
    #        for tup in nonces:
    #            tau += tup[1]
    #        self.database[ssid].tau = tau
    #        return tau

            

    def store_step1_params(self, ssid, idx, B1, V1):
        '''Takes a list of ciphertext objects produced in
        step1 of distributed verification, stores them in
        the user object'''

        with self.lock:
            if isinstance(idx, str):
                self.database[ssid].step1ciphers.append((int(idx), B1, V1))
            elif isinstance(idx, int):
                self.database[ssid].step1ciphers.append((idx, B1, V1))

            if len(self.database[ssid].step1ciphers) == THRESHOLD:
                self.database[ssid].step1ciphers.sort()
                return (self.database[ssid].tau, self.database[ssid].step1ciphers)
            else:
                return False, False

    def store_step2_params(self, idx, ssid, yg, tau2, ai, C_bar, zeta, Ri_dict, C_dict):
        with self.lock:
            self.database[ssid].yg = yg
            self.database[ssid].tau2 = tau2
            self.database[ssid].ai = ai
            self.database[ssid].C_bar = C_bar
            self.database[ssid].C_bar_arr.append(C_bar)
            self.database[ssid].zeta = zeta
            self.database[ssid].Ri_dict = Ri_dict
            self.database[ssid].C_dict = C_dict


    def get_step3_verify_params(self, ssid, idx):
        with self.lock:
            if self.database[ssid].tau2 is None or self.database[ssid].C_dict is None:
                return False, False
            else:
                return self.database[ssid].tau2, self.database[ssid].C_dict[idx]


    def store_step3_params(self, ssid, idx, Ri):
        with self.lock:
            self.database[ssid].Ri_dict[idx] = Ri 
            if len(self.database[ssid].Ri_dict) == THRESHOLD:
                return True
            else:
                return False
                
    def get_step3_proof_params(self, ssid, idx):
        with self.lock:
            g_bar = self.database[ssid].yg.b
            C_bar = self.database[ssid].C_bar
            Ci = self.database[ssid].C_dict[idx]
            ai = self.database[ssid].ai
            zeta = self.database[ssid].zeta
            Ri = self.database[ssid].Ri_dict[idx]

            return (g_bar, C_bar, Ci, ai, zeta, Ri)


    def get_step4_params(self, ssid, idx):
        with self.lock:
            if idx in self.database[ssid].Ri_dict:
                tau2 = self.database[ssid].tau2
                g_bar = self.database[ssid].yg.b
                Ci = self.database[ssid].C_dict[idx]
                Ri = self.database[ssid].Ri_dict[idx]

                return tau2, g_bar, Ci, Ri
            else:
                return False, False, False, False

    def store_C_bar(self, ssid, idx, C_bar):
        with self.lock:
            self.database[ssid].C_bar_arr.append(C_bar)
            if len(self.database[ssid].C_bar_arr) == THRESHOLD:
                return True
            else:
                return False

    def get_C_bar_arr(self, ssid):
        with self.lock:
            return self.database[ssid].C_bar_arr, self.database[ssid].yg.a

    def get_BV(self, ssid):
        with self.lock:
            return self.database[ssid].B, self.database[ssid].V
