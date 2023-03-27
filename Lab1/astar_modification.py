import copy
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
                self.graph_dict[edge.start_stop].append(Node(edge.end_stop, edge.arr_time, edge.line))
            else:
                self.graph_dict[edge.start_stop] = [Node(edge.end_stop, edge.arr_time, edge.line)]


class GraphToGoal:
    def __init__(self, line_prioritised):
        self.graph_dict = {}
        self.line_prioritised = line_prioritised

    def add_neighbour_nodes(self, node):
        # We only make path in one way because path in another way is not the same!
        for edge in node.edges:
            if edge.line == self.line_prioritised:
                if edge.start_stop in self.graph_dict:
                    self.graph_dict[edge.start_stop].append(Node(edge.end_stop, edge.arr_time, edge.line))
                else:
                    self.graph_dict[edge.start_stop] = [Node(edge.end_stop, edge.arr_time, edge.line)]


# Only get to the stop from which we can go immediately to the destination
def astar_stops_modified(start_node, neighbors_fn):
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

        # If we have a stop from which we can take the line to the end we go with this line
        line_to_end = get_line_to_end(curr_node)
        if line_to_end:
            return came_from, cost_so_far[curr_node.stop], curr_node, line_to_end

        # Avoid crash when arriving to Zorawina
        if curr_node.stop in neighbors_fn.graph_dict:
            for neighbor in neighbors_fn.graph_dict[curr_node.stop]:
                new_cost = cost_so_far[curr_node.stop] + time_cost(curr_node, neighbor)
                if new_cost < cost_so_far[neighbor.stop]:
                    cost_so_far[neighbor.stop] = new_cost
                    priority = new_cost + stop_heuristic(curr_node, neighbor)
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = curr_node


def astar_stops_to_goal(start_node, end_node, neighbors_fn):
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
                    priority = new_cost + manhattan_heuristic(neighbor, end_node)
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = curr_node


# In most cases the connection with the least amount of times will also be one of the fastest
# To ensure no extra line changes we will add extra punishment for any line change
def time_cost(curr_node, neighbor):
    time = convert_to_seconds(neighbor.arr_time) - convert_to_seconds(curr_node.arr_time)
    # To avoid cases with negative time we add a punishment of one day to the score
    if time < 0:
        time += 24 * 60 * 60

    extra_cost = 0 if curr_node.line_arr == neighbor.line_arr else 100000
    return time + extra_cost


# First follow the line
# Second analyse stops from the biggest to the smallest
def stop_heuristic(curr_node, neighbor):
    if curr_node.line_arr == neighbor.line_arr:
        return 1
    else:
        return 999 - get_stop_size(curr_node.stop)


def manhattan_heuristic(neighbor, end_node):
    return abs(end_node.stop_location[0] - neighbor.stop_location[0]) + abs(end_node.stop_location[1] - neighbor.stop_location[1])


# Stop size is the number of connections that derive from the stop
def get_stop_size(stop):
    df = Node.ALL_CONNECTIONS_DF[Node.ALL_CONNECTIONS_DF['start_stop'] == stop]
    return df['line'].nunique()


def get_line_to_end(curr_node):
    for edge in curr_node.edges:
        if edge.line in Node.LINES_TO_END:
            return edge.line
    return None


# Find the final node based on the end_stop
def find_last_node(came_from, end_stop):
    for node in came_from:
        if node.stop == end_stop:
            return node


def get_shortest_path_astar_stops_mod(start_node, end_stop):
    Node.set_lines_arriving_to_end(end_stop)
    came_from, cost, node_to_end, line_to_end = astar_stops_modified(start_node, Graph())
    came_from2, cost2 = astar_stops_to_goal(Node(node_to_end.stop, node_to_end.arr_time, line_to_end), Node(end_stop, None), GraphToGoal(line_to_end))

    path = get_path(node_to_end, came_from)
    path2 = get_path(find_last_node(came_from2, end_stop), came_from2)
    path.extend(path2)

    return cost + cost2, path

def get_path(node, came_from):
    path = []
    curr_node = node
    while curr_node:
        path.append(curr_node)
        curr_node = came_from[curr_node]
    path.reverse()

    return path
