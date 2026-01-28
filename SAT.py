import json
import sys

assignments = {}
n_props = 0
n_splits = 0

class SAT:
   

    def __init__(self, json_path):
       
        
        self.variables = []
        self.clauses = []

        with open(json_path, "r") as file:
            data = json.load(file)
            self.variables = data['U']
            self.clauses = data['C']

        if not self.check_integrity():
            raise ValueError('Error: Wrong representation of SAT problem')

    def check_integrity(self) -> bool:
        '''Function to check the correct representation of the SAT problem.'''
        return self.check_variables() and self.check_clauses()

    def check_variables(self) -> bool:
        '''Function to check the correct representation of the variables.'''
        print(f"Variables: {self.variables}")
        # Remove the 'u' prefix from the variables for validation
        self.variables = [var.lstrip('u') for var in self.variables]
        return len(self.variables) == len(set(self.variables))

    def check_clauses(self) -> bool:
        '''Function to check the correct representation of the clauses.'''
        print(f"Clauses: {self.clauses}")
        for clause in self.clauses:
            for literal in clause:
              
                var = literal.lstrip('!').lstrip('u')
                if var not in self.variables:
                    print(f"Invalid variable in clause: {literal}")
                    return False
        return True

    def __str__(self) -> str:
        '''Function to transform this object into a readable string.'''
        return f'U: {{{", ".join(self.variables)}}}\n' + \
               f'C: {{[{"], [".join([", ".join(c) for c in self.clauses])}]}}'


def is_satisfiable(cnf):
    """Check if the CNF formula is satisfiable and return a solution."""
    global assignments, n_props, n_splits
    assignments = {}
    n_props = 0
    n_splits = 0

    def unit_propagation(cnf):
        """Apply unit propagation on the CNF."""
        global assignments, n_props
        while True:
            unit_clauses = [clause for clause in cnf if len(clause) == 1]
            if not unit_clauses:
                break
            for clause in unit_clauses:
                literal = clause[0]
                n_props += 1
                var = abs(literal)
                value = literal > 0
                assignments[var] = value
                cnf = [
                    [lit for lit in clause if lit != -literal]
                    for clause in cnf if literal not in clause
                ]
        return cnf

    def solve(cnf):
        """Solve the CNF recursively using a divide-and-conquer approach."""
        global assignments, n_splits
        cnf = unit_propagation(cnf)
        if not cnf:  # All clauses are satisfied
            return True, assignments
        if any(not clause for clause in cnf):  # Empty clause found
            return False, {}

        # Choose a variable to split on (heuristic: take the first variable in the CNF)
        var = abs(next(literal for clause in cnf for literal in clause))
        n_splits += 1

        # Try with var = True
        backup = assignments.copy()
        assignments[var] = True
        sat, solution = solve([[lit for lit in clause if lit != -var] for clause in cnf if var not in clause])
        if sat:
            return True, solution
        assignments = backup  # Restore if it fails

        # Try with var = False
        assignments[var] = False
        return solve([[lit for lit in clause if lit != var] for clause in cnf if -var not in clause])

    # Convert CNF to a list of integers
    cnf = [[(int(literal[1:]) if literal[0] == 'u' else -int(literal[2:])) for literal in clause] for clause in cnf]
    return solve(cnf)


def run():
    if len(sys.argv) < 2:
        print("Usage: python SAT.py <path_to_json>")
        return

    path = sys.argv[1]
    sat_problem = SAT(path)
    print(sat_problem)

    satisfiable, solution = is_satisfiable(sat_problem.clauses)
    if satisfiable:
        print("Oui, la formule est satisfaisable.")
        print("Affectations trouvées :")
        for var, value in solution.items():
            print(f"u{var} = {'vrai' if value else 'faux'}")
        print(f"Nombre de propagations unitaires : {n_props}")
        print(f"Nombre de splits : {n_splits}")
    else:
        print("Non, la formule n'est pas satisfaisable.")


if __name__ == '__main__':
    run()
