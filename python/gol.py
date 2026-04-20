import random
import numpy as np


def init_grid(w, h):

    grid = np.zeros((w, h))
    return grid
       

def render_grid(grid):
    for k in range(len(grid)):
        print(grid[k])
    print("")


def add_ones(grid, cord: list): # cor = [ (1,2), (3,3) ]
    for tuple in cord:
        x = tuple[0]
        y = tuple[1]
        grid[x][y] = 1

def gen_random(n, count):
    cord = []
    for i in range(count):
        cord.append((random.randint(0, n-1), random.randint(0, n-1)))
    return cord



# add diagonals to rules
def apply_rule(grid):
    buffer = [row[:] for row in grid]
    n = len(grid) 

    for i in range(n):
        for j in range(n):
            count = 0

            # if celling
            if i == 0:
                # if left corner 
                if j == 0:
                    right_neigh = grid[i][j+1]
                    down_neigh = grid[i+1][j]
                    down_right_diag = grid[i+1][j+1]

                    count += 1 if right_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if down_right_diag == 1 else 0


                # if right corner
                elif j == (n - 1):
                    left_neigh = grid[i][j-1]
                    down_neigh = grid[i+1][j]
                    down_left_diag = grid[i+1][j-1]

                    count += 1 if left_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if down_left_diag == 1 else 0

                # if celling interior
                else:
                    left_neigh = grid[i][j-1]
                    right_neigh = grid[i][j+1]
                    down_neigh = grid[i+1][j]
                    down_right_diag = grid[i+1][j+1]
                    down_left_diag = grid[i+1][j-1]

                    count += 1 if left_neigh == 1 else 0
                    count += 1 if right_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if down_right_diag == 1 else 0
                    count += 1 if down_left_diag == 1 else 0

            
            
            # if floor
            elif i == (n - 1):
                # if left corner
                if j == 0:
                    right_neigh = grid[i][j+1]
                    up_neigh = grid[i-1][j]
                    up_right_diag = grid[i-1][j+1]

                    count += 1 if right_neigh == 1 else 0
                    count += 1 if up_neigh == 1 else 0
                    count += 1 if up_right_diag == 1 else 0

                # if right corner
                elif j == (n - 1):
                    left_neigh = grid[i][j-1]
                    up_neigh = grid[i-1][j]
                    up_left_diag = grid[i-1][j-1]
                
                    count += 1 if left_neigh == 1 else 0
                    count += 1 if up_neigh == 1 else 0
                    count += 1 if up_left_diag == 1 else 0

                # if floor interior
                else:       
                    left_neigh = grid[i][j-1]
                    right_neigh = grid[i][j+1]
                    up_neigh = grid[i-1][j]
                    up_right_diag = grid[i-1][j+1]
                    up_left_diag = grid[i-1][j-1]

                    count += 1 if left_neigh == 1 else 0
                    count += 1 if right_neigh == 1 else 0
                    count += 1 if up_neigh == 1 else 0
                    count += 1 if up_right_diag == 1 else 0
                    count += 1 if up_left_diag == 1 else 0



            else:   
                # if left wall
                if j == 0:
                    up_neigh = grid[i-1][j]
                    down_neigh = grid[i+1][j]
                    right_neigh = grid[i][j+1]
                    up_right_diag = grid[i-1][j+1]
                    down_right_diag = grid[i+1][j+1]

                    count += 1 if up_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if right_neigh == 1 else 0
                    count += 1 if up_right_diag == 1 else 0
                    count += 1 if down_right_diag == 1 else 0


                # if right wall 
                elif j == (n - 1):
                    up_neigh = grid[i-1][j]
                    down_neigh = grid[i+1][j]
                    left_neigh = grid[i][j-1]
                    up_left_diag = grid[i-1][j-1]
                    down_left_diag = grid[i+1][j-1]

                    count += 1 if up_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if left_neigh == 1 else 0
                    count += 1 if up_left_diag == 1 else 0
                    count += 1 if down_left_diag == 1 else 0


                # if interior
                else:
                    up_neigh = grid[i-1][j]
                    down_neigh = grid[i+1][j]
                    left_neigh = grid[i][j-1]
                    right_neigh = grid[i][j+1]
                    
                    up_right_diag = grid[i-1][j+1]
                    down_right_diag = grid[i+1][j+1]
                    down_left_diag = grid[i+1][j-1]
                    up_left_diag = grid[i-1][j-1]

                    count += 1 if up_neigh == 1 else 0
                    count += 1 if down_neigh == 1 else 0
                    count += 1 if left_neigh == 1 else 0
                    count += 1 if right_neigh == 1 else 0  
                    
                    count += 1 if up_right_diag == 1 else 0  
                    count += 1 if down_right_diag == 1 else 0  
                    count += 1 if down_left_diag == 1 else 0  
                    count += 1 if up_left_diag == 1 else 0  

                     
                     

            # apply rule
            if grid[i][j] == 0 and count == 3: 
                buffer[i][j] = 1

            elif grid[i][j] == 1 and (count == 2 or count == 3): 
                buffer[i][j] = 1

            else: 
                buffer[i][j] = 0
                    

    for i in range(n):
        grid[i] = buffer[i]






def game_of_life(w, h, cordinates, it):

    grid = init_grid(w, h)
    add_ones(grid, cordinates)
    
    i = 0
    while i < it:
        render_grid(grid)
        apply_rule(grid)
        i += 1






