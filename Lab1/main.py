from datetime import datetime

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra
from astar_time import get_shortest_path_astar_time
from astar_stops import get_shortest_path_astar_stops
from results import print_results, draw_results

def task1a(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_dijkstra(start_node, end_stop)
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task1b(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_astar_time(start_node, end_stop)
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task1c(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_astar_stops(start_node, end_stop)

    print_results(start_stop, arrival_time, path, end_stop)
    #print(f'Cost: {cost}')
    #draw_results(all_connections, path)


if __name__ == "__main__":
    task1c("żar", "leśnica", datetime.strptime("8:00:00", "%H:%M:%S").time())