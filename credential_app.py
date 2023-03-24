import time
from verifier import Verifier
from client import Client
from params import THRESHOLD, TOTAL


def main():
    client = Client("127.0.0.1", 8000, THRESHOLD, TOTAL, 0)
    verifier1 = Verifier("127.0.0.1", 8001, THRESHOLD, TOTAL, 1)
    verifier2 = Verifier("127.0.0.1", 8002, THRESHOLD, TOTAL, 2)

    client.start()
    verifier1.start()
    verifier2.start()

    print("user connecting")
    client.connect_with_node('127.0.0.1', 8001)
    client.connect_with_node('127.0.0.1', 8002)


    print("verifier1 connecting")
    verifier1.connect_with_node('127.0.0.1', 8002)


    client.initiate_auth()
    #time.sleep(2)

    client.stop()
    verifier1.stop()
    verifier2.stop()

main()
