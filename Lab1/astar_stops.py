import heapq

from nodes import Node


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


def astar_stops(start_node, end_stop, neighbors_fn):
    front = [(0, start_node)]
    came_from = {start_node: None}
    cost_so_far = {start_node.stop: 0}

    while front:
        _, curr_node = heapq.heappop(front)

        # Add dynamically new nodes to the graph
        curr_node.generate_edges()
        neighbors_fn.add_neighbour_nodes(curr_node)

        # We can assume that there is always the end stop
        if curr_node.stop == end_stop:
            # cost_so_far needs to be fixed 
            return came_from, cost_so_far

        # Avoid crash when arriving to Zorawina
        if curr_node.stop in neighbors_fn.graph_dict:
            for neighbor in neighbors_fn.graph_dict[curr_node.stop]:
                new_cost = cost_so_far[curr_node.stop] + 1
                if neighbor.stop not in cost_so_far or new_cost < cost_so_far[neighbor.stop]:
                    cost_so_far[neighbor.stop] = new_cost
                    priority = new_cost + time_cost(curr_node, neighbor)
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = curr_node


def line_cost(node1, node2):
    return 1 if node1.line_arrived == node2.line_arrived else 100


# Find the final node based on the end_stop
def find_last_node(came_from, end_stop):
    for node in came_from:
        if node.stop == end_stop:
            return node


def get_shortest_path_astar_stops(start_node, end_stop):
    graph = Graph()
    came_from, cost = astar_stops(start_node, end_stop, graph)

    path = []
    curr_node = find_last_node(came_from, end_stop)
    while curr_node:
        path.append(curr_node)
        curr_node = came_from[curr_node]
    path.reverse()

    return cost, path
