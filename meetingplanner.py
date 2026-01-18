from ortools.linear_solver import pywraplp

# Return a smallest list of meeting times so that every person
# can attend at least one meeting. a is a matrix where the
# rows are meeting times, the columns are people, and
# a[i][j] = 1 if meeting i can be attended by person j, and
# a[i][j] = 0 otherwise. If there is no list of meetings which
# can accommodate everyone, return an empty list.
def minimize_meetings(a):

    # Create a SCIP integer program solver
    solver = pywraplp.Solver.CreateSolver("SCIP")

    m = len(a)    # number of meetings
    n = len(a[0]) # number of people

    # x[i] = 1 if meeting i is chosen, 0 otherwise
    x = [solver.IntVar(0, 1, "x"+str(i)) for i in range(m)]

    # Objective function
    solver.Minimize(solver.Sum(x[i] for i in range(m)))

    # Constraints
    for j in range(n):
        solver.Add(solver.Sum(a[i][j]*x[i] for i in range(m)) >= 1)

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        meeting_times = [i for i in range(m) if x[i].solution_value() == 1]
    else:
        meeting_times = []

    return meeting_times # This should be a list of times.



# Return a list of k meeting times which maximizes the number
# of people who can attend at least one meeting. a is the
# same as above.
def maximize_attendance(a, k):          

    solver = pywraplp.Solver.CreateSolver("SCIP")

    m = len(a)
    n = len(a[0])

    # x[i] = 1 if meeting i is chosen, 0 otherwise
    x = [solver.IntVar(0, 1, "x"+str(i)) for i in range(m)]

    # y[j] = 1 if person i is covered, 0 otherwise
    y = [solver.IntVar(0, 1, "y"+str(j)) for j in range(n)]

    # Objective function
    solver.Maximize(solver.Sum(y[j] for j in range(n)))

    # Constraints
    for j in range(n):
        solver.Add(solver.Sum(a[i][j]*x[i] for i in range(m)) - y[j] >= 0)        
    solver.Add(solver.Sum(x[i] for i in range(m)) == k)

    # Solve
    status = solver.Solve()

    meeting_times = [i for i in range(m) if x[i].solution_value() == 1]

    return meeting_times # This should be a list of k times.
        
