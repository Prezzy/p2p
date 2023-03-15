import time

from verifier import Verifier
from user import User

user = User("127.0.0.1", 8000, 0)
verifier1 = Verifier("127.0.0.1", 8001, 1)
verifier2 = Verifier("127.0.0.1", 8002, 2)

user.start()

verifier1.start()
verifier2.start()


user.connect_with_node('127.0.0.1', 8001)
user.connect_with_node('127.0.0.1', 8002)

#time.sleep(2)

user.stop()
verifier1.stop()
verifier2.stop()
