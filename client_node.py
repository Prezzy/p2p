import time
from client import Client
from params import THRESHOLD, TOTAL


client = Client("127.0.0.1", 8000, THRESHOLD, TOTAL, 0)

client. start()

client.connect_with_node('127.0.0.1', 8001)
client.connect_with_node('127.0.0.1', 8002)
#client.connect_with_node('127.0.0.1', 8003)
#client.connect_with_node('127.0.0.1', 8004)
client.initiate_auth()
