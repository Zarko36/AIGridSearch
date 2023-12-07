from search import SearchAlgorithm
from contextlib import redirect_stdout
import sys

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

def clear_last_lines(n):
    for _ in range(n):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear line

a_star = ("a_star", [
    "a_star_search_example_1.txt",
    "a_star_search_example_2.txt",
    "a_star_search_example_3.txt",
    "a_star_search_example_4.txt",
    "a_star_search_example_5.txt"
], SearchAlgorithm.a_star_search)
best_first = ("best_first", [
    "best_first_search_example_1.txt",
    "best_first_search_example_2.txt",
    "best_first_search_example_3.txt",
    "best_first_search_example_4.txt",
    "best_first_search_example_5.txt"
], SearchAlgorithm.best_first_search)
greedy = ("greedy", [
    "greedy_search_example_1.txt",
    "greedy_search_example_2.txt",
    "greedy_search_example_3.txt",
    "greedy_search_example_4.txt",
    "greedy_search_example_5.txt"
], SearchAlgorithm.greedy_search)
uniform = ("uniform", [
    "uniform_search_example_1.txt",
    "uniform_search_example_2.txt",
    "uniform_search_example_3.txt",
    "uniform_search_example_4.txt",
    "uniform_search_example_5.txt"
], SearchAlgorithm.uniform_search)
bfs = ("bfs", [
    "bfs_example_1.txt",
    "bfs_example_2.txt",
    "bfs_example_3.txt",
    "bfs_example_4.txt",
    "bfs_example_5.txt"
], SearchAlgorithm.bfs)
dfs = ("dfs", [
    "dfs_example_1.txt",
    "dfs_example_2.txt",
    "dfs_example_3.txt",
    "dfs_example_4.txt",
    "dfs_example_5.txt"
], SearchAlgorithm.dfs)
examples = [
    "example_1.txt",
    "example_2.txt",
    "example_3.txt",
    "example_4.txt",
    "example_5.txt"
]

def exampleFileNameToGrid(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return [line.split() for line in lines]

def algorithmOutputFileNameToGrid(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return int(lines[0].replace('\n', '')), [line.split() for line in lines[1:]]

def getGridDifference(array1, array2, spacing):
    if len(array1) != len(array2) or any(len(row1) != len(row2) for row1, row2 in zip(array1, array2)):
        raise ValueError("Input arrays must have the same shape")

    return [[' ' * (spacing - len(elem1.strip()) + 1) + elem1.strip() + ' ' if elem1 != elem2 else ' ' * spacing + '. ' for elem1, elem2 in zip(row1, row2)] for row1, row2 in zip(array1, array2)]

def printGridDifferences(expected, actual, horizontal = False, verticle = False):
    if horizontal:
        print('\tExpecting | Difference | Actual')
        formattedExpectedGrid, spacingExpected = formatGrid(expected)
        formattedActualGrid, spacingActual = formatGrid(actual)
        gridDifference = getGridDifference(actual, expected, spacingExpected)
        for i in range(len(expected)):
            print('\t\t\t' + ' '.join(formattedExpectedGrid[i]) + '\t\t' + ' '.join(gridDifference[i]) + '\t\t' + ' '.join(formattedActualGrid[i]))
    if verticle:
        print('\tExpecting  : ')
        spacingInbetween = printGrid(expected, '\t\t\t')
        print('\tReceived   : ')
        printGrid(actual, '\t\t\t')
        print('\tDifference : ')
        for row in getGridDifference(actual, expected, spacingInbetween):
            print('\t\t\t' + ' '.join(row))
        print()

def assertEqual(expected, actual):
    if (expected != actual):
        if (isinstance(expected, list)):
            printGridDifferences(expected, actual, True)
        else:
            print(f'\tExpecting : \'{expected}\'\n\tReceived  : \'{actual}\'')
            print()
        return False
    return True

def executeWithoutConsoleOutput(func, output_file = 'output.txt', *args, **kwargs):
    with open(output_file, 'a') as file:
        with redirect_stdout(file):
            return func(*args, **kwargs)

examples = list(map(exampleFileNameToGrid, examples))
algorithmsFilesAndFunction = [bfs, dfs, uniform, greedy, best_first, a_star]
for algorithmName, fileNames, algorithmFunction in algorithmsFilesAndFunction:
    for i, file_name in enumerate(fileNames):
        with open('output.txt', 'w') as file:
            pass
        print(f'Testing {algorithmName}, {file_name}:')
        found_expected, final_state_expected = algorithmOutputFileNameToGrid(file_name)
        printGrid(final_state_expected, '\t', True)
        found_actual, final_state_actual = executeWithoutConsoleOutput(algorithmFunction, 'output.txt', examples[i])
        clear_last_lines(len(final_state_expected) + 2)
        if (not assertEqual(final_state_expected, final_state_actual)):
            exit()
        print(f'    Passed')