from datetime import datetime

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra

def main_task1(start_stop, end_stop, optymalization_criteria, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)
    
    get_shortest_path_dijkstra(start_node, end_stop)

if __name__ == "__main__":
    main_task1("spółdzielcza", "krzyki", "t", datetime.strptime("12:00:00", "%H:%M:%S").time())