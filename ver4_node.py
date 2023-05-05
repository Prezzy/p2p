import time
from verifier import Verifier
from params import THRESHOLD, TOTAL

PORT = 8004
ID = 4

verifier = Verifier("127.0.0.1", PORT, THRESHOLD, TOTAL, ID)

verifier.start()

res = verifier.connect_with_node('127.0.0.1', 8003)
res = verifier.connect_with_node('127.0.0.1', 8002)

