import json
import sys


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
    
        return self.check_variables() and self.check_clauses()

    def check_variables(self) -> bool:
        """Function to check the correct representation of the variables."""
        print(f"Variables: {self.variables}")
        return len(self.variables) == len(set(self.variables))

    def check_clauses(self) -> bool:
        """Function to check the correct representation of the clauses."""
        print(f"Clauses: {self.clauses}")
        for clause in self.clauses:
            for literal in clause:
                var = literal.lstrip('!')
                if var not in self.variables:
                    print(f"Invalid variable in clause: {literal}")
                    return False
        return True

    def __str__(self) -> str:
        """Function to transform this object into a readable string."""
        return f'U: {{{", ".join(self.variables)}}}\n' + \
               f'C: {{[{"], [".join([", ".join(c) for c in self.clauses])}]}}'


def verify_solution(sat_problem, solution):
    """
    Vérifie si une solution donnée satisfait l'instance SAT.

        Dictionnaire représentant les valeurs des variables (True/False).
    Returns:
    -------
    bool
        True si la solution satisfait l'instance SAT, False sinon.
    """
    for clause in sat_problem.clauses:
        clause_satisfied = False
        for literal in clause:
            var = literal.lstrip('!')
            value = solution.get(var, None)
            if value is None:
                print(f"Erreur : La variable {var} n'est pas définie dans la solution.")
                return False
            if (literal.startswith('!') and not value) or (not literal.startswith('!') and value):
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False  
    return True


def run():
    
    if len(sys.argv) < 2:
        print("Usage: python SAT.py <path_to_json>")
        return

    path = sys.argv[1]
    sat_problem = SAT(path)
    print(sat_problem)

    # Définir une solution à tester
    solution = {
        "u1": True,
        "u2": True
    }

    # Vérifier si cette solution satisfait l'instance
    if verify_solution(sat_problem, solution):
        print("La solution satisfait l'instance SAT.")
    else:
        print("La solution ne satisfait pas l'instance SAT.")


if __name__ == '__main__':
    run()
