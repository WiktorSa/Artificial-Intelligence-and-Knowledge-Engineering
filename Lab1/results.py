def print_results(start_stop, arrival_time, path, end_stop):
    edges = get_edges(path)
    connections = get_connections(edges)
    cur_arr_time = arrival_time

    print(f'Start at {start_stop} at {cur_arr_time}')
    for connection in connections:
        if connection.depart_time != cur_arr_time:
            print(f'Wait at {connection.start_stop} from {cur_arr_time} to {connection.depart_time}')
        print(connection)
        cur_arr_time = connection.arr_time

    print(f'Arrived at {end_stop} at {cur_arr_time}')

# Get all edges leading to the goal
def get_edges(path):
    edges = []
    for i in range(len(path)-1):
        for edge in path[i].edges:
            if edge.end_stop == path[i+1].stop:
                edges.append(edge)

    return edges

# Get all connections leading to the goal (it will be used to determine when to change line)
def get_connections(edges):
    first_edge = edges.pop(0)
    connections = [Connection(first_edge.line, first_edge.start_stop, first_edge.end_stop, 
                              first_edge.depart_time, first_edge.arr_time)]
    cur_conn_idx = 0
    for edge in edges:
        if edge.line == connections[cur_conn_idx].line:
            connections[cur_conn_idx].end_stop = edge.end_stop
            connections[cur_conn_idx].arr_time = edge.arr_time
        else:
            connections.append(Connection(edge.line, edge.start_stop, 
                                           edge.end_stop, edge.depart_time, 
                                           edge.arr_time))
            cur_conn_idx += 1

    return connections


class Connection:
    def __init__(self, line, start_stop, end_stop, depart_time, arr_time):
        self.line = line
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.depart_time = depart_time
        self.arr_time = arr_time

    def __str__(self):
        return f'Travel with line {self.line} from {self.start_stop} to {self.end_stop} from {self.depart_time} to {self.arr_time}'
