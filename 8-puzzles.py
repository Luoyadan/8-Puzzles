# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:22:11 2016
CS170 Individual Project : The Eight Puzzle
@author: Yadan Luo
"""

# Solves a randomized 8-puzzle using uniformcost/A* with mistile/A* with Mahanttan dis
import random

_goal_state = [[1,2,3],

               [4,5,6],

               [7,8,0]]


class Puzzle:


    def __init__(self):

        # initialize heuristic value of nodes

        self._hval = 0

        # initialize search depth of current instance of nodes

        self._depth = 0

        # parent node in search path

        self._parent = None
        

        self.adj_matrix = []

        for i in range(3):

            self.adj_matrix.append(_goal_state[i][:])


    def __str__(self):

        res = ''

        for row in range(3):

            res += ' '.join(map(str, self.adj_matrix[row]))

            res += '\r\n'

        return res



    def _copy(self):

        p = Puzzle()

        for i in range(3):

            p.adj_matrix[i] = self.adj_matrix[i][:]

        return p



    def _get_legal_moves(self):

        """Returns list of tuples with which the possible space may be swapped"""

        # find location of the blank

        row, col = self.find(0)

        space = []

        # find which pieces can move there

        if row > 0:

            space.append((row - 1, col))

        if col > 0:

            space.append((row, col - 1))

        if row < 2:

            space.append((row + 1, col))

        if col < 2:

            space.append((row, col + 1))

        return space



    def _generate_moves(self):

        space = self._get_legal_moves()

        zero = self.find(0)



        def swap_and_copy(a, b):

            p = self._copy()

            p.swap(a,b)

            p._depth = self._depth + 1

            p._parent = self

            return p



        return map(lambda pair: swap_and_copy(zero, pair), space)



    def _generate_solution_path(self, path):

        if self._parent == None:

            return path

        else:

            path.append(self)
            return self._parent._generate_solution_path(path)



    def solve(self, h, sign):

        """Performs search for goal state.
        sign : parameter for choosing different algorithm:
            (1) Uniformcost algorithm
            (2) A* with Misplaced Tile heuristic
            (3) A* with the Manhattan distance heuristic
            
        h(puzzle) - heuristic function, returns an integer
    
        """

        def is_solved(puzzle):

            return puzzle.adj_matrix == _goal_state
            
        # mistile fuc: calculate misplaced tile for current status
        def mistile(puzzle):
            
            mis = 0
            
            for i in range(len(puzzle.adj_matrix)):
                
                if puzzle.adj_matrix[i] != _goal_state[i]:
                    
                    mis +=1
                    
            return mis
        
        def index(item, seq):

            """Helper function that returns -1 for non-found index value of a seq"""

            if item in seq:

                return seq.index(item)

            else:

                return -1

        openl = [self]

        closedl = []

        maxnodes = 0

        move_count = 0

        while len(openl) > 0:

            x = openl.pop(0)

            move_count += 1

            if (is_solved(x)):

                if len(closedl) > 0:

                    return maxnodes,x,x._generate_solution_path([]), move_count

                else:

                    return [x]



            succ = x._generate_moves()

            idx_open = idx_closed = -1

            for move in succ:

                idx_open = index(move, openl)

                idx_closed = index(move, closedl)

                hval = h(move)

                fval = hval + move._depth



                if idx_closed == -1 and idx_open == -1:

                    move._hval = hval

                    openl.append(move)

                elif idx_open > -1:

                    copy = openl[idx_open]

                    if fval < copy._hval + copy._depth:

                        copy._hval = hval

                        copy._parent = move._parent

                        copy._depth = move._depth

                elif idx_closed > -1:

                    copy = closedl[idx_closed]

                    if fval < copy._hval + copy._depth:

                        move._hval = hval

                        closedl.remove(copy)

                        openl.append(move)

            closedl.append(x)
            
            if sign == 1 :  
                openl = sorted(openl, key=lambda p: p._depth)
                print("The best state: f(n)=",int(openl[0]._depth), "is...")
                print(openl[0])
                print("Expanding this node...\n")
            
            if sign == 2 :
                openl = sorted(openl, key=lambda p: mistile(p))
                print("The best state: m(n)=",int(mistile(openl[0])),"is...")
                print(openl[0])
                print("Expanding this node...\n")

            if sign == 3 :
                openl = sorted(openl, key=lambda p: p._hval + p._depth)
                print("The best state: g(n)=",int(openl[0]._depth),"and h(n)=",int(openl[0]._hval),"is...")
                print(openl[0])
                print("Expanding this node...\n")
            maxnodes = max(maxnodes, len(openl))                        
        # if finished state not found, return failure

        return [], 0




    def shuffle(self, step_count):

        for i in range(step_count):

            row, col = self.find(0)

            space = self._get_legal_moves()

            target = random.choice(space)

            self.swap((row, col), target)            

            row, col = target



    def find(self, value):

        """returns the (row, col) of wanted piece"""

        if value < 0 or value > 8:

            raise Exception("value out of range")



        for row in range(3):

            for col in range(3):

                if self.adj_matrix[row][col] == value:

                    return row, col

    

    def peek(self, row, col):

        """returns the value at the specified row and column"""

        return self.adj_matrix[row][col]



    def poke(self, row, col, value):

        """sets the value at the specified row and column"""

        self.adj_matrix[row][col] = value



    def swap(self, pos_a, pos_b):

        """swaps values at the specified coordinates"""

        temp = self.peek(*pos_a)

        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))

        self.poke(pos_b[0], pos_b[1], temp)





def heur(puzzle, item_total_calc, total_calc):

    """

    Heuristic template that provides the current and target position for each number and the 

    total function.

    
    """

    t = 0

    for row in range(3):

        for col in range(3):

            val = puzzle.peek(row, col) - 1

            target_col = val % 3

            target_row = val / 3


            if target_row < 0: 

                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)


def default(puzzle):

    return heur(puzzle,

                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),

                lambda t : t)

def main():

    p = Puzzle()
    puzzletype = input("Welcome Yadan's 8-puzzle solver. (CS170 Oct 25, 2016)\nType 1 to use default \nType 2 to use own \n")
    if int(puzzletype) == 1:
        p.shuffle(70)
    elif int(puzzletype) == 2:
        p.adj_matrix = []
        print("Input your matrix by row (use a zero to represent the blank and use space between numbers)")
        for i in range(3):
            p.adj_matrix.append([int(j) for j in input("input row:").split()])
    else: 
        print("Wrong input : please restart it later :)")
        
    print (p.adj_matrix)
    
    sign = input("Choose algorithm :\n1. Uniform Cost\n2. A* with Misplaced Tile heuristic\n3. A* with Manhattan distance heuristic\n")

    maxnodes, final, path, count = p.solve(default, int(sign))
    path.reverse()
    print("Goal!!\nTo solve this problem the search algorithm expanded", count, "nodes")
    print("The maximum number of nodes in the queue at any one time was", maxnodes)
    print("The depth of the goal node was", final._depth)
    


if __name__ == "__main__":

    main()
