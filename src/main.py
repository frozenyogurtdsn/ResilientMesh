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

    def send_packet(self, packet, next_node):
        if packet.ttl <= 0:
            print(
                f"{self.node_id}: Packet expired."
            )
            return

        packet.ttl -= 1

        print(
            f"{self.node_id} -> {next_node.node_id}: "
            f"Packet from {packet.source} to {packet.destination} "
            f"(TTL: {packet.ttl})"
        )

        next_node.receive_packet(packet)


    def receive_packet(self, packet):
        print(
            f"{self.node_id} received packet "
            f"from {packet.source}"
        )

        if packet.packet_id in self.seen_packets:
            print(
                f"{self.node_id}: Duplicate packet "
                f"{packet.packet_id}. Dropping packet."
            )
            return

        self.seen_packets.add(packet.packet_id)

        if self.node_id == packet.destination:
            print(
                f"{self.node_id} is the destination. "
                f"Packet delivered."
            )
            return

        if packet.ttl <= 0:
            print(
                f"{self.node_id}: Packet expired. Dropping packet."
            )
            return

        self.storage.append(packet)

        for neighbor in self.neighbors:
            if neighbor.node_id == packet.destination:
                print(
                    f"{self.node_id} found destination "
                    f"{neighbor.node_id} as a neighbor."
                )
                self.send_packet(packet, neighbor)
                return




A = node("A")
B = node("B")
C = node("C")

A.neighbors = [B]
B.neighbors = [A, C]
C.neighbors = [B]

packet = Packet("P1", "A", "C", "Hello from A", 5)



print("Packet:", packet.source, "->", packet.destination)
print("Data:", packet.data)
print("TTL:", packet.ttl)

print("A neighbors:", [node.node_id for node in A.neighbors])
print("B neighbors:", [node.node_id for node in B.neighbors])
print("C neighbors:", [node.node_id for node in C.neighbors])


A.send_packet(packet, B)