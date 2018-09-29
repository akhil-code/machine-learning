import numpy as np
import matplotlib.pyplot as plt
from numpy import random

class Individual:
    def __init__(self, numbers=None, mutate_prob=0.01,minv=0,maxv=100):
        if numbers is None:
            self.numbers = random.randint(minv,high=maxv+1,size=10)
        else:
            self.numbers = numbers
            if mutate_prob > random.rand():
                mutate_index = random.randint(0,high=len(self.numbers))
                self.numbers[mutate_index] = random.randint(0, high=maxv+1)

    def get_fitness(self, target=900):
        individual_sum = sum(self.numbers)
        return abs(target - individual_sum)

class Population:
    def __init__(self, pop_size=10, retain=0.2, mutate_prob=0.01, retain_prob=0.03):
        self.parents = []
        self.pop_size = pop_size
        self.done = False
        self.generation = 1
        self.mutate_prob = mutate_prob
        self.retain_prob = retain_prob
        self.retain = retain
        self.fitness_history = []

        self.individuals = [Individual(mutate_prob=mutate_prob) for i in range(pop_size)]
    
    def grade(self):
        fitness_sum = 0
        for individual in self.individuals:
            fitness_sum += individual.get_fitness()
        
        pop_fitness = fitness_sum / self.pop_size
        self.fitness_history.append(pop_fitness)

        if pop_fitness == 0:
            self.done = True
        
        if self.generation % 5 == 0:
            print(f"generation: {self.generation}, fitness: {pop_fitness}")

    def select_parents(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.get_fitness())
        retain_length = int(self.retain * len(self.individuals))
        self.parents = self.individuals[:retain_length]
        
        unfittest = self.individuals[retain_length:]
        for individual in unfittest:
            if self.retain_prob > random.rand():
                self.parents.append(individual)

    def breed(self):
        target_children_size = self.pop_size - len(self.parents)
        children = []
        if len(self.parents) > 0:
            while len(children) < target_children_size:
                father = random.choice(self.parents)
                mother = random.choice(self.parents)
                if(father != mother):
                    child_numbers = [random.choice(pair) for pair in zip(father.numbers, mother.numbers)]
                    child = Individual(child_numbers)
                    children.append(child)
            self.individuals = self.parents + children

    
    def evolve(self):
        self.select_parents()
        self.breed()
        self.parents = []
        self.generation += 1
    
    def display_population(self):
        for individual in self.individuals:
            print(f"{individual.numbers} -> sum = {sum(individual.numbers)}")
    


if __name__ == "__main__":
    GENERATIONS = 50000
    population = Population(pop_size=10)

    for generation in range(GENERATIONS):
        population.grade()
        population.evolve()

        if population.done:
            population.display_population()
            break
    
    plt.plot(np.arange(len(population.fitness_history)), population.fitness_history)
    plt.xlabel('generations')
    plt.ylabel('fitness')
    plt.show()
    
    
