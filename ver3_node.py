import time
from verifier import Verifier
from params import THRESHOLD, TOTAL

verifier1 = Verifier("127.0.0.1", 8003, THRESHOLD, TOTAL, 3)

verifier1.start()

time.sleep(5)

#verifier1.connect_with_node('127.0.0.1', 8002)
