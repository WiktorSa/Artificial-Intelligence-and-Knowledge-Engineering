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
            if edge.start_stop in self.graph_dict:
                self.graph_dict[edge.start_stop].append(Node(edge.end_stop, edge.arr_time))
            else:
                self.graph_dict[edge.start_stop] = [Node(edge.end_stop, edge.arr_time)]


def astar_stops(start_node, end_node, neighbors_fn):
    cost_so_far = defaultdict(lambda: float('inf'))
    cost_so_far[start_node.stop] = 0

    came_from = {start_node: None}    

    front = [(0, start_node)]
    while front:
        _, curr_node = heapq.heappop(front)

        # Add dynamically new nodes to the graph
        curr_node.generate_edges()
        neighbors_fn.add_neighbour_nodes(curr_node)

        # We can assume that there is always the end stop
        if curr_node.stop == end_node.stop:
            return came_from, cost_so_far[end_node.stop]

        # Avoid crash when arriving to Zorawina
        if curr_node.stop in neighbors_fn.graph_dict:
            for neighbor in neighbors_fn.graph_dict[curr_node.stop]:
                new_cost = cost_so_far[curr_node.stop] + time_cost(curr_node, neighbor)
                if new_cost < cost_so_far[neighbor.stop]:
                    cost_so_far[neighbor.stop] = new_cost
                    priority = new_cost + manhattan_heuristic(neighbor, end_node)
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = curr_node


def time_cost(curr_node, neighbor):
    time = convert_to_seconds(neighbor.arr_time) - convert_to_seconds(curr_node.arr_time)
    # To avoid cases with negative time we add a punishment of one day to the score
    if time < 0:
        time += 24 * 60 * 60
    return time 


def manhattan_heuristic(neighbor, end_node):
    return abs(end_node.stop_location[0] - neighbor.stop_location[0]) + abs(end_node.stop_location[1] - neighbor.stop_location[1])


# Find the final node based on the end_stop
def find_last_node(came_from, end_stop):
    for node in came_from:
        if node.stop == end_stop:
            return node


# Note - we cannot get time for the last node
def get_shortest_path_astar_stops(start_node, end_stop):
    graph = Graph()
    came_from, cost = astar_stops(start_node, Node(end_stop, None), graph)

    path = []
    curr_node = find_last_node(came_from, end_stop)
    while curr_node:
        path.append(curr_node)
        curr_node = came_from[curr_node]
    path.reverse()

    return cost, path

