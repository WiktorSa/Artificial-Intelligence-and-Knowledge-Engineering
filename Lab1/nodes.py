import pandas as pd

"""
Every node is a stop with the time of arrival
Every edge is the best possible connection from the node to another node
"""

class Node:
    ALL_CONNECTIONS_DF = None

    def __init__(self, stop, arr_time):
        self.stop = stop
        self.arr_time = arr_time
        self.edges = []

    def generate_edges(self, optimalization_criteria='t'):
        # There is no need to generate edges twice
        if not self.edges:
            df = self.ALL_CONNECTIONS_DF[(self.ALL_CONNECTIONS_DF['start_stop'] == self.stop) & 
                                         (self.ALL_CONNECTIONS_DF['departure_time'] >= self.arr_time)]
            
            # If time is a criteria than we only take connections that will take us the fastest from one stop to another
            if optimalization_criteria == 't':
                df = df.drop_duplicates(subset=['end_stop'])
            # TO DO - optimalize for lines
            elif optimalization_criteria == 's':
                df = df.drop_duplicates(subset=['line', 'end_stop'])

            for ind in df.index:
                self.edges.append(self.Edge(df['line'][ind], df['departure_time'][ind], df['arrival_time'][ind],
                                       df['start_stop'][ind], df['end_stop'][ind]))
                
    def __str__(self):
        text = f'Stop {self.stop} arrived at {self.arr_time}\n'
        for i, edge in enumerate(self.edges, 1):
            text += f'Connection {i}\n'
            text += str(edge)
            text += "\n"
        return text
    
    # Filler method - only used to avoid heapq crash
    def __gt__(self, other):
        return True

    class Edge:
        def __init__(self, line, depart_time, arr_time, start_stop, end_stop):
            self.line = line
            self.depart_time = depart_time
            self.arr_time = arr_time
            self.start_stop = start_stop
            self.end_stop = end_stop

        def __str__(self):
            return f'Line: {self.line}, Departure time: {self.depart_time}, Arrival time: {self.arr_time}, Start: {self.start_stop}, End: {self.end_stop}'


def setup_data(arr_time, filename="connection_graph.csv"):
    df = pd.read_csv(filename, dtype=object, encoding='utf8')
    df.drop(['Unnamed: 0.1', 'Unnamed: 0', 'company', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat', 'end_stop_lon'], axis=1, inplace=True)
    df.loc[df['line'] == 'C ', 'line'] = 'C'
    df['departure_time'] = pd.to_datetime(df['departure_time'], format="%H:%M:%S").dt.time
    df['arrival_time'] = pd.to_datetime(df['arrival_time'], format="%H:%M:%S").dt.time
    df['start_stop'] = df['start_stop'].map(lambda x: x.lower())
    df['end_stop'] = df['end_stop'].map(lambda x: x.lower())

    # Because there are no travels during night we can drop times that are before our departure time
    df = df[(df['departure_time'] >= arr_time)]
    # Sorting values by time to quickly get the quickest connection
    df = df.sort_values(['departure_time', 'arrival_time'])

    Node.ALL_CONNECTIONS_DF = df
