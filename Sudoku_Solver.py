#
# Constraint Satisfaction Problem approach for 
# A4 Sudoku Solver assignment.
#
# CS 131 - Artificial Intelligence
#
# Written by - Vivian Lau vlau02
# Last modified - 11/13/2023

import math # used to round floats down to integers (floor)
import copy 

class SudokuSolver:
    
    # sets up board and possible values for each square
    def __init__(self, boardIn):
        self.possVal = [[set() for x in range(9)] for y in range(9)] 
        self.numEmptyElem = 81
        self.board = boardIn
        self.setUp()
        
    # makes sure puzzle is valid and calls solver() to solve sudoku if so
    def run(self):
        if not self.isBoardValid():
            print("Invalid input for board, cannot run solver.")
        else:
            print("Puzzle problem:")
            self.printBoard()
            
            if self.solver(0) == True:
                print("-------------------------------------------\n")
                print("Solution found:")
                self.printBoard()
            else:
                print("No solution found.")
        
    # given number of elements that have been filled (from (0,0)), finds solution to
    # sudoku puzzle specified when initializing the class
    def solver(self, numElemFilled):
        found = False
        totalElemTried = numElemFilled # when trying (0,0), there is 0 elements tried
        
        if (totalElemTried >= 80): # checks if all elements are filled
            return True
        if (not self.isFillPossible()): # checks if solution is possible
            return False
        
        # continue until filled up all elements or ran out of options
        while not self.numEmptyElem == 0 and not found:
            # get row and column of element to try
            rowIn = math.floor(totalElemTried/9)
            colIn = (totalElemTried)%9
            subSqIn = (math.floor(rowIn / 3) * 3) + math.floor(colIn / 3)
            
            # copy possible values of element to try
            possValueAtElem = copy.deepcopy(self.possVal[rowIn][colIn])
            
            # check if there's no solution (having empty elem with no possible values)
            if self.board[rowIn][colIn] == 0 and len(possValueAtElem) == 0:
                return False
            
            # if spot is empty and has possible values, update state for trying
            if self.board[rowIn][colIn] == 0:
                # update possible values (element is filled while trying)
                self.possVal[rowIn][colIn] = set()

                self.numEmptyElem -= 1 # update numEmptyElem
            
            # try all values at spot
            for tryValue in possValueAtElem:
                
                # save all indices of impacted elements (row, col, subsq)
                impactElemCoor = self.setImpactedElemCoor(rowIn, colIn, subSqIn, tryValue)
                
                self.board[rowIn][colIn] = tryValue # fill element with possible value

                # recursively call to fill another element with updated state
                if self.solver(totalElemTried) == True: # there was a solution found
                    return True
                else: # possible value is not solution, so revert state
                    for coor in impactElemCoor: # tuple that is (row, col)
                        self.possVal[coor[0]][coor[1]].add(tryValue)
                    self.board[rowIn][colIn] = 0
            
            # after trying all possible values at element, if element is not filled
            if (self.board[rowIn][colIn] == 0):
                self.numEmptyElem += 1
                self.possVal[rowIn][colIn] = possValueAtElem # restore possibilities
                return False # no solution for elem at current state
            else: # if element is filled
                totalElemTried += 1 # increment number of elements tried
                if (totalElemTried == 81): # if filled all 80 elements
                    return True # solution is found, otherwise try filling next element
        
    def printBoard(self):
        print()
        for rowIn in range(9):
            if rowIn in [3, 6]:
                print ('-----+-----+-----')
            print(' ', end='')
            for colIn in range(9):
                if colIn in [3, 6]:
                    print (' | ', end=""),
                print (self.board[rowIn][colIn], end="")
            print()
        print()
        
    # updates all impacted elements by given possible value to be tried by element of 
    # given coordinates by removing the given possible value from the elements
    # returns all indices of impacted elements (row, col, subsq) by given possible value
    # to be tried by element of given coordinates
    def setImpactedElemCoor(self, rowIn, colIn, subSqIndex, tryValue):
        impactElemCoor = set()

        # iterate through row/col in search of elements with same possible value
        # to save the coordinates and remove the possible value
        for i in range(9):
            # check if ith element in same row has same possible value
            if tryValue in self.possVal[rowIn][i]:
                impactElemCoor.add((rowIn, i))
                self.possVal[rowIn][i].remove(tryValue)

            # check if ith element in same column has same possible value
            if tryValue in self.possVal[i][colIn]:
                impactElemCoor.add((i, colIn))
                self.possVal[i][colIn].remove(tryValue)

            # get the row and col index of the ith element in the subsquare
            subSqRowIn = math.floor(subSqIndex/3)*3 + math.floor(i/3)
            subSqColIn = (subSqIndex % 3)*3 + i%3
            # check if ith element in same subquare has same possible value
            if tryValue in self.possVal[subSqRowIn][subSqColIn]:
                impactElemCoor.add((subSqRowIn, subSqColIn))
                self.possVal[subSqRowIn][subSqColIn].remove(tryValue)
        
        return impactElemCoor
        
    # remove all empty squares in a given 1-d list
    def removeEmpty(self, domainIn):
        while 0 in domainIn:
            domainIn.remove(0)
        
    # returns the desired column as a 1-d list
    # left-most column is considered index 0 and increases right-ward
    def getCol(self, colIndex):
        singleCol = []
        for row in self.board:
            singleCol.append(row[colIndex])
        return singleCol
    
    # returns the desired square as a 1-d list
    # in-order from left-right columns then top-down rows
    def getSquare(self, squareIndex):
        singleSquare = []
        
        rowStart = math.floor(squareIndex / 3) * 3
        colStart = (squareIndex % 3) * 3
        
        for i in range(rowStart, rowStart + 3):
            for j in range(colStart, colStart + 3):
                singleSquare.append(self.board[i][j])
        
        return singleSquare
        
    # returns boolean value of if given row is valid under constraints
    def isRowValid(self, rowIndex):
        return self.isConstraintValid(self.board[rowIndex])
        
    # returns boolean value of if given column is valid under constraints
    def isColValid(self, colIndex):
        return self.isConstraintValid(self.getCol(colIndex))
    
    # returns boolean value of if given square is valid under constraints
    def isSquareValid(self, squareIndex):
        return self.isConstraintValid(self.getSquare(squareIndex))
    
    # returns boolean value of if there any numbers used twice in a list 
    # of elements of any single constraint (row, column, square)
    def isConstraintValid(self, constraintElemsIn):
        constraintElems = copy.deepcopy(constraintElemsIn)
        self.removeEmpty(constraintElems) # remove empty elements
        
        # return if there are any duplicates (no duplicates is true)
        return len(set(constraintElems)) == len(constraintElems)
        
    def isFillPossible(self):
        # go through each element in each constraint (row, col, sq)
        for constraint in range(9):
            rowPossVal = set()
            colPossVal = set()
            sqPossVal = set()
            
            rowNumEmpty = 0
            colNumEmpty = 0
            sqNumEmpty = 0
            
            for index in range(9):
                # get all possible values in row
                rowPossVal = rowPossVal.union(self.possVal[constraint][index])
                if self.board[constraint][index] == 0: # if is empty
                    rowNumEmpty += 1
                
                # get all possible values in col
                colPossVal = colPossVal.union(self.possVal[index][constraint])
                if self.board[index][constraint] == 0: # if is empty
                    colNumEmpty += 1
                    
                subSqRowIn = math.floor(constraint/3)*3 + math.floor(index/3)
                subSqColIn = (constraint % 3)*3 + index%3
                
                # get all possible values in subSquare
                sqPossVal = sqPossVal.union(self.possVal[subSqRowIn][subSqColIn])
                if self.board[subSqRowIn][subSqColIn] == 0: # if is empty
                    sqNumEmpty += 1
            
            # if not enough possible values for empty spot in constraint, no solution
            if (len(rowPossVal) < rowNumEmpty or len(colPossVal) < colNumEmpty \
                or len(sqPossVal) < sqNumEmpty):
                return False
        
        # if enough values for empty spots in constraint, solution exists
        return True
        
    # returns boolean value of if the whole board is currently valid 
    # under all constraints
    def isBoardValid(self):
        # check if board has 9 rows
        if (len(self.board) < 9):
            return False # board is invalid
        
        for i in range(0,9):
            # check if board has 9 columns in each row
            if (len(self.board[i]) < 9):
                return False # board is invalid
            
            # check if there are any duplicate numbers in a constraint on the board
            if ((not self.isRowValid(i)) or 
                (not self.isColValid(i)) or 
                (not self.isSquareValid(i)) ):
                return False # board is invalid
        
        # if did not fail any constraints, then board is valid
        return True
        
    # initializes possVal and numEmptyElem
    # iterate through each square initialize all possible values (as a set) that
    # each square could be based on current values on board in possVal matrix
    def setUp(self):
        numEmptyElem = 0
        for rowIn in range(9):
            for colIn in range(9):
                # check if element is empty
                if self.board[rowIn][colIn] == 0:
                    numEmptyElem += 1 # update numEmptyElem
                
                    # get which subsquare the current square is in
                    sqIn = (math.floor(rowIn / 3) * 3) + math.floor(colIn / 3)

                    # get values under relevant constraints that are predetermined
                    usedVal = set(self.board[rowIn]).union(set(self.getCol(colIn)), 
                                                   set(self.getSquare(sqIn)) )

                    # possible value for square is all unused values
                    self.possVal[rowIn][colIn] = \
                    set([0,1,2,3,4,5,6,7,8,9]).difference(usedVal)
                    
                else: # already has a pre-determined value
                    self.possVal[rowIn][colIn] = set() # has no possible values