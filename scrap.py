import time
from verifier import Verifier
from client import Client
from p2pnetwork.node import Node

node1 = Node("127.0.0.1", 8000, 1)
node2 = Node("127.0.0.1", 8001, 2)
node3 = Node("127.0.0.1", 8002, 3)
node4 = Node("127.0.0.1", 8003, 4)


print("starting")
node1.start()
node2.start()
node3.start()
node4.start()

node1.debug = True
print("connecting")
flag = True

while(flag):
    time.sleep(2)
    res = node1.connect_with_node("127.0.0.1", 8005)
    if res:
        flag = False
#node2.connect_with_node("127.0.0.1", 8002)
#node3.connect_with_node("127.0.0.1", 8003)
#node4.connect_with_node("127.0.0.1", 8000)

#node1.connect_with_node("127.0.0.1", 8002)
#node2.connect_with_node("127.0.0.1", 8000)

print("all connected")
