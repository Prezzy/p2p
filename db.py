

class User:

    def __init__(self, ssid=None):
        self.ssid = ssid
        self.user_nonde = None
        self.nonces = []
        self.step1ciphers = {}
        self.Enc = None
        self.B = None
        self.V = None
        self.tau
        self.Bproduct = None
        self.Tprime = None
        self.coeff = None
        self.Cbar = None
        self.zeta = None
        self.Ri = None
        self.Carr = None
        self.verifyR_result = {}


class Database:

    def __init__(self):
        self.database = {}

    def new_auth_nonce(self, ssid, idx, nonce):
        '''Takes in the ssid of user, idx of verifier, and string 
        representation of verifier nonce for the session. Stores
        a tuple with verifier id as int, and the nonce value'''

        with self.lock:
            if ssid in self.database:
                self.database[ssid].nonces.append((int(idx), nonce))
            else:
                self.database[ssid] = User()
                self.database[ssid].nonces.append((int(idx), nonce))

    def store_token_params(self, ssid, Enc, B, V):
        '''Takes in three ciphertext objects from users auth request
        and stores them'''

        with self.lock:
            user = self.database[ssid]
            user.Enc = Enc
            user.B = B
            user.V = V


    
    def store_authentication_nonce(self, ssid, user_nonce):
        '''Takes a user supplies nonce, stores it, and generates
        the tau string of all session nonces, returns tau'''

        with self.lock:
            tau = user_nonce
            nonces = self.database[ssid].nonces
            nonces.sort()
            for tup in nonces:
                tau += tup[1]
            self.database[ssid].tau = tau
            return tau

            

    def store_step1_params(self, idx, ssid, BVi):
        '''Takes a list of ciphertext objects produced in
        step1 of distributed verification, stores them in
        the user object'''

        with self.lock:
            self.database[ssid].step1ciphers[idx] = BVi

    def update_R(self, idx, result):
        with self.lock:
            self.database[ssid].verifyR_result[idx] = result
            items = self.database[ssid].verifyR_result.items()
            if len(items) == threhsold:
                if False not in items:
                    return True
                else:
                    return False
            return False

    def addBproduct(self, ssid, Bproduct):
        with self.lock:
            self.database[ssid].Bproduct = Bproduct

    def addTprime(self, ssid, Tprime):
        with self.lock:
            self.database[ssid].Tprime = Tprime

    def addCoeff(self, ssid, coeff):
        with self.lock:
            self.database[ssid].coeff = coeff

    def addCbar(self, ssid, Cbar):
        with self.lock:
            self.database[ssid].Cbar = Cbar

    def addZeta(self, ssid, zeta):
        with self.lock:
            self.database[ssid].zeta = zeta

    def addRi(self, ssid, Ri):
        with self.lock:
            self.database[ssid].Ri = Ri

    def addCarr(self, ssid, Carr):
        pass
        #with self.lock:

    def getBV(self, ssid, B, V):
        pass
        #with self.lock:
        #return (self.database[ssid].B, self.database[ssid].V)

    def getBproduct(self, ssid, Bproduct):
        pass
        #with self.lock:
        #    return self.database[ssid].Bproduct

    def getTprime(self, ssid, Tprime):
        with self.lock:
            return self.database[ssid].Tprime

    def getCoeff(self, ssid, coeff):
        with self.lock:
            return self.database[ssid].coeff

    def getCbar(self, ssid, Cbar):
        with self.lock:
            return self.database[ssid].Cbar

    def getZeta(self, ssid, zeta):
        with self.lock:
            return self.database[ssid].zeta

    def getRi(self, ssid, Ri):
        with self.lock:
            return self.database[ssid].Ri

    def getCarr(self, ssid, Carr):
        with self.lock:
            return self.database[ssid].Carr
