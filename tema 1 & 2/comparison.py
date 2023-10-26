from puzzle import init_state, is_final_state, move
from greedy import greedy, manhattan_distance, hamming_distance, euclidean_distance, chebyshev_distance
from iddfs import iddfs
from a_star import a_star
import time

if __name__ == "__main__":
    instances = [
        [2, 7, 5, 0, 8, 4, 3, 1, 6],
        [8, 6, 7, 2, 5, 4, 0, 3, 1],
        [2, 5, 3, 1, 0, 6, 4, 7, 8]
    ]

    heuristics = [manhattan_distance, hamming_distance, euclidean_distance, chebyshev_distance]

    strategies = ["IDDFS", "A*", "Greedy (Manhattan)", "Greedy (Hamming)", "Greedy (Euclidean)", "Greedy (Chebyshev)"]

    for i, instance in enumerate(instances):
        initial_state = init_state(instance)
        print(f"Instance {i + 1}:")

        for j, strategy in enumerate(strategies):
            if strategy == "IDDFS":
                print("IDDFS:")
                start_time = time.time()
                solution, counter = iddfs(initial_state)
            elif strategy == "A*":
                print("A*:")
                counter = 0
                start_time = time.time()
                solution = a_star(initial_state)
            else:
                heuristic = heuristics[j - 2]
                print(f"{strategy}:")
                start_time = time.time()
                solution, counter = greedy(initial_state, heuristic)

            end_time = time.time()
            if solution is not None:
                print(f"Solution found in {end_time - start_time:.6f} seconds.")
                print(f"Solution length: {counter} moves.")
                if strategy == "A*":
                    for step in solution[-1]:
                        print(step)
                else:
                    for step in solution[0]:
                        print(step)
            else:
                print("No solution found.")
            print()
    print("----------")
