import random
import json
import time
import psutil
import matplotlib.pyplot as plt

def generate_sat_instance(num_variables, num_clauses):
    """Générer une instance SAT aléatoire avec num_variables variables et num_clauses clauses."""
    
    variables = [f'u{i}' for i in range(1, num_variables + 1)]
    
    clauses = []
    for _ in range(num_clauses):
        clause_length = random.randint(2, 5)  # Les clauses peuvent contenir 2 à 5 littéraux
        clause = random.sample(variables, clause_length)
        # Ajout de la négation de manière aléatoire pour chaque littéral
        clause = [f'!{var}' if random.choice([True, False]) else var for var in clause]
        clauses.append(clause)
    
    return {"U": variables, "C": clauses}

def save_sat_instance(filename, num_variables, num_clauses):
    """Enregistrer une instance SAT dans un fichier JSON."""
    instance = generate_sat_instance(num_variables, num_clauses)
    with open(filename, "w") as file:
        json.dump(instance, file, indent=4)
    print(f"Fichier généré : {filename}")

def measure_time_and_memory(func, *args):
    """Mesurer le temps d'exécution et l'utilisation de la mémoire d'une fonction."""
    # Mesurer l'utilisation de la mémoire et du temps avant l'exécution
    process = psutil.Process()
    memory_before = process.memory_info().rss 
    start_time = time.time()

    # Exécution de la fonction
    result = func(*args)

    # Mesurer le temps et la mémoire après l'exécution
    end_time = time.time() 
    memory_after = process.memory_info().rss 

    # Calcul des différences
    execution_time = end_time - start_time
    memory_usage = memory_after - memory_before  # En octets

    return result, execution_time, memory_usage

def generate_multiple_instances_and_analyze():
    """Générer plusieurs fichiers SAT, analyser et enregistrer le temps d'exécution et l'utilisation de la mémoire."""
    sizes = [
        (100, 200),
        (500, 1000),
        (1000, 2000),
        (2000, 4000),
        (5000, 10000)
    ]
    
    times = []
    memory_usages = []
    for num_vars, num_clauses in sizes:
        filename = f"sat_{num_vars}_{num_clauses}.json"
        save_sat_instance(filename, num_vars, num_clauses)

        # Mesurer le temps et la mémoire pour la génération de l'instance SAT
        _, exec_time, mem_usage = measure_time_and_memory(save_sat_instance, filename, num_vars, num_clauses)
        times.append(exec_time)
        memory_usages.append(mem_usage)

    return sizes, times, memory_usages

def plot_performance(sizes, times, memory_usages):
    """Tracer les graphiques de temps d'exécution et d'utilisation de la mémoire."""
    # Extraire le nombre de variables et de clauses
    num_vars = [size[0] for size in sizes]
    num_clauses = [size[1] for size in sizes]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(num_vars, times, marker='o', color='b', label="Temps d'exécution")
    plt.xlabel('Taille')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Temps d\'exécution SAT')
    plt.grid(True)

    
    plt.subplot(1, 2, 2)
    plt.plot(num_vars, memory_usages, marker='o', color='r', label="Utilisation de la mémoire")
    plt.xlabel('Taille')
    plt.ylabel('Utilisation de la mémoire (octets)')
    plt.title('Utilisation de la mémoire SAT')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    sizes, times, memory_usages = generate_multiple_instances_and_analyze()

  
    plot_performance(sizes, times, memory_usages)

if __name__ == '__main__':
    main()
