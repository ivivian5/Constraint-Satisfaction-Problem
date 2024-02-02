#
# main function for A4 Sudoku Solver assignment.
# Calls sudoku solver to find a solution to user-prompted sudoku board.
#
# CS 131 - Artificial Intelligence
#
# Written by - Vivian Lau vlau02
# Last modified - 11/13/2023

from Sudoku_Solver import SudokuSolver
import timeit

print ("----------------------------------------------------------------------")
print ("Welcome to Vivian's Sudoku Solver!")
print ("----------------------------------------------------------------------")

problem = input("Enter \t\"easy\" if you'd like to run solver on easy sudoku puzzle" +\
                ", \n\t\"hard\" if you'd like to run on hard sudoku puzzle, and " +\
                "\n\t other to enter your own sudoku puzzle: ")

board = [[0 for x in range(9)] for y in range(9)] 

if (problem.lower() == "easy"): # easy puzzle
    # initial board for easy puzzle
    board = [[6,0,8,7,0,2,1,0,0],
             [4,0,0,0,1,0,0,0,2],
             [0,2,5,4,0,0,0,0,0],
             [7,0,1,0,8,0,4,0,5],
             [0,8,0,0,0,0,0,7,0],
             [5,0,9,0,6,0,3,0,1],
             [0,0,0,0,0,6,7,5,0],
             [2,0,0,0,9,0,0,0,8],
             [0,0,6,8,0,5,2,0,3]]
    
elif (problem.lower() == "hard"): # hard puzzle
    # initial board for hard puzzle
    board = [[0,7,0,0,4,2,0,0,0],
             [0,0,0,0,0,8,6,1,0],
             [3,9,0,0,0,0,0,0,7],
             [0,0,0,0,0,4,0,0,9],
             [0,0,3,0,0,0,7,0,0],
             [5,0,0,1,0,0,0,0,0],
             [8,0,0,0,0,0,0,7,6],
             [0,5,4,8,0,0,0,0,0],
             [0,0,0,6,1,0,0,5,0]]
else:
    print()
    for rowIn in range(9):
        for colIn in range(9):
            userIn = input("Enter integer from (1-9) to be inserted at (" + str(rowIn) \
                           + "," + str(colIn) + ") or \"empty\" to leave empty: ")
            print()
            if (not userIn.lower() == "empty" and not userIn == ""):
                try:
                    userIn = (int(userIn))

                    if (userIn < 1 or userIn > 9):
                        raise ValueError

                    board[rowIn][colIn] = userIn

                except ValueError:
                    print ('\n\n\tError: Please give valid integer between 1-9',\
                           'to insert element at (',rowIn, ',', colIn, \
                           ') or \"empty\" to leave empty.\n')

print()
# initialize solver
ss = SudokuSolver(board)

timerStart = timeit.default_timer()
# run solver
ss.run()
timerEnd = timeit.default_timer()

print("Execution Time:", round(timerEnd - timerStart, 3), " seconds\n")

print ("----------------------------------------------------------------------")
print ("Thanks for using Vivian's Knapsack Problem Solver!")
print ("----------------------------------------------------------------------")