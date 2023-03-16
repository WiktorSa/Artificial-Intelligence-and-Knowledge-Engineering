from datetime import datetime

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra
from astar_time import get_shortest_path_astar_time
from results import print_results

def task1a(start_stop, end_stop, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_dijkstra(start_node, end_stop)
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')


def task1b(start_stop, end_stop, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_astar_time(start_node, end_stop)
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')


def task1c(start_stop, end_stop, arrival_time):
    setup_data(arrival_time)
    start_node = Node(start_stop, arrival_time)

    cost, path = get_shortest_path_astar(start_node, end_stop, "s")
    print_results(start_stop, arrival_time, path, end_stop)
    #print(f'Cost: {cost}')


if __name__ == "__main__":
    task1b("żar", "kowale", datetime.strptime("9:00:00", "%H:%M:%S").time())