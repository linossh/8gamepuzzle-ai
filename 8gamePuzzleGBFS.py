from collections import deque
from copy import deepcopy

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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

def get_pos(current_state, element):
    for row_idx, row in enumerate(current_state):
        if element in row:
            return (row_idx, row.index(element))

def is_goal(state):
    return state == END

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x_goal, y_goal = (state[i][j] - 1) // 3, (state[i][j] - 1) % 3
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance

def hamming_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != END[i][j]:
                distance += 1
    return distance

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

def gbfs_combined(start):
    queue = deque([(start, None)])
    came_from = {str(start): (None, None)}

    while queue:
        queue = deque(sorted(queue, key=lambda x: hamming_distance(x[0]) + manhattan_distance(x[0])))
        current_state, direction = queue.popleft()

        if is_goal(current_state):
            return build_path(came_from, current_state)

        for next_state, next_direction in get_adjacent_nodes(current_state):
            if str(next_state) not in came_from:
                came_from[str(next_state)] = (current_state, next_direction)
                queue.append((next_state, next_direction))

def build_path(came_from, current_state):
    path = []
    while current_state:
        path.append(current_state)
        current_state, _ = came_from[str(current_state)]
    return path[::-1]

if __name__ == '__main__':

    start_matrix = [
        [6, 4, 7],
        [8, 5, 0],
        [3, 2, 1]
    ]

    solution = gbfs_combined(start_matrix)

    print("SOLUTION")
    for step, state in enumerate(solution):
        print_puzzle(state, step)
    print('Total steps:', len(solution) - 1)
