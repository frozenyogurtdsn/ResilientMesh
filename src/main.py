class Packet:
    def __init__(self, packet_id, source, destination, data, ttl):
        self.packet_id = packet_id
        self.source = source
        self.destination = destination
        self.data = data
        self.ttl = ttl




class node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.storage = []
        self.seen_packets = set()
        self.network = None

    def send_packet(self, packet, next_node):
        if packet.ttl <= 0:
            

            print(
                f"{self.node_id}: Packet expired."
            )
            return

        packet.ttl -= 1

        self.network.record_transmission()

        print(
            f"{self.node_id} -> {next_node.node_id}: "
            f"Packet from {packet.source} to {packet.destination} "
            f"(TTL: {packet.ttl})"
        )

        next_node.receive_packet(packet, self)

    def receive_packet(self, packet, sender):
        if sender is None:
            print(
                f"{self.node_id} created packet "
                f"{packet.packet_id}"
            )
        else:
            print(
                f"{self.node_id} received packet "
                f"{packet.packet_id} from {sender.node_id}"
            )

        if packet.packet_id in self.seen_packets:
            self.network.record_duplicate()

            print(
                f"{self.node_id}: Duplicate packet "
                f"{packet.packet_id}. Dropping packet."
            )
            return

        self.seen_packets.add(packet.packet_id)

        if self.node_id == packet.destination:
            self.network.record_delivery()

            print(
                f"{self.node_id} is the destination. "
                f"Packet delivered."
            )
            return

        if packet.ttl <= 0:
            self.network.record_drop()

            print(
                f"{self.node_id}: Packet expired. Dropping packet."
            )
            return

        self.storage.append(packet)

        for neighbor in self.neighbors:
            if neighbor != sender:
                self.send_packet(packet, neighbor)

class Network:
    
    def __init__(self):
        self.nodes = {}
        self.transmission_count = 0
        self.delivered_packets = 0
        self.duplicate_packets = 0
        self.dropped_packets = 0

    def add_node(self, node):
        self.nodes[node.node_id] = node
        node.network = self

    def connect(self, node_a_id, node_b_id):
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]

        if node_b not in node_a.neighbors:
            node_a.neighbors.append(node_b)

        if node_a not in node_b.neighbors:
            node_b.neighbors.append(node_a)
    def record_transmission(self):
        self.transmission_count += 1
        
    def record_delivery(self):
         self.delivered_packets += 1

    def record_duplicate(self):
         self.duplicate_packets += 1

    def record_drop(self):
         self.dropped_packets += 1
network = Network()

A = node("A")
B = node("B")
C = node("C")

network.add_node(A)
network.add_node(B)
network.add_node(C)

network.connect("A", "B")
network.connect("A", "C")
network.connect("B", "C")

packet = Packet("P1", "A", "C", "Hello from A", 5)



print("Packet:", packet.source, "->", packet.destination)
print("Data:", packet.data)
print("TTL:", packet.ttl)

print("A neighbors:", [node.node_id for node in A.neighbors])
print("B neighbors:", [node.node_id for node in B.neighbors])
print("C neighbors:", [node.node_id for node in C.neighbors])


A.receive_packet(packet, None)
print("Total transmissions:", network.transmission_count)
print("Delivered packets:", network.delivered_packets)
print("Duplicate packets:", network.duplicate_packets)
print("Dropped packets:", network.dropped_packets)