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
            if self.network.verbose:
                print(
                    f"{self.node_id}: Packet expired."
                )
            return

        forwarded_packet = Packet(
            packet.packet_id,
            packet.source,
            packet.destination,
            packet.data,
            packet.ttl - 1
        )

        self.network.record_transmission()

        if self.network.verbose:
            print(
                f"{self.node_id} -> {next_node.node_id}: "
                f"Packet from {forwarded_packet.source} "
                f"to {forwarded_packet.destination} "
                f"(TTL: {forwarded_packet.ttl})"
            )

        next_node.receive_packet(forwarded_packet, self)

    def receive_packet(self, packet, sender):
        if self.network.verbose:
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

            if self.network.verbose:
                print(
                    f"{self.node_id}: Duplicate packet "
                    f"{packet.packet_id}. Dropping packet."
                )
            return

        self.seen_packets.add(packet.packet_id)

        if self.node_id == packet.destination:
            self.network.record_delivery()

            if self.network.verbose:
                print(
                    f"{self.node_id} is the destination. "
                    f"Packet delivered."
                )
            return

        if packet.ttl <= 0:
            self.network.record_drop()

            if self.network.verbose:
                print(
                    f"{self.node_id}: Packet expired. Dropping packet."
                )
            return

        self.storage.append(packet)

        for neighbor in self.neighbors:
            if neighbor != sender:
                self.send_packet(packet, neighbor)
class Network:
    def __init__(self, verbose=False):
     self.nodes = {}
     self.transmission_count = 0
     self.delivered_packets = 0
     self.duplicate_packets = 0
     self.dropped_packets = 0
     self.generated_packets = 0
     self.verbose = verbose

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

    def generate_packet(self, packet_id, source, destination, data, ttl):
        packet = Packet(
            packet_id,
            source,
            destination,
            data,
            ttl
        )

        self.generated_packets += 1

        return packet

    def run_simulation(self, packets):
        for packet in packets:
            source_node = self.nodes[packet.source]
            source_node.receive_packet(packet, None)

    def reset_metrics(self):
        self.transmission_count = 0
        self.delivered_packets = 0
        self.duplicate_packets = 0
        self.dropped_packets = 0
        self.generated_packets = 0

        for node in self.nodes.values():
            node.seen_packets.clear()
            node.storage.clear()

    def get_metrics(self):
        delivery_rate = 0

        if self.generated_packets > 0:
            delivery_rate = (
                self.delivered_packets
                / self.generated_packets
            )

        return {
            "generated": self.generated_packets,
            "delivered": self.delivered_packets,
            "duplicates": self.duplicate_packets,
            "dropped": self.dropped_packets,
            "transmissions": self.transmission_count,
            "delivery_rate": delivery_rate
        }

    def create_packets(self, num_packets, source, destination, data, ttl):
        packets = []

        for i in range(num_packets):
            packet = self.generate_packet(
                f"P{i + 1}",
                source,
                destination,
                data,
                ttl
            )

            packets.append(packet)

        return packets
    def create_line_topology(self, num_nodes):
        self.nodes = {}

        previous_node = None

        for i in range(num_nodes):
            node_id = chr(ord("A") + i)
            new_node = node(node_id)

            self.add_node(new_node)

            if previous_node is not None:
                self.connect(
                    previous_node.node_id,
                    new_node.node_id
                )

            previous_node = new_node
    def create_diamond_topology(self):
        self.nodes = {}

        for node_id in ["A", "B", "C", "D"]:
            self.add_node(node(node_id))

        self.connect("A", "B")
        self.connect("A", "C")
        self.connect("B", "D")
        self.connect("C", "D")
    
    def create_mesh_topology(self, num_nodes, connectivity):
        self.nodes = {}

        for i in range(num_nodes):
            node_id = chr(ord("A") + i)
            self.add_node(node(node_id))

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if j - i <= connectivity:
                    self.connect(
                        chr(ord("A") + i),
                        chr(ord("A") + j)
                    )
        
        


    def run_experiment(self, num_packets, source, destination, data, ttl):
        self.reset_metrics()

        packets = self.create_packets(
            num_packets,
            source,
            destination,
            data,
            ttl
        )

        self.run_simulation(packets)

        return self.get_metrics()
    
    
network = Network(verbose=False)

connectivity_values = [1, 2, 3, 4]

experiment_results = []

for connectivity in connectivity_values:
    network.create_mesh_topology(10, connectivity)

    source = "A"
    destination = "J"

    results = network.run_experiment(
        100,
        source,
        destination,
        "Hello from A",
        10
    )

    experiment_results.append({
        "connectivity": connectivity,
        **results
    })

print("\nExperiment Results:")

for result in experiment_results:
    print(result)