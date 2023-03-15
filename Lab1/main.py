from datetime import datetime

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra
from results import print_results

def main_task1(start_stop, end_stop, optymalization_criteria, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)
    
    time, path = get_shortest_path_dijkstra(start_node, end_stop)
    print_results(start_stop, arrival_time, path, time, end_stop)    

if __name__ == "__main__":
    main_task1("żar", "kowale", "t", datetime.strptime("9:00:00", "%H:%M:%S").time())