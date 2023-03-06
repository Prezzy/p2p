class User:

    def __init__(self, ssid=None):
        self.ssid = ssid
        self.nonces = {}
        self.B = None
        self.V = None
        self.Bproduct = None
        self.Tprime = None
        self.coeff = None
        self.Cbar = None
        self.zeta = None
        self.Ri = None
        self.Carr = None


class Database:

    def __init__(self):
        self.ssid = ssid

    def new_auth_nonce(self, ssid, idx, nonce):
        with self.lock:
            if ssid in self.database:
                self.database[ssid].nonces[idx] = nonce
            else:
                self.database[ssid] = User()
                self.database[ssid].nonces[idx] = nonce

    def addBV(self, ssid, B, V):
        with self.lock:
            self.database[ssid].B = B
            self.database[ssid].V = V

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
        with self.lock:

    def getBV(self, ssid, B, V):
        with self.lock:
            return (self.database[ssid].B, self.database[ssid].V)

    def getBproduct(self, ssid, Bproduct):
        with self.lock:
            return self.database[ssid].Bproduct

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
