from datetime import datetime
import time

from nodes import Node, setup_data
from dijkstra import get_shortest_path_dijkstra
from astar_time import get_shortest_path_astar_time
from astar_stops import get_shortest_path_astar_stops
from astar_modification import get_shortest_path_astar_stops_mod
from tabu_search import tabu_search
from tabu_search_length import tabu_search_length
from tabu_search_aspiration import tabu_search_aspiration
from tabu_search_sampling import tabu_search_sampling
from results import print_results, draw_results

def task1a(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time, remove_night_routes=True)
    start_node = Node(start_stop, arrival_time)

    time_start = time.time()
    cost, path = get_shortest_path_dijkstra(start_node, end_stop)
    print(f'Execution time: {time.time() - time_start:.2f} seconds')
    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task1b(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time, remove_night_routes=True)
    start_node = Node(start_stop, arrival_time)

    time_start = time.time()
    cost, path = get_shortest_path_astar_time(start_node, end_stop)
    print(f'Execution time: {time.time() - time_start:.2f} seconds')

    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)

def task1c(start_stop, end_stop, arrival_time):
    all_connections = setup_data(arrival_time, remove_night_routes=True)
    start_node = Node(start_stop, arrival_time, '-1')

    time_start = time.time()
    cost, path = get_shortest_path_astar_stops(start_node, end_stop)
    print(f'Execution time: {time.time() - time_start:.2f} seconds')

    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task1d(start_stop, end_stop, arrival_time):
    # We remove night routes to avoid situation when the best way to get to the stop is with the night route
    # We need to do that because we don't have all the data about night routes
    all_connections = setup_data(arrival_time, remove_night_routes=True)
    start_node = Node(start_stop, arrival_time, '-1')

    time_start = time.time()
    cost, path = get_shortest_path_astar_stops_mod(start_node, end_stop)
    print(f'Execution time: {time.time() - time_start:.2f} seconds')

    print_results(start_stop, arrival_time, path, end_stop)
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task2a(start_stop, optimalization_criteria, arrival_time,  *list_stops):
    all_connections = setup_data(arrival_time, remove_night_routes=True)

    stops = [Node(stop, None) for stop in list_stops]
    stops_dict = {0: start_stop, len(stops)+1: start_stop}
    best_solution, best_solution_cost = tabu_search(stops)

    time_start = time.time()
    print("\nStops from the first to last")
    print(f'{start_stop}, ', end='')
    for i, idx in enumerate(best_solution, 1):
        stops_dict[i] = stops[idx].stop
        print(f'{stops[idx].stop}, ', end='')
    print(start_stop)
    print("Best solution cost: {}".format(best_solution_cost))
    print(f'Execution time: {time.time() - time_start:.8f} seconds\n')

    start_node = Node(stops_dict[0], arrival_time)
    start_node.generate_edges()
    path = [start_node]
    cost = 0
    cur_arr_time = arrival_time
    for i in range(len(stops_dict)-1):
        if optimalization_criteria == 't':
            part_cost, part_path = get_shortest_path_astar_time(Node(stops_dict[i], cur_arr_time), stops_dict[i+1])
        elif optimalization_criteria == 's':
            part_cost, part_path = get_shortest_path_astar_stops_mod(Node(stops_dict[i], cur_arr_time, '-1'), stops_dict[i+1])
        else:
            raise Exception("Incorrect optimalization criteria")
        
        print(f'\nConnection from {stops_dict[i]} to {stops_dict[i+1]}')
        print_results(stops_dict[i], cur_arr_time, part_path, stops_dict[i+1])

        # Don't remember the first stop to avoid stops duplicates
        path.extend(part_path[1:])
        cost += part_cost
        cur_arr_time = path[-1].arr_time

    print()
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task2b(start_stop, optimalization_criteria, arrival_time,  *list_stops):
    all_connections = setup_data(arrival_time, remove_night_routes=True)

    stops = [Node(stop, None) for stop in list_stops]
    stops_dict = {0: start_stop, len(stops)+1: start_stop}
    best_solution, best_solution_cost = tabu_search_length(stops)

    time_start = time.time()
    print("\nStops from the first to last")
    print(f'{start_stop}, ', end='')
    for i, idx in enumerate(best_solution, 1):
        stops_dict[i] = stops[idx].stop
        print(f'{stops[idx].stop}, ', end='')
    print(start_stop)
    print("Best solution cost: {}".format(best_solution_cost))
    print(f'Execution time: {time.time() - time_start:.8f} seconds\n')

    start_node = Node(stops_dict[0], arrival_time)
    start_node.generate_edges()
    path = [start_node]
    cost = 0
    cur_arr_time = arrival_time
    for i in range(len(stops_dict)-1):
        if optimalization_criteria == 't':
            part_cost, part_path = get_shortest_path_astar_time(Node(stops_dict[i], cur_arr_time), stops_dict[i+1])
        elif optimalization_criteria == 's':
            part_cost, part_path = get_shortest_path_astar_stops_mod(Node(stops_dict[i], cur_arr_time, '-1'), stops_dict[i+1])
        else:
            raise Exception("Incorrect optimalization criteria")
        
        print(f'\nConnection from {stops_dict[i]} to {stops_dict[i+1]}')
        print_results(stops_dict[i], cur_arr_time, part_path, stops_dict[i+1])

        # Don't remember the first stop to avoid stops duplicates
        path.extend(part_path[1:])
        cost += part_cost
        cur_arr_time = path[-1].arr_time

    print()
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task2c(start_stop, optimalization_criteria, arrival_time,  *list_stops):
    all_connections = setup_data(arrival_time, remove_night_routes=True)

    stops = [Node(stop, None) for stop in list_stops]
    stops_dict = {0: start_stop, len(stops)+1: start_stop}
    best_solution, best_solution_cost = tabu_search_aspiration(stops)

    time_start = time.time()
    print("\nStops from the first to last")
    print(f'{start_stop}, ', end='')
    for i, idx in enumerate(best_solution, 1):
        stops_dict[i] = stops[idx].stop
        print(f'{stops[idx].stop}, ', end='')
    print(start_stop)
    print("Best solution cost: {}".format(best_solution_cost))
    print(f'Execution time: {time.time() - time_start:.8f} seconds\n')

    start_node = Node(stops_dict[0], arrival_time)
    start_node.generate_edges()
    path = [start_node]
    cost = 0
    cur_arr_time = arrival_time
    for i in range(len(stops_dict)-1):
        if optimalization_criteria == 't':
            part_cost, part_path = get_shortest_path_astar_time(Node(stops_dict[i], cur_arr_time), stops_dict[i+1])
        elif optimalization_criteria == 's':
            part_cost, part_path = get_shortest_path_astar_stops_mod(Node(stops_dict[i], cur_arr_time, '-1'), stops_dict[i+1])
        else:
            raise Exception("Incorrect optimalization criteria")
        
        print(f'\nConnection from {stops_dict[i]} to {stops_dict[i+1]}')
        print_results(stops_dict[i], cur_arr_time, part_path, stops_dict[i+1])

        # Don't remember the first stop to avoid stops duplicates
        path.extend(part_path[1:])
        cost += part_cost
        cur_arr_time = path[-1].arr_time

    print()
    print(f'Cost: {cost}')
    draw_results(all_connections, path)


def task2d(start_stop, optimalization_criteria, arrival_time,  *list_stops):
    all_connections = setup_data(arrival_time, remove_night_routes=True)

    stops = [Node(stop, None) for stop in list_stops]
    stops_dict = {0: start_stop, len(stops)+1: start_stop}
    best_solution, best_solution_cost = tabu_search_sampling(stops)

    time_start = time.time()
    print("\nStops from the first to last")
    print(f'{start_stop}, ', end='')
    for i, idx in enumerate(best_solution, 1):
        stops_dict[i] = stops[idx].stop
        print(f'{stops[idx].stop}, ', end='')
    print(start_stop)
    print("Best solution cost: {}".format(best_solution_cost))
    print(f'Execution time: {time.time() - time_start:.8f} seconds\n')

    start_node = Node(stops_dict[0], arrival_time)
    start_node.generate_edges()
    path = [start_node]
    cost = 0
    cur_arr_time = arrival_time
    for i in range(len(stops_dict)-1):
        if optimalization_criteria == 't':
            part_cost, part_path = get_shortest_path_astar_time(Node(stops_dict[i], cur_arr_time), stops_dict[i+1])
        elif optimalization_criteria == 's':
            part_cost, part_path = get_shortest_path_astar_stops_mod(Node(stops_dict[i], cur_arr_time, '-1'), stops_dict[i+1])
        else:
            raise Exception("Incorrect optimalization criteria")
        
        print(f'\nConnection from {stops_dict[i]} to {stops_dict[i+1]}')
        print_results(stops_dict[i], cur_arr_time, part_path, stops_dict[i+1])

        # Don't remember the first stop to avoid stops duplicates
        path.extend(part_path[1:])
        cost += part_cost
        cur_arr_time = path[-1].arr_time

    print()
    print(f'Cost: {cost}')
    draw_results(all_connections, path)

    
if __name__ == "__main__":
    task1b("leśnica", "wojnów", datetime.strptime("10:00:00", "%H:%M:%S").time())
    # task1b("kwiska", "pl. grunwaldzki", datetime.strptime("10:00:00", "%H:%M:%S").time())
    # task2d('pilczyce', 's', datetime.strptime("8:00:00", "%H:%M:%S").time(), 'zakrzów', 'leśnica', 'kromera', 'biskupin', 'krzyki')
    # task2a('leśnica', 't', datetime.strptime("8:00:00", "%H:%M:%S").time(), 'pl. grunwaldzki', 'klecina', 'racławicka', 'oporów')