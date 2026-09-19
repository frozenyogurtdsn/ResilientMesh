
class node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.storage = []
        self.seen_packets = set()

A = node("A")
B = node("B")
C = node("C")

A.neighbors = [B]
B.neighbors = [A, C]
C.neighbors = [B]

print("A neighbors:", [node.node_id for node in A.neighbors])
print("B neighbors:", [node.node_id for node in B.neighbors])
print("C neighbors:", [node.node_id for node in C.neighbors])

