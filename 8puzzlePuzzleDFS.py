from copy import deepcopy
import sys

def count_inversions(lst):
    inversions = 0
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] and lst[j] and lst[i] > lst[j]:
                inversions += 1
    return inversions

def is_solvable(start):
    flatten_start = [num for row in start for num in row if num != 0]
    inversions = count_inversions(flatten_start)
    
    row_empty = sum(start, []).index(0) // len(start[0]) + 1

    if len(start) % 2 == 0:
        if (inversions + row_empty) % 2 != 0:
            return False
    else:
        if inversions % 2 != 0:
            return False
    return True

if __name__ == '__main__':
    start_matrix = [
        [6, 4, 7],
        [8, 5, 0],
        [3, 2, 1]
    ]

    if not is_solvable(start_matrix):
        print("O quebra-cabeça não é solucionável.")
        sys.exit()
    else:
        print("O quebra-cabeça é solucionável.")
        
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
        for row in range(len(current_state)):
            if element in current_state[row]:
                return (row, current_state[row].index(element))

    def is_goal(state):
        return state == END

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

    def dfs(start):
        stack = [(start, None)]
        came_from = {str(start): (None, None)}

        while stack:
            current_state, direction = stack.pop()

            if is_goal(current_state):
                return build_path(came_from, current_state)

            for next_state, next_direction in get_adjacent_nodes(current_state):
                if str(next_state) not in came_from:
                    came_from[str(next_state)] = (current_state, next_direction)
                    stack.append((next_state, next_direction))

    solution = dfs(start_matrix)

    print()
    step_count = 1
    for state in solution:
        print("Step", step_count)
        print_puzzle(state)
        print()
        step_count += 1

    print('Total steps:', len(solution) - 1)
