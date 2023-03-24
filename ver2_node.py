import time
from verifier import Verifier
from params import THRESHOLD, TOTAL

verifier2 = Verifier("127.0.0.1", 8002, THRESHOLD, TOTAL, 2)

verifier2.start()

time.sleep(5)

verifier2.connect_with_node("127.0.0.1", 8001)
