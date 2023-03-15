import heapq
import math


class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_edges(self, node):
        # We only make path in one way because path in another way is not the same!
        for edge in node.edges:
            if edge.start_stop in self.graph_dict:
                self.graph_dict[edge.start_stop].append(edge)
            else:
                self.graph_dict[edge.start_stop] = [edge]


def astar(start_node, end_stop, neighbors_fn, heuristic_fn):
    front = [(0, start_node)]
    came_from = {start_node: None}
    cost_so_far = {start_node.stop: 0}

    while front:
        _, current = heapq.heappop(front)

        if current.stop == end_stop:
            break

        for neighbor in neighbors_fn(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_fn(goal, neighbor)
                heapq.heappush(front, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, cost_so_far[goal]

# Find the final node based on the end_stop
def find_last_node(prev_nodes, end_stop):
    for node in prev_nodes:
        if node.stop == end_stop:
            return node

def get_shortest_path_astar(start_node, end_stop):
    graph = Graph()
    distances, prev_nodes = astar(start_node, end_stop, graph)

    path = []
    curr_node = find_last_node(prev_nodes, end_stop)
    while curr_node:
        path.append(curr_node)
        curr_node = prev_nodes[curr_node]
    path.reverse()

    return distances[end_stop], path

