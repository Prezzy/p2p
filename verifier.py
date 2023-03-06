from p2pnetwork.node import Node
from db import Database, User

class Verifier (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=4):
        super(Verifier, self).__init__(host, port, id, callback, max_connections)

        #TODO: import db structure
        self.db = Database()
        self.key = Key()

    def node_message(self, connected_node, message):
        
        print("node_message from " + connected_node.id + ": " + str(message))

        if('_type' in message):
            if (message['_type'] == 'auth-init'):
                self.received_auth_init(connected_node, message)

            if (message['_type'] == 'broadcast-nonce'):
                self.received_broadcast_nonce(connected_node, message)

            if (message['_type'] == 'token-auth'):
                self.received_token_auth(connected_node, message)

            if (message['_type'] == 'broadcast-step1-result'):
                self.received_step1(connected_node, message)

            if (message['_type'] == 'broadcast-step2-result'):
                self.received_step2(connected_node, message)

            if (message['_type'] == 'broadcast-step3-result'):
                self.received_step3(connected_node, message)
    

    def received_auth_init(self, node, data):
        nonce = rand_felement_b64str(self.key)
        self.db.new_auth_nonce(data['ssid'], self.id, nonce)

    def received_broadcast_nonde(self, node, data):
        self.db.new_auth_nonce(data['ssid'], data['id'], data['nonce'])

    def received_token_auth(self, node, data):
        ssid = data['ssid']
        if ssid in self.db:
            token = data['token']
            B = data['B']
            V = data['V']
            user_nonce = data['user-nonce']
            proof = data['proof']
            #verify()
            #self.db.addBV(ssid,B,V)
            #res = dist1()
            #self.send_to_nodes(res)

    def received_step1(self, node, data):
        ssid = data['ssid']
        if ssid in self.db:
            B = self.db[ssid].B
            V = self.db[ssid].V
            V1 = data['V1']
            V2 = data['V2']
            V3 = data['V3']
            proof = data['proof']
            #verify()

    def received_step2(self, node, data):
        ssid = data['ssid']
        if data['ssid'] in self.db:
            tau2 = self.db[data['ssid']].tau2
            Cj = self.db[data['ssid']].#TODO
            Rj = data['Rj']
            proof = data['proof']
            #verify()

    def received_step3(self, node, data):
        ssid = data['ssid']
        if ssid in self.db:
            tau2 = self.db[ssid].tau2
            gbar = self.db[ssid].gbar
            Cbar = data['Cbar']
            Cj = self.db[ssid].
            Rj = self.db[ssid].
            proof = self.db[ssid]
            #verify()




