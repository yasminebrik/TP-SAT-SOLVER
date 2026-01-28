import random
import json
import time
import psutil
import matplotlib.pyplot as plt

class SAT_3:
    def __init__(self, json_path):
        self.variables = []
        self.clauses = []
        with open(json_path, "r") as file:
            data = json.load(file)
            self.variables = data['U']
            self.clauses = data['C']
        if not self.check_integrity():
            raise ValueError('Error: Wrong representation of SAT_3 problem')

    def check_integrity(self) -> bool:
        return self.check_variables() and self.check_clauses()

    def check_variables(self) -> bool:
        return len(self.variables) == len(set(self.variables))

    def check_clauses(self) -> bool:
        for clause in self.clauses:
            if len(clause) != 3:
                return False
            for literal in clause:
                stripped_literal = literal.lstrip('!').lstrip('-')
                if stripped_literal not in self.variables:
                    return False
        return True

    def is_satisfiable(self):
        def unit_propagation(cnf, assignments):
            while True:
                unit_clauses = [clause for clause in cnf if len(clause) == 1]
                if not unit_clauses:
                    break
                for clause in unit_clauses:
                    literal = clause[0]
                    var = abs(literal)
                    value = literal > 0
                    assignments[self.variables[var - 1]] = value
                    cnf = [
                        [lit for lit in clause if lit != -literal]
                        for clause in cnf if literal not in clause
                    ]
            return cnf

        def solve(cnf, assignments):
            cnf = unit_propagation(cnf, assignments)
            if not cnf: 
                return True
            if any(not clause for clause in cnf):  
                return False

            for clause in cnf:
                for literal in clause:
                    if -literal in clause:
                        return False

            var = abs(next(literal for clause in cnf for literal in clause))
            assignments[var] = True
            if solve([[lit for lit in clause if lit != -var] for clause in cnf if var not in clause], assignments):
                return True

            assignments[var] = False
            return solve([[lit for lit in clause if lit != var] for clause in cnf if -var not in clause], assignments)

        variable_map = {f"u{i+1}": i+1 for i in range(len(self.variables))}
        cnf = []
        for clause in self.clauses:
            cnf_clause = []
            for literal in clause:
                if literal.startswith('!'):
                    var = literal[1:]
                    cnf_clause.append(-variable_map[var])
                else:
                    var = literal
                    cnf_clause.append(variable_map[var])
            cnf.append(cnf_clause)

        assignments = {var: None for var in self.variables}
        return solve(cnf, assignments)

def generate_sat_3_instance(num_variables, num_clauses):
    variables = [f'u{i}' for i in range(1, num_variables + 1)]
    clauses = []
    for _ in range(num_clauses):
        clause = random.sample(variables, 3)
        clause = [f'!{var}' if random.choice([True, False]) else var for var in clause]
        clauses.append(clause)
    return {"U": variables, "C": clauses}

def save_sat_3_instance(filename, num_variables, num_clauses):
    instance = generate_sat_3_instance(num_variables, num_clauses)
    with open(filename, "w") as file:
        json.dump(instance, file, indent=4)

def measure_time_and_memory(func, *args):
    process = psutil.Process()
    memory_before = process.memory_info().rss
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    memory_after = process.memory_info().rss
    execution_time = end_time - start_time
    memory_usage = memory_after - memory_before
    return result, execution_time, memory_usage

def generate_multiple_instances_and_analyze():
    sizes = [
        (10, 20),
        (50, 100),
        (100, 200),
        (200, 400),
        (500, 1000)
    ]
    
    times = []
    memory_usages = []
    for num_vars, num_clauses in sizes:
        filename = f"sat_3_{num_vars}_{num_clauses}.json"
        save_sat_3_instance(filename, num_vars, num_clauses)

   
        sat_problem = SAT_3(filename)
        _, exec_time, mem_usage = measure_time_and_memory(sat_problem.is_satisfiable)
        times.append(exec_time)
        memory_usages.append(mem_usage)

    return sizes, times, memory_usages

def plot_performance(sizes, times, memory_usages):
    num_vars = [size[0] for size in sizes]
    num_clauses = [size[1] for size in sizes]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(num_vars, times, marker='o', color='b', label="Temps d'exécution")
    plt.xlabel('Taille')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Temps d\'exécution 3SAT ')
    plt.grid(True)
    

    plt.subplot(1, 2, 2)
    plt.plot(num_vars, memory_usages, marker='o', color='r', label="Utilisation de la mémoire")
    plt.xlabel('Taille')
    plt.ylabel('Utilisation de la mémoire (octets)')
    plt.title('Utilisation de la mémoire 3SAT ')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    sizes, times, memory_usages = generate_multiple_instances_and_analyze()
    plot_performance(sizes, times, memory_usages)

if __name__ == '__main__':
    main()
