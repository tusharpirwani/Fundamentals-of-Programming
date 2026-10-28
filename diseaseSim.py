# 
# diseaseSim.py - simulates the spread of disease through a population
#
# Student Name   : Tushar Pirwani
# Student Number : 22464293
#
# Version history:
#
# 28/10/24 - beta version released for FOP assignment
#
import numpy as np
import matplotlib.pyplot as plt
import random

def get_neighbours(r, c, num_r, num_c, neighbourhood_type= "moore"):
    neighbours = []
    if neighbourhood_type== "moore":
        for dr in [-1, 0, 1]:      # the loop iterates over dr, dc with given values, represing relative changes in row and column indicies
            for dc in [-1, 0, 1]:
                if not (dr == 0 and dc == 0):   # excludes the cell itself
                    nr, nc = r + dr, c + dc        # creates new coordinates nr,nc for each valid direction
                    if 0 <= nr < num_r and 0 <= nc < num_c:     # if nr, nc meet this condition(lie in the grid boundary and not execde it)
                        neighbours.append((nr, nc))   # then they get added to the neighbours list
    elif neighbourhood_type== "von Neumann":
        for dr, dc in [(-1,0), (1, 0), (0, -1), (0, 1)]:     # the loop iterates here for four possible coordinates
            nr, nc = r + dr, c + dc
            if 0 <= nr < num_r and 0 <= nc < num_c:
                neighbours.append((nr, nc))
    return neighbours 

def distribute(grid, num_r, num_c, numpeep):  # it ensures that each individual is randomly placed in a cell on the grid, increasing the value of that cell by 1 each time a new individual is placed.
    for i in range(numpeep):
        rpos = random.randint(0, num_r-1) # generates a random integer between 0 and num_r-1 (inclusive) to select a random row
        cpos = random.randint(0, num_c-1) # generates a random integer between 0 and num_c-1 (inclusive) to select a random column
        grid[rpos, cpos] += 1 # Increments the value at the chosen cell by 1

def makeScatter(grid, num_r, num_c, status_map):
    r_values = []
    c_values = []
    count_values = []
    colors = []
    # Loop through each cell in the grid
    for row in range(num_r):   # Iterate over rows  
        for col in range(num_c):  # Iterate over columns
            if grid[row, col] > 0: # If the cell contains one or more individuals
                r_values.append(row) # Add the row index to r_values list
                c_values.append(col)  # Add the column index to c_values list
                count_values.append(grid[row, col] * 100)  # Add the scaled(for visualization) number of individuals to count_values
                # Add the color based on the status of the cell (infected, recovered, etc.)
                colors.append(status_map[(row, col)]) # status_map(dictionary) provides the status (color) for each (row, col)
   # Return the data for the scatter plot: row indices, column indices, scaled count values, and colors
    return r_values, c_values, count_values, colors

    
def displayGrid(grid, num_r, num_c):
    for row in range(num_r-1, -1, -1):  # Iterate over each row starting from the last row (num_r-1) to the first row (0)
        for col in range(num_c):        # Iterate over each column in the current row
            print(grid[row,col], end=" ") # Print the value at grid[row, col] with a space(instead of a new line) after it (to separate columns)
        print()  # After printing all columns in the current row, move to the next line (start new row)


def plotGrids(infected, uninfected, recovered, deceased, airports, barriers, NUM_ROWS, NUM_COLS, timestep):
    plt.figure(figsize=(20,20))  # Set the figure size for the plot

    # Initialize status map for color coding each cell (initially all uninfected 'b')
    status_map = {(r, c): 'b' for r in range(NUM_ROWS) for c in range(NUM_COLS)}  # Default 'b' for uninfected

    # Plot Infected individuals (Red color)
    Irows, Icols, Icount, _ = makeScatter(infected, NUM_ROWS, NUM_COLS, status_map)  # Get the scatter data for infected from makeScatter function
    for i in range(len(Irows)):  # Manual iteration over Irows and Icols to update status_map
        r = Irows[i]  # Row index of infected individual
        c = Icols[i]  # Column index of infected individual
        status_map[(r, c)] = 'r'  # Update the status_map to mark this cell as 'r' (red - infected)
    plt.scatter(Icols, Irows, s=Icount, c='r', alpha=0.5, label="Infected")  # Scatter plot for infected individuals

    # Plot Uninfected individuals (Blue color)
    Urows, Ucols, Ucount, _ = makeScatter(uninfected, NUM_ROWS, NUM_COLS, status_map)  # Get the scatter data for uninfected
    for i in range(len(Urows)):  # Manual iteration over Urows and Ucols to update status_map
        r = Urows[i]  # Row index of uninfected individual
        c = Ucols[i]  # Column index of uninfected individual
        status_map[(r, c)] = 'b'  # Update the status_map to mark this cell as 'b' (blue - uninfected)
    plt.scatter(Ucols, Urows, s=Ucount, c='b', alpha=0.5, label="Uninfected")  # Scatter plot for uninfected individuals

    # Plot Recovered individuals (Green color)
    Rrows, Rcols, Rcount, _ = makeScatter(recovered, NUM_ROWS, NUM_COLS, status_map)  # Get the scatter data for recovered
    for i in range(len(Rrows)):  # Manual iteration over Rrows and Rcols to update status_map
        r = Rrows[i]  # Row index of recovered individual
        c = Rcols[i]  # Column index of recovered individual
        status_map[(r, c)] = 'g'  # Update the status_map to mark this cell as 'g' (green - recovered)
    plt.scatter(Rcols, Rrows, s=Rcount, c='g', alpha=0.5, label="Recovered")  # Scatter plot for recovered individuals

    # Plot Deceased individuals (Gray color)
    Drows, Dcols, Dcount, _ = makeScatter(deceased, NUM_ROWS, NUM_COLS, status_map)  # Get the scatter data for deceased
    for i in range(len(Drows)):  # Manual iteration over Drows and Dcols to update status_map
        r = Drows[i]  # Row index of deceased individual
        c = Dcols[i]  # Column index of deceased individual
        status_map[(r, c)] = 'k'  # Update the status_map to mark this cell as 'k' (black - deceased)
    plt.scatter(Dcols, Drows, s=Dcount, c='k', alpha=0.5, label="Deceased")  # Scatter plot for deceased individuals

    # Plot Airports (Yellow color, star-shaped markers)
    Arows = []  # List to hold row coordinates for airports
    Acols = []  # List to hold column coordinates for airports
    for airport in airports:  # Iterate over the airports list to extract coordinates
        Arows.append(airport[0])  # Add row coordinate for airport
        Acols.append(airport[1])  # Add column coordinate for airport
    plt.scatter(Acols, Arows, s=200, c='y', marker='*', label="Airports")  # Scatter plot for airports (yellow stars)

    # Plot Barriers (Black color, X-shaped markers)
    Brows = []  # List to hold row coordinates for barriers
    Bcols = []  # List to hold column coordinates for barriers
    for barrier in barriers:  # Iterate over the barriers list to extract coordinates
        Brows.append(barrier[0])  # Add row coordinate for barrier
        Bcols.append(barrier[1])  # Add column coordinate for barrier
    plt.scatter(Bcols, Brows, s=500, c='black', marker='X', label="Barriers")  # Scatter plot for barriers (black Xs)

    # Add a legend to label each type of data (infected, uninfected, recovered, etc.)
    plt.legend()
    plt.title(f"Time Step: {timestep}")
    plt.show()
          
def movePeeps(cur, next, r, c, NUM_ROWS, NUM_COLS, barriers):
    
    # Loop through each individual(peep) in the current cell
    for peep in range(cur[r,c]):  
        
        # Generate random movement for the individual
        rMove = random.randint(-1,1)  # Random row movement (-1, 0, or 1)
        cMove = random.randint(-1,1)   # Random column movement (-1, 0, or 1)
        
        # Calculate the target cell coordinates after movement
        target_r = r + rMove
        target_c = c + cMove
        
        # Check if the target cell is within grid boundaries and not a barrier
        if (0 <= target_r < NUM_ROWS and 0 <= target_c < NUM_COLS and
            (target_r, target_c) not in barriers):
            # Move the individual to the target cell
            next[target_r, target_c] += 1
            
        else:
            # If movement is invalid (out of bounds or into a barrier), keep the individual in the current cell
            next[r, c] += 1
    
def infect(inf, notinf, r, c, prob):
    
    # Scale the infection probability by the number of infected individuals in the cell
    prob = prob * inf[r,c] 
    
    # Proceed only if the scaled probability is greater than 0
    if prob:
        # Iterate through each uninfected individual in the current cell
        for peep in range(notinf[r,c]):
            # Generate a random value and compare it to the infection probability
            if random.random() < prob:
                inf[r, c] +=1      # Increase the count of infected individuals in the cell
                notinf[r, c] -=1   # decrease the count of uninfected individuals in the cell
                
def recover_and_die(infected, recovered, deceased, immunity, death_prob, recovery_prob, r, c):
    
    # Iterate through all infected individuals in the given cell
    for i in range(infected[r, c]):
        
        # Generate a random number to determine if the individual dies
        if random.random() < death_prob:
            deceased[r, c] += 1  # Increment the count of deceased individuals in this cell
            infected[r, c] -= 1  # Decrement the count of infected individuals in this cell
            
        # If the individual does not die, generate another random number for recovery
        elif random.random() < recovery_prob:
            recovered[r, c] += 1  # Increment the count of recovered individuals in this cell
            infected[r, c] -= 1  # Decrement the count of infected individuals in this cell
            immunity[r, c] = 1  # Mark the cell as immune since recovery confers immunity
            
def setup_airports_and_barriers(NUM_ROWS, NUM_COLS, num_airports, num_barriers):
    airports = [] # Initialize an empty list to store airport positions
    barriers = [] # Initialize an empty list to store barrier positions
    
    for _ in range(num_airports):  # Loop to place the specified number of airports
        r, c = random.randint(0, NUM_ROWS-1), random.randint(0, NUM_COLS-1) # Generate a random row and column
        airports.append((r, c)) # Append the airport coordinates as a tuple
        
    for _ in range(num_barriers): # Loop to place the specified number of barriers
        r, c = random.randint(0, NUM_ROWS-1), random.randint(0, NUM_COLS-1) # Generate a random row and column
        barriers.append((r, c)) # Append the barrier coordinates as a tuple

    return airports, barriers


def get_neighbourhood_type():
    neighbourhood_type = input("Choose neighbourhood type (moore or von Neumann): ").strip().lower()
    if neighbourhood_type == "moore" or neighbourhood_type == "von neumann":
        return neighbourhood_type
    else:
        print("Invalid input. Please enter 'moore' or 'von Neumann'.")
        return None
    
def get_simulation_parameters():
    NUM_ROWS = input("Enter number of rows for the grid (positive integer): ")
    NUM_COLS = input("Enter number of columns for the grid (positive integer): ")
    NUM_STEPS = input("Enter number of steps for the simulation (positive integer): ")
    INIT_POP = input("Enter initial population (non-negative integer): ")
    INIT_INFECTED = input("Enter initial infected population (non-negative integer): ")

    # Validation
    # converting inputs from strings to integars
    try:
        NUM_ROWS = int(NUM_ROWS)
        NUM_COLS = int(NUM_COLS)
        NUM_STEPS = int(NUM_STEPS)
        INIT_POP = int(INIT_POP)
        INIT_INFECTED = int(INIT_INFECTED)
        
        if NUM_ROWS <= 0 or NUM_COLS <= 0 or NUM_STEPS <= 0 or INIT_POP < 0 or INIT_INFECTED < 0:
            print("All values must be positive integers.")
            return None
        
        if INIT_INFECTED > INIT_POP:
            print("Initial infected population cannot exceed the initial population per cell.")
            return None
        
        return NUM_ROWS, NUM_COLS, NUM_STEPS, INIT_POP, INIT_INFECTED
    except ValueError:
        print("Invalid input. Please enter integers for all fields.")
        return None

def print_final_stats(infected, uninfected, recovered, deceased, NUM_ROWS, NUM_COLS):
    # Final Stats
    # Calculate total number of individuals in each state (infected, uninfected, recovered, deceased)
    total_infected = np.sum(infected) # Sum all infected individuals across the grid
    total_uninfected = np.sum(uninfected) # Sum all uninfected individuals across the grid
    total_recovered = np.sum(recovered) # Sum all recovered individuals across the grid
    total_deceased = np.sum(deceased) # Sum all deceased individuals across the grid

    print(f"Simulation complete! Final statistics:")
    print(f"Total Infected: {total_infected}")
    print(f"Total Uninfected: {total_uninfected}")
    print(f"Total Recovered: {total_recovered}")
    print(f"Total Deceased: {total_deceased}")
    print(f"Grid Size: {NUM_ROWS} rows by {NUM_COLS} columns")
    print(f"Total Population: {total_infected + total_uninfected + total_recovered + total_deceased}")
    

def simulate(NUM_ROWS, NUM_COLS, NUM_STEPS, INIT_POP, INIT_INFECTED, neighbourhood_type="moore"):
    # Initialize the grids to track the state of each cell in the simulation
    infected = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # Tracks infected individuals
    uninfected = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # Tracks uninfected individuals
    recovered = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # Tracks recovered individuals
    deceased = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # Tracks deceased individuals
    immunity = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # Tracks immunity after recovery

    # Distribute initial populations (infected and uninfected) across the grid
    distribute(infected, NUM_ROWS, NUM_COLS, INIT_INFECTED) # Distribute the initial infected individuals
    distribute(uninfected, NUM_ROWS, NUM_COLS, INIT_POP) # Distribute the initial uninfected population

    # Set up airports and barriers (to restrict movement)
    airports, barriers = setup_airports_and_barriers(NUM_ROWS, NUM_COLS, 3, 5)

    # Loop through each timestep in the simulation
    for timestep in range(NUM_STEPS):
        # Create temporary grids for updated values after each timestep
        infected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=int) # Temporary grid for updated infected individuals
        uninfected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=int) # Temporary grid for updated uninfected individuals

        # Loop through each cell in the grid (representing people)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # If the cell is infected, attempt to infect neighboring uninfected cells
                if infected[row, col] > 0:
                    infect(infected, uninfected, row, col, 0.1)  # the function infect() is called to spread the infection to neighboring cells(10% chance).

                # Move infected and uninfected people based on the neighbourhood type and avoid barriers
                movePeeps(infected, infected2, row, col, NUM_ROWS, NUM_COLS, barriers) # Move infected people
                movePeeps(uninfected, uninfected2, row, col, NUM_ROWS, NUM_COLS, barriers) # Move uninfected people

                # Apply recovery or death processes based on probabilities
                recover_and_die(infected, recovered, deceased, immunity, 0.05, 0.1, row, col)  # 5% recovery, 10% death rate

        # After processing all cells in the grid, plot the state of the simulation
        plotGrids(infected, uninfected, recovered, deceased, airports, barriers, NUM_ROWS, NUM_COLS, timestep)

        # Update the infected and uninfected grids for the next timestep
        infected = infected2.copy() # Copy the updated infected grid (to prevent modifying the current grid)
        uninfected = uninfected2.copy() # Copy the updated uninfected grid (to prevent modifying the current grid)

    # After completing all timesteps, print the final statistics of the simulation
    print_final_stats(infected, uninfected, recovered, deceased, NUM_ROWS, NUM_COLS)


# Main Program
# Get simulation parameters from the user
parameters = get_simulation_parameters()
if parameters:
    NUM_ROWS, NUM_COLS, NUM_STEPS, INIT_POP, INIT_INFECTED = parameters
    # Get the neighbourhood type (Moore or Von Neumann)
    neighbourhood_type = get_neighbourhood_type()
    if neighbourhood_type:
        # Start the simulation with the given parameters
        simulate(NUM_ROWS, NUM_COLS, NUM_STEPS, INIT_POP, INIT_INFECTED, neighbourhood_type) 

