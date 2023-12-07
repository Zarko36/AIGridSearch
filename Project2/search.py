from typing import List, Tuple
from queue import Queue
from queue import PriorityQueue
import heapq
from heapq import heappop, heappush

def formatGrid(grid):
    maxLength = 0
    new_grid = grid.copy()
    for row in new_grid:
        for position in row:
            maxLength = max(maxLength, len(position))
    for i, row in enumerate(new_grid):
        for j, position in enumerate(row):
            new_grid[i][j] = ' ' * (maxLength - len(position) + 1) + position + ' '
    return new_grid, maxLength

def printGrid(grid, space = '', withAxis = False):
    formattedGrid = [row[:] for row in grid]
    if withAxis:
        formattedGrid.insert(0, [str(i) for i in range(len(formattedGrid[0]))])
        formattedGrid.insert(1, [' '] * len(formattedGrid[0]))
        for i, row in enumerate(formattedGrid):
            if i >= 2:
                row.insert(0, str(i - 2) + ')')
            else:
                row.insert(0, ' ')

    formattedGrid, maxLength = formatGrid(formattedGrid)
    for row in formattedGrid:
        print(space + ' '.join(row))
    return maxLength

class SearchAlgorithm:
    
    @staticmethod
    def uniform_search(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        heap = [(0, start_row, start_col)]
        heapq.heapify(heap)
        visited = set()
        visited.add((start_row, start_col))
        costDict = {(start_row, start_col): 0}
        order = 1
        while heap:
            cost, row, col = heapq.heappop(heap)
            if grid[row][col] == '0':
                grid[row][col] = str(order)
                order += 1
            if grid[row][col] == 't':
                return (1, grid)
            for r, c in [(row, col+1), (row+1, col), (row, col-1), (row-1, col)]:
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '-1':
                    if cost+1 < costDict.get((r, c), float('inf')):
                        heapq.heappush(heap, (cost+1, r, c))
                        costDict[(r, c)] = cost+1
        return (-1, grid)

    @staticmethod
    def dfs(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        def dfs_helper(row: int, col: int, visited: List[Tuple[int, int]]) -> bool:
            if grid[row][col] == 't':
                return True
            visited.append((row, col))
            for r, c in [(row-1, col), (row, col-1), (row+1, col), (row, col+1)]:
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] in ['0', 't'] and (r, c) not in visited:
                    if dfs_helper(r, c, visited):
                        return True
            return False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        visited = []
        found = dfs_helper(start_row, start_col, visited)
        count = 1
        for row, col in visited:
            if grid[row][col] == '0':
                grid[row][col] = str(count)
                count += 1
        return (1 if found else -1, grid)

    @staticmethod
    def bfs(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        q = Queue()
        q.put((start_row, start_col))
        visited = set()
        visited.add((start_row, start_col))
        while not q.empty():
            row, col = q.get()
            if grid[row][col] == 't':
                return (1, grid)
            for r, c in [(row, col+1), (row+1, col), (row, col-1), (row-1, col)]:
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '-1':
                    if (r, c) not in visited:
                        q.put((r, c))
                        visited.add((r, c))
                        if grid[r][c] == '0':
                            grid[r][c] = str(len(visited) - 1)
                        if grid[r][c] == 't':
                            return (1, grid)
        return (-1, grid)

    
    @staticmethod
    def best_first_search(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        def heuristic(currentCell):
            return abs(currentCell[0] - target_row) + abs(currentCell[1] - target_col)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 't':
                    target_row, target_col = i, j
                    break
        pq = PriorityQueue()
        pq.put((heuristic((start_row, start_col)), start_row, start_col))
        costDict = {(start_row, start_col): 0}
        order = 1
        while not pq.empty():
            cost, row, col = pq.get()
            if grid[row][col] == '0':
                grid[row][col] = str(order)
                order += 1
            if grid[row][col] == 't':
                return (1, grid)
            for r, c in [(row, col+1), (row+1, col), (row, col-1), (row-1, col)]:
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '-1':
                    if cost+1 < costDict.get((r, c), float('inf')):
                        pq.put((heuristic((r, c)), r, c))
                        costDict[(r, c)] = cost+1
        return (-1, grid)

    @staticmethod
    def a_star_search(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        def heurestic(cell):
            return abs(cell[0] - target_row) + abs(cell[1] - target_col)
        visited = set()
        order = 1
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 't':
                    target_row, target_col = i, j
                    break
        start = (start_row, start_col)
        target = (target_row, target_col)
        costScore = {start: 0}
        heuresticScore = [(heurestic(start), start)]
        while heuresticScore:
            _, currentCell = heappop(heuresticScore)
            if currentCell == target:
                return (1, grid)
            if grid[currentCell[0]][currentCell[1]] == '0':
                grid[currentCell[0]][currentCell[1]] = str(order)
                order += 1
            visited.add(currentCell)
            for neighbor in [(currentCell[0], currentCell[1]+1), (currentCell[0]+1, currentCell[1]), (currentCell[0], currentCell[1]-1), (currentCell[0]-1, currentCell[1])]:
                r, c = neighbor
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '-1':
                    if neighbor in visited:
                        continue
                    newCostScore = costScore[currentCell] + 1
                    newHeuresticScore = newCostScore + heurestic(neighbor)
                    if newCostScore < costScore.get(neighbor, float('inf')):
                        costScore[neighbor] = newCostScore
                    heappush(heuresticScore, (newHeuresticScore, neighbor))
        return (-1, grid)

    @staticmethod
    def greedy_search(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        grid = [row[:] for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 's':
                    start_row, start_col = i, j
                    break
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 't':
                    target_row, target_col = i, j
                    break
        visited = set()
        heap = []
        heapq.heapify(heap)
        heapq.heappush(heap, (abs(start_row - target_row) + abs(start_col - target_col), start_row, start_col))
        min_r = start_row
        min_c = start_col
        min = abs(start_row - target_row) + abs(start_col - target_col)
        order = 1
        while heap:
            distance, row, col = heapq.heappop(heap)
            if grid[row][col] == 't':
                return 1, grid
            if (row, col) not in visited:
                visited.add((row, col))
                if grid[row][col] != 's':
                    grid[row][col] = str(order)
                    order += 1
                for r, c in [(row, col+1), (row+1, col), (row, col-1), (row-1, col)]:
                    if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and (r, c) not in visited:
                        distance = abs(c - target_col) + abs(r - target_row)
                        h_check = abs(min_r - target_row) + abs(min_c - target_col)
                        if distance < min and grid[r][c] != '-1' and distance < h_check:
                            min = distance
                            min_r, min_c = r, c
                heapq.heappush(heap, (distance, min_r, min_c))
        return -1, grid


if __name__ == "__main__":

    example1 = [
    ['0', '0', '0', '0'],
        ['0', '-1', '-1', 't'],
        ['s', '0', '-1', '0'],
        ['0', '0', '0', '-1']
    ]
    example2 = [
        ['s', '0', '0', '0', '-1', '-1', '-1', '-1'],
        ['0', '0', '0', '0', '0', '-1', '-1', '-1'],
        ['-1', '-1', '0', '-1', '-1', '0', '0', '0'],
        ['-1', '0', '0', '0', '0', '0', '0', 't']
    ]
    example3 = [
        ['s', '0', '0', '-1', '0'],
        ['0', '-1', '0', '-1', 't'],
        ['0', '-1', '0', '0', '0'],
        ['0', '0', '0', '-1', '0'],
        ['0', '-1', '-1', '-1', '0']
    ]
    example4 = [
        ['s', '0', '0', '0', '0'],
        ['-1', '-1', '0', '0', '0'],
        ['t', '-1', '0', '0', '0',],
        ['-1', '0', '0', '-1', '0'],
        ['0', '-1', '0', '-1', '0']
    ]
    example5 = [
        ['0', '0', '0', '-1', '0'],
        ['0', '0', '0', '-1', '0'],
        ['s', '0', '0', '0', '0'],
        ['0', '0', '0', '-1', 't'],
        ['0', '0', '0', '-1', '0']
    ]
    example6 = [
        ['0', '0', '0', '0', '0', '0', '0', '-1', '0', '0'],
        ['0', '0', '-1', '0', '0', '0', '0', '0', '0', '-1'],
        ['0', '-1', '-1', '0', '-1', '-1', '-1', '0', '-1', '0'],
        ['0', '0', '0', '0', '-1', '0', '0', '0', '-1', '0'],
        ['0', '-1', 't', '0', '0', '0', '-1', '-1', '0', '-1'],
        ['0', '0', '-1', '0', '-1', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '-1', '0', '-1', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '-1', '0', '0'],
        ['0', 's', '-1', '0', '-1', '0', '0', '0', '0', '0'],
        ['-1', '0', '0', '0', '0', '-1', '-1', '-1', '0', '-1']
    ]
    example7 = [
        ['0', '0', '0', '0', '0', '0', '-1', '0', '0', '0'],
        ['0', '-1', '0', '0', '0', '0', '0', '-1', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '-1', '0', '0', '0', '0', '0', '-1', 's', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', 't', '0', '0', '0', '0', '0', '0']
    ]

    test = "a_star_search"
    if test == "dfs":
        print("Depth-First Search")
        found, final_state = SearchAlgorithm.dfs(example1)
        print("Example 1")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")
        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.dfs(example2)
        print("Example 2")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.dfs(example3)
        print("Example 3")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.dfs(example4)
        print("Example 4")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.dfs(example5)
        print("Example 5")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
    elif test == "bfs":
        print("Breadth-First Search")
        found, final_state = SearchAlgorithm.bfs(example1)
        print("Example 1")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")
        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.bfs(example2)
        print("Example 2")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.bfs(example3)
        print("Example 3")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.bfs(example4)
        print("Example 4")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.bfs(example5)
        print("Example 5")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
    elif test == "uniform_search":
        print("Uniform Search")
        # found, final_state = SearchAlgorithm.uniform_search(example1)
        # print("Example 1")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")
        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        # found, final_state = SearchAlgorithm.uniform_search(example2)
        # print("Example 2")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")

        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        # found, final_state = SearchAlgorithm.uniform_search(example3)
        # print("Example 3")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")

        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        # found, final_state = SearchAlgorithm.uniform_search(example4)
        # print("Example 4")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")

        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        # found, final_state = SearchAlgorithm.uniform_search(example5)
        # print("Example 5")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")

        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        # found, final_state = SearchAlgorithm.uniform_search(example6)
        # print("Example 6")
        # if found == 1:
        #     print("Target found!")
        # else:
        #     print("Target not found.")

        # for row in final_state:
        #     print(' '.join(row))
        # print("\n")
        found, final_state = SearchAlgorithm.uniform_search(example7)
        print("Example 7")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
    elif test == "greedy_search":
        print("Greedy Search")
        found, final_state = SearchAlgorithm.greedy_search(example1)
        print("Example 1")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")
        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.greedy_search(example2)
        print("Example 2")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.greedy_search(example3)
        print("Example 3")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.greedy_search(example4)
        print("Example 4")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.greedy_search(example5)
        print("Example 5")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
    elif test == "best_first_search":
        print("Best First Search")
        found, final_state = SearchAlgorithm.best_first_search(example1)
        print("Example 1")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")
        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.best_first_search(example2)
        print("Example 2")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.best_first_search(example3)
        print("Example 3")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.best_first_search(example4)
        print("Example 4")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.best_first_search(example5)
        print("Example 5")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
    elif test == "a_star_search":
        print("A* Search")
        found, final_state = SearchAlgorithm.a_star_search(example1)
        print("Example 1")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")
        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.a_star_search(example2)
        print("Example 2")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.a_star_search(example3)
        print("Example 3")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.a_star_search(example4)
        print("Example 4")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")
        found, final_state = SearchAlgorithm.a_star_search(example5)
        print("Example 5")
        if found == 1:
            print("Target found!")
        else:
            print("Target not found.")

        for row in final_state:
            print(' '.join(row))
        print("\n")