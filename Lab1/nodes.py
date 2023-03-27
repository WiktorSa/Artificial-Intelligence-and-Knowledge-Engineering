from datetime import datetime

import pandas as pd
import numpy as np

"""
Every node is a stop with the time of arrival
Every edge is the best possible connection from the node to another node
"""

class Node:
    ALL_CONNECTIONS_DF = None
    # Which lines arrive to the end
    LINES_TO_END = None

    def __init__(self, stop, arr_time, line_arr=None):
        self.stop = stop
        self.arr_time = arr_time
        # Which line was used to arrive at the given stop
        self.line_arr = line_arr
        self.edges = []
        self.stop_location = self.get_location()

    def generate_edges(self, line_prioritised=None):
        # There is no need to generate edges twice
        if not self.edges:
            df = self.ALL_CONNECTIONS_DF[(self.ALL_CONNECTIONS_DF['start_stop'] == self.stop) & 
                                         (self.ALL_CONNECTIONS_DF['departure_time'] >= self.arr_time)]
            
            # line priority means that the given line will be prioritised when deciding on connection from one stop to another
            if line_prioritised:
                given_line_df = df[df['line'] == line_prioritised]
                # Other lines will be separated into those that arrive to the end goal and those that do not
                other_lines_df = df[df['line'] != line_prioritised]

                if self.LINES_TO_END != []:
                    lines_going_to_end = other_lines_df[other_lines_df['line'].isin(Node.LINES_TO_END)]
                    lines_not_going_to_end = other_lines_df[~other_lines_df['line'].isin(Node.LINES_TO_END)]
                    df = pd.concat([given_line_df, lines_going_to_end, lines_not_going_to_end])
                else:
                    df = pd.concat([given_line_df, other_lines_df])
            
            df = df.drop_duplicates(subset=['end_stop'])

            for ind in df.index:
                self.edges.append(self.Edge(df['line'][ind], df['departure_time'][ind], df['arrival_time'][ind],
                                       df['start_stop'][ind], df['end_stop'][ind]))
                
    def get_location(self):
        df = self.ALL_CONNECTIONS_DF[self.ALL_CONNECTIONS_DF['start_stop'] == self.stop]

        lat = df['start_stop_lat'].mean()
        lon = df['start_stop_lon'].mean()
        # Sometimes connection can only be one way (you can arrive at the given stop but cannot leave)
        if np.isnan(lat) or np.isnan(lon):
            lat = df['end_stop_lat'].mean()
            lon = df['end_stop_lon'].mean()

        return (lat, lon)
    
    # Method used for debugging connections
    def get_stop_info(self):
        return f'Stop {self.stop} arrived at {self.arr_time}\n'
    
    @staticmethod
    def set_lines_arriving_to_end(stop):
        Node.LINES_TO_END = Node.ALL_CONNECTIONS_DF[Node.ALL_CONNECTIONS_DF['end_stop'] == stop]['line'].unique()
                
    def __str__(self):
        text = f'Stop {self.stop} arrived at {self.arr_time}\n'
        for i, edge in enumerate(self.edges, 1):
            text += f'Connection {i}\n'
            text += str(edge)
            text += "\n"
        return text
    
    # Filler method - only used to avoid heapq crash in dijkstra
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


def setup_data(arr_time, filename="connection_graph.csv", remove_night_routes=False):
    df = pd.read_csv(filename, dtype=object, encoding='utf8')
    df.drop(['Unnamed: 0.1', 'Unnamed: 0', 'company'], axis=1, inplace=True)
    df.loc[df['line'] == 'C ', 'line'] = 'C'
    df['departure_time'] = pd.to_datetime(df['departure_time'], format="%H:%M:%S").dt.time
    df['arrival_time'] = pd.to_datetime(df['arrival_time'], format="%H:%M:%S").dt.time
    df['start_stop'] = df['start_stop'].map(lambda x: x.lower())
    df['end_stop'] = df['end_stop'].map(lambda x: x.lower())
    df['start_stop_lat'] = df['start_stop_lat'].map(lambda x: float(x))
    df['start_stop_lon'] = df['start_stop_lon'].map(lambda x: float(x))
    df['end_stop_lat'] = df['end_stop_lat'].map(lambda x: float(x))
    df['end_stop_lon'] = df['end_stop_lon'].map(lambda x: float(x))

    # Sorting values by time to quickly get the quickest connection
    all_possible_connections = df[df['departure_time'] >= arr_time]
    if remove_night_routes:
        all_possible_connections = all_possible_connections[all_possible_connections['departure_time'] <= datetime.strptime("22:00:00", "%H:%M:%S").time()]
    # Removing routes from the same stops
    all_possible_connections = all_possible_connections[all_possible_connections['start_stop'] != all_possible_connections['end_stop']]
    # Sorting values by time to quickly get the quickest connection
    all_possible_connections = all_possible_connections.sort_values(['departure_time', 'arrival_time'])

    Node.ALL_CONNECTIONS_DF = all_possible_connections

    return df
