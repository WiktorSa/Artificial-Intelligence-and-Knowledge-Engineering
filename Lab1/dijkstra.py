import heapq
from collections import defaultdict

def dijkstra2(graph_dict, start):
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = 0
    pq = [(0, start)]
    prev_nodes = {node: None for node in graph_dict}
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor, weight in graph_dict[curr_node]:
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))
    return distances, prev_nodes


class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_edges(self, node):
        return
        edges = self.generate_edges(node)

        # We only make path in one way because path in another way is not the same!
        for start_node, end_node, start_stop, end_stop, weight in edges:
            # Don't add paths that go backwards (e.g. go back one stop)
            if not self.is_path_go_backwards(start_stop, end_stop):
                if start_stop in self.graph_dict:
                    self.graph_dict[start_stop].append((end_node, weight))
                    #self.graph_dict[start_stop].append((end_stop, weight, start_node, end_node))
                else:
                    self.graph_dict[start_stop] = [(end_node, weight)]
                    #self.graph_dict[start_stop] = [(end_stop, weight, start_node, end_node)]

    @staticmethod
    def generate_edges(node):
        edges = []
        for neighbor_node in node.nodes:
            # Cost is calculated based on how much seconds it takes to get from one stop to another
            edges.append((node, neighbor_node, neighbor_node.start_stop, neighbor_node.end_stop, neighbor_node.arr_time_seconds_midnight - node.arr_time_seconds_midnight))

        return edges
    
    def is_path_go_backwards(self, start_stop, end_stop):
        if end_stop not in self.graph_dict:
            return False
        
        for stop, _, _, _ in self.graph_dict[end_stop]:
            if stop == start_stop:
                return True
            
        return False


def dijkstra(graph, start_node):
    distances = defaultdict(lambda x: float('inf'))
    prev_nodes = defaultdict(lambda x: None)

    distances[start_node] = 0
    prev_nodes[start_node] = None

    pq = [(0, start_node)]    
    """
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        # Add dynamically new nodes to the graph
        curr_node.generate_nodes()
        graph.add_edges(curr_node)

        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph.graph_dict[curr_node.end_stop]:
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
        #        print(distances)
                #prev_nodes[neighbor] = curr_node
                #heapq.heappush(pq, (new_dist, neighbor))
    """
                
    return distances, prev_nodes

# start_node contains start_stop while end_node contains end_stop with no connections
def get_shortest_path_dijkstra(start_node, end_stop):
    graph = Graph()
    distances, prev_nodes = dijkstra(graph, start_node)
    """
    path = []
    curr_node = end_stop
    while curr_node:
        path.append(curr_node)
        curr_node = prev_nodes[curr_node]
    path.reverse()
    return distances[goal], path
    """
