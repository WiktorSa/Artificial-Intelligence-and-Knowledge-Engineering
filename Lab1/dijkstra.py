import heapq
from collections import defaultdict

from nodes import Node
from utils import convert_to_seconds

class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_neighbour_nodes(self, node):
        # We only make path in one way because path in another way is not the same!
        for edge in node.edges:
            # Weight is the number of seconds it takes from going from one stop to another
            weight = convert_to_seconds(edge.arr_time) - convert_to_seconds(node.arr_time)

            if edge.start_stop in self.graph_dict:
                self.graph_dict[edge.start_stop].append((Node(edge.end_stop, edge.arr_time), weight))
            else:
                self.graph_dict[edge.start_stop] = [(Node(edge.end_stop, edge.arr_time), weight)]


def dijkstra(graph, start_node):
    distances = defaultdict(lambda: float('inf'))
    distances[start_node.stop] = 0
    prev_nodes = {start_node: None}

    pq = [(0, start_node)]
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        # Add dynamically new nodes to the graph
        curr_node.generate_edges()
        graph.add_neighbour_nodes(curr_node)

        if curr_dist > distances[curr_node.stop]:
            continue
        
        # Avoid crash when arriving to Zorawina
        if curr_node.stop in graph.graph_dict:
            for neighbour, weight in graph.graph_dict[curr_node.stop]:
                new_dist = curr_dist + weight
                if new_dist < distances[neighbour.stop]:
                    distances[neighbour.stop] = new_dist
                    prev_nodes[neighbour] = curr_node
                    heapq.heappush(pq, (new_dist, neighbour))
                
    return distances, prev_nodes

# Find the final node based on the end_stop
def find_last_node(prev_nodes, end_stop):
    for node in prev_nodes:
        if node.stop == end_stop:
            return node
    

def get_shortest_path_dijkstra(start_node, end_stop):
    graph = Graph()
    distances, prev_nodes = dijkstra(graph, start_node)

    path = []
    curr_node = find_last_node(prev_nodes, end_stop)
    while curr_node:
        path.append(curr_node)
        curr_node = prev_nodes[curr_node]
    path.reverse()

    return distances[end_stop], path
