import heapq
from collections import defaultdict

from nodes import Node
from utils import convert_to_seconds


class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_neighbour_nodes(self, node):
        # Delete nodes to insure than only connections from the given node will be analysed
        if node.stop in self.graph_dict:
            del self.graph_dict[node.stop]
        # We only make path in one way because path in another way is not the same!
        for edge in node.edges:
            if edge.start_stop in self.graph_dict:
                self.graph_dict[edge.start_stop].append(Node(edge.end_stop, edge.arr_time, edge.line))
            else:
                self.graph_dict[edge.start_stop] = [Node(edge.end_stop, edge.arr_time, edge.line)]


def astar_stops(start_node, end_node, neighbors_fn):
    cost_so_far = defaultdict(lambda: float('inf'))
    cost_so_far[start_node.stop] = 0

    came_from = {start_node: None}    

    front = [(0, start_node)]
    while front:
        _, curr_node = heapq.heappop(front)

        # Add dynamically new nodes to the graph
        # Line prioritised should be based on the stops
        curr_node.generate_edges(curr_node.line_arr)
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
                    priority = new_cost + stop_heuristic(curr_node, neighbor)
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = curr_node


# In most cases the connection with the least amount of times will also be one of the fastest
# To ensure no extra line changes we will add extra punishment for any line change
def time_cost(curr_node, neighbor):
    time = convert_to_seconds(neighbor.arr_time) - convert_to_seconds(curr_node.arr_time)
    extra_cost = 0 if curr_node.line_arr == neighbor.line_arr else 10000
    return time + extra_cost

# First follow the line
# Second follow from the stop that has a line that goes to the end
# Third analyse stops from the biggest to the smallest
def stop_heuristic(curr_node, neighbor):
    if curr_node.line_arr == neighbor.line_arr:
        return 1
    elif is_there_connection_to_end(curr_node):
        return 25
    else:
        return 999 - get_stop_size(curr_node.stop)

# Stop size is the number of connections that derive from the stop
def get_stop_size(stop):
    df = Node.ALL_CONNECTIONS_DF[Node.ALL_CONNECTIONS_DF['start_stop'] == stop]
    return df['line'].nunique()


def is_there_connection_to_end(curr_node):
    for edge in curr_node.edges:
        if edge.line in Node.LINES_TO_END:
            return True
    return False


# Find the final node based on the end_stop
def find_last_node(came_from, end_stop):
    for node in came_from:
        if node.stop == end_stop:
            return node


# Note - we cannot get time for the last node
def get_shortest_path_astar_stops(start_node, end_stop):
    # This will be used to quickly get to the line arriving to the goal
    Node.set_lines_arriving_to_end(end_stop)
    came_from, cost = astar_stops(start_node, Node(end_stop, None), Graph())

    path = []
    curr_node = find_last_node(came_from, end_stop)
    while curr_node:
        path.append(curr_node)
        curr_node = came_from[curr_node]
    path.reverse()

    return cost, path

