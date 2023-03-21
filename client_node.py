import time
from client import Client


client = Client("127.0.0.1", 8000, 0)

client. start()

time.sleep(2)

client.connect_with_node('127.0.0.1', 8001)
client.connect_with_node('127.0.0.1', 8002)

client.initiate_auth()
