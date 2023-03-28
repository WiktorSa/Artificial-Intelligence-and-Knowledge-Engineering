import random
import math


def tabu_search_sampling(stops):
    random.seed(121)

    n_stops = len(stops)
    
    max_iterations = math.ceil(1.1*(n_stops**2))
    turns_improved = 0
    improve_thresh = 2 * math.floor(math.sqrt(max_iterations))

    tabu_list = []

    distances = [[distance(stops[i], stops[j]) for i in range(n_stops)] for j in range(n_stops)]

    total = 0
    for i in range(n_stops):
        for j in range(n_stops):
            total += distances[i][j]

    current_solution = list(range(n_stops))
    random.shuffle(current_solution)
    best_solution = current_solution[:]
    best_solution_cost = sum([distances[current_solution[i]][current_solution[(i+1) % n_stops]] for i in range(n_stops)])

    for iteration in range(max_iterations):
        if turns_improved > improve_thresh:
            break
        best_neighbor = None
        best_neighbor_cost = float('inf')
        tabu_candidate = (0, 0)

        for i in range(n_stops):
            for j in range(i+1, n_stops):
                if random.random() < 0.5:
                    neighbor = current_solution[:]
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbor_cost = sum([distances[neighbor[i]][neighbor[(i+1)%n_stops]] for i in range(n_stops)])
                    if (i, j) not in tabu_list:
                        if neighbor_cost < best_neighbor_cost:
                            best_neighbor = neighbor[:]
                            best_neighbor_cost = neighbor_cost
                            tabu_candidate = (i, j)

        if best_neighbor is not None:
            current_solution = best_neighbor[:]
            tabu_list.append(tabu_candidate)
            if best_neighbor_cost < best_solution_cost:
                best_solution = best_neighbor[:]
                best_solution_cost = best_neighbor_cost
                turns_improved = 0
            else:
                turns_improved = turns_improved + 1

        print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

    return best_solution, best_solution_cost

def distance(stop1, stop2):
    return math.sqrt((stop2.stop_location[0] - stop1.stop_location[0]) ** 2 + (stop2.stop_location[1] - stop1.stop_location[1]) ** 2)
