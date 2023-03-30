import time
from verifier import Verifier
from params import THRESHOLD, TOTAL

PORT = 8001
ID = 1

verifier = Verifier("127.0.0.1", PORT, THRESHOLD, TOTAL, ID)

verifier.start()

res = False
while(not res):
    res = verifier.connect_with_node('127.0.0.1', 8002)

res = False
while(not res):
    res = verifier.connect_with_node('127.0.0.1', 8003)

