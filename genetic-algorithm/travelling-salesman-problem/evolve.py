import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from numpy import random
import time


def get_graph():
    g = np.ones((7,7), dtype=np.int64)*np.inf

    edges = (
        (1, 2, 12),
        (2, 4, 12),
        (1, 3, 10),
        (2, 3, 8),
        (3, 4, 11),
        (1, 7, 12),
        (3, 7, 9),
        (3, 5, 3),
        (4, 5, 11),
        (5, 7, 7),
        (7, 6, 9),
        (5, 6, 6),
        (4, 6, 10),
    )

    for v1,v2,dist in edges:
        g[v1-1][v2-1] = g[v2-1][v1-1] = dist
    return g

class Individual:
    graph = get_graph()
    no_of_nodes = graph.shape[0]

    def __init__(self, individual=None, mutation_prob=0.03):
        if individual is None:
            self.path = np.arange(self.no_of_nodes)
            random.shuffle(self.path[1:])
        else:
            i, j = random.randint(1, high=self.no_of_nodes), random.randint(1, high=self.no_of_nodes)
            if mutation_prob > random.rand():
                individual[i], individual[j] = individual[j], individual[i]
            self.path = individual


    def get_fitness(self):
        fitness = 0
        for i in range(self.no_of_nodes-1):
            fitness += self.graph[self.path[i]][self.path[i+1]]
        return fitness

class Population:
    def __init__(self, pop_size=10, retain=0.2, mutation_prob=0.03, retain_prob=0.03):
        self.pop_size = pop_size
        self.fitness_history = []
        self.pop_size = pop_size
        self.retain = retain
        self.mutation_prob = mutation_prob
        self.retain_prob = retain_prob
        self.generation = 1
        self.no_of_nodes = 7

        self.individuals = [Individual() for i in range(self.pop_size)]
    
    def grade(self):
        self.pop_fitness = min([i.get_fitness() for i in self.individuals])
        self.fitness_history.append(self.pop_fitness)

        
    
    def select_parents(self):
        retain_length = int(self.retain * self.pop_size)
        self.individuals = sorted(self.individuals, key=lambda x: x.get_fitness())
        self.parents = self.individuals[:retain_length]

        unfittest = self.individuals[retain_length:]
        for individual in unfittest:
            if self.retain_prob > random.rand():
                print(f"selected: {individual.path}")
                self.parents.append(individual)
    
    def crossover(self, path1, path2):
        path = [path1[0]] + [random.choice(pair) for pair in zip(path1[1:], path2[1:])]
        path_contains = set(path)
        all_nodes = set(np.arange(self.no_of_nodes))
        path_doesnot_contains = all_nodes.difference(path_contains)

        used = [False for i in range(self.no_of_nodes)]
        for i in range(self.no_of_nodes):
            if used[path[i]] == False:
                used[path[i]] = True
            else:
                if path1[i] in path_doesnot_contains:
                    path[i] = path1[i]
                elif path2[i] in path_doesnot_contains:
                    path[i] = path2[i]
                else:
                    path[i] = random.choice(list(path_doesnot_contains))

                path_doesnot_contains.remove(path[i])
        return path

    def breed(self):
        target_children_size = self.pop_size - len(self.parents)
        children = []

        if len(self.parents) > 0:
            while len(children) < target_children_size:
                father = self.parents[random.randint(len(self.parents))]
                mother = self.parents[random.randint(len(self.parents))]
                if father != mother:
                    child_path = self.crossover(father.path, mother.path)
                    child = Individual(individual=child_path, mutation_prob=self.mutation_prob)
                    # print(f"generation:{self.generation} -> father:{father.path}    mother:{mother.path}    child:{child.path}")
                    # time.sleep(0.01)
                    children.append(child)
            
            self.individuals = self.parents + children

    def evolve(self,info_after_generations=50):
        self.grade()
        self.select_parents()
        self.breed()

        if self.generation % info_after_generations == 0:
            print(f"generation:{self.generation}  -> fitness: {self.pop_fitness}")

        self.parents = []
        self.generation += 1
    
    def show_population(self):
        for individual in self.individuals:
            print(f"ind: {individual}  -> fitness: {individual.get_fitness()}")


if __name__== '__main__':
    GENERATIONS = 1000000
    SHOW_GRAPH = True

    population = Population(pop_size=10, mutation_prob=0.05)
    for i in range(GENERATIONS):
        population.evolve(info_after_generations=20)
    
    optimal_path = population.individuals[0].path
    print(optimal_path)
    
    plt.plot(np.arange(len(population.fitness_history)), population.fitness_history)
    plt.xlabel('generations')
    plt.ylabel('fitness')
    plt.title('Travelling salesman problem')
    plt.show()

