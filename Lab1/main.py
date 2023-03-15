from datetime import datetime

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra
from astar import get_shortest_path_astar
from results import print_results

def main_task1(start_stop, end_stop, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)
    
    #cost, path = get_shortest_path_dijkstra(start_node, end_stop)
    #print_results(start_stop, arrival_time, path, end_stop)
    #print(f'Travel took {time / 60} minutes')

    cost, path = get_shortest_path_astar(start_node, end_stop, "t")
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')

if __name__ == "__main__":
    main_task1("żar", "kowale", datetime.strptime("9:00:00", "%H:%M:%S").time())