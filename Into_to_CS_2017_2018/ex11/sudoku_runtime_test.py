import ex11_sudoku as sudoku
import time


# Tip: to print all docstrings to file, use terminal command: pydoc -w ./ex6.py
def tester():
    start_time = time.time()
    if sudoku.run_game('sudoku_tables/sudoku_table1.txt', True):
        print('Sudoku 1 passed')
    else:
        print('sudoku 1 - Failed - No solution')
    print('Runtime:', float(time.time()) - float(start_time))

    if sudoku.run_game('sudoku_tables/sudoku_table2.txt', True):
        print('Sudoku 2 passed')
    else:
        print('sudoku 2 - Failed - No solution')
    print('Runtime:', float(time.time()) - float(start_time))

    if not sudoku.run_game('sudoku_tables/sudoku_table3.txt', True):
        print('Sudoku 3 passed')
    else:
        print('sudoku 1 - Should be no solution')
    print('Total Runtime:', float(time.time()) - float(start_time))


if __name__ == "__main__":
    tester()
