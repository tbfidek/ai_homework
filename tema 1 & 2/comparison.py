from puzzle import init_state, is_final_state, move
from greedy import greedy, manhattan_distance, hamming_distance, euclidean_distance, chebyshev_distance
from iddfs import iddfs
import time

if __name__ == "__main__":
    instances = [
        [2, 7, 5, 0, 8, 4, 3, 1, 6],
        [8, 6, 7, 2, 5, 4, 0, 3, 1],
        [2, 5, 3, 1, 0, 6, 4, 7, 8]
    ]

    heuristics = [manhattan_distance, hamming_distance, euclidean_distance, chebyshev_distance]

    strategies = ["IDDFS", "Greedy (Manhattan)", "Greedy (Hamming)", "Greedy (Euclidean)", "Greedy (Chebyshev)"]

    for i, instance in enumerate(instances):
        initial_state = init_state(instance)
        print(f"Instance {i + 1}:")

        for j, heuristic in enumerate(heuristics):
            if j == 0:
                print("IDDFS:")
                start_time = time.time()
                solution = iddfs(initial_state)
            else:
                print(f"Greedy ({heuristics[j-1].__name__}):")
                start_time = time.time()
                solution = greedy(initial_state, heuristic)

            end_time = time.time()
            if solution is not None:
                print(f"Solution found in {end_time - start_time:.2f} seconds.")
                print(f"Solution length: {len(solution[0])} moves.")
                for step in solution[0]:
                    print(step)
            else:
                print("No solution found.")
            print()

        print("----------")
