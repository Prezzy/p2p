import time
from verifier import Verifier
from params import THRESHOLD, TOTAL

PORT = 8002
ID = 2

verifier = Verifier("127.0.0.1", PORT, THRESHOLD, TOTAL, ID)

verifier.start()


