from collections import deque
from copy import deepcopy

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
END = [[1, 2, 3],
       [4, 0, 8],
       [7, 5, 6]]

def print_puzzle(array, step=None):
    if step is not None:
        print("Step:", step)
    for row in array:
        print("+---" * len(row) + "+")
        print("|", end=" ")
        for elem in row:
            if elem == 0:
                print(" ", end=" | ")
            else:
                print(elem, end=" | ")
        print()
    print("+---" * len(array[0]) + "+")
    print()

def get_pos(current_state, element):
    for row_idx, row in enumerate(current_state):
        if element in row:
            return (row_idx, row.index(element))

def is_goal(state, end_state):
    return sorted(state) == sorted(end_state)

def get_adjacent_nodes(current_state):
    list_nodes = []
    empty_pos = get_pos(current_state, 0)
    for dir in DIRECTIONS.keys():
        new_pos = (empty_pos[0] + DIRECTIONS[dir][0], empty_pos[1] + DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < len(current_state) and 0 <= new_pos[1] < len(current_state[0]):
            new_state = deepcopy(current_state)
            new_state[empty_pos[0]][empty_pos[1]] = current_state[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            list_nodes.append((new_state, dir))
    return list_nodes

def build_path(came_from, current_state):
    path = []
    while current_state:
        path.append(current_state)
        current_state, _ = came_from[str(current_state)]
    return path[::-1]

def bfs(start):
    queue = deque([(start, None)])
    came_from = {str(start): (None, None)}
    visited = set([str(start)])
    while queue:
        current_state, direction = queue.popleft()
        if is_goal(current_state, END):
            return build_path(came_from, current_state)
        for next_state, next_direction in get_adjacent_nodes(current_state):
            if str(next_state) not in visited:
                came_from[str(next_state)] = (current_state, next_direction)
                visited.add(str(next_state))
                queue.append((next_state, next_direction))

def count_inversions(array):
    inversions = 0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j] and array[i] != 0 and array[j] != 0:
                inversions += 1
    return inversions

def is_solvable(start):
    flattened_start = [item for sublist in start for item in sublist]
    inversions = count_inversions(flattened_start)
    if len(start) % 2 == 1:
        return inversions % 2 == 0
    else:
        empty_row = len(start) - start.index(0) // len(start[0])
        return (empty_row % 2 == 1) == (inversions % 2 == 0)

if __name__ == '__main__':
    start_matrix = [[6, 4, 7],
                    [8, 5, 0],
                    [3, 2, 1]]
    if is_solvable(start_matrix):
        solution = bfs(start_matrix)
        if solution:
            print("SOLUTION")
            for step, state in enumerate(solution):
                print_puzzle(state, step)
            print('Total steps:', len(solution) - 1)
        else:
            print("Não foi possível encontrar uma solução.")
    else:
        print("O estado inicial não tem solução.")
