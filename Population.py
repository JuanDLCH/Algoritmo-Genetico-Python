from typing import List
from Individual import *
import math as mt
from operaciones import *
from prettytable import PrettyTable

class Poblacion:
    def __init__(self, crossover_probability, mutation_probability, max_generations):
        #Const
        self.population_size = 100
        self.fx_lower_bound = -20
        self.fx_upper_bound = 20
        self.precision = 3
        self.chromosome_lenght = mt.ceil(mt.log2((self.fx_upper_bound - self.fx_lower_bound) * pow(10, self.precision)))
        #Variab
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.max_generations = max_generations
        self.parents = list()
        self.offspring = list()
        self.parents : List[Individual]
        self.offspring : List[Individual]
        for i in range(self.population_size):
            self.parents.append(Individual(self.chromosome_lenght))
            self.offspring.append(Individual(self.chromosome_lenght))
        self.roulette = np.zeros(self.population_size, dtype=float)
        self.the_best = Individual(self.chromosome_lenght)
        self.current_best = Individual(self.chromosome_lenght)

    #Se crea la primera generacion
    def createFirstGeneration(self):
        for i in range(self.population_size):
            for j in range(self.chromosome_lenght):
                self.parents[i].cromosoma[j] = flip(0.5)

    #Evalua aptitud del individuo
    def evaluateTargetFunction(self, individual: Individual):
        individual.x = individual.binary2Real(self.fx_lower_bound, self.fx_upper_bound)
        individual.fitness = 1 / (pow(individual.x, 2) + 0.001)
        return individual
        
    #Evaluar la aptitud de una poblacion
    def evaluatePopulation(self):
        i = 0
        for i in range(self.population_size):
            self.parents[i] = self.evaluateTargetFunction(self.parents[i])

            #Llenar la ruleta con la probabilidad de cada individuo para ser seleccionado
    def updateRoulette(self):
        i = 0
        sum_fitness = 0
        for i in range(self.population_size):
            sum_fitness += self.parents[i].fitness
        
        i = 0
        for i in range(self.population_size):
            self.roulette[i] = self.parents[i].fitness / sum_fitness


    #Se hace la seleccion por ruleta
    def rouletteWheelSelection(self):
        r = rnd.random()
        suma = 0
        i = 0
        while(suma < r):
            suma += self.roulette[i]
            i+=1  
        return i -1

    def generarHijos(self):
        i = 0
        while i < (self.population_size - 1):
            selected_father = self.rouletteWheelSelection()
            selected_mother = self.rouletteWheelSelection()
            
            self.offspring[i], self.offspring[i+1] = self.crossover(self.parents[selected_father], self.parents[selected_mother])
            self.offspring[i].parents[0] = self.offspring[i+1].parents[1] = selected_father + 1
            self.offspring[i].parents[1] = self.offspring[i+1].parents[0] = selected_mother + 1
            
            self.offspring[i] = self.mutation(self.offspring[i])
            self.offspring[i] = self.evaluateTargetFunction(self.offspring[i])

            self.offspring[i+1] = self.mutation(self.offspring[i+1])
            self.offspring[(i+1)] = self.evaluateTargetFunction(self.offspring[(i+1)])
            i+=2

    #Recombinacion de los padres seleccionados
    def crossover(self, father: Individual, mother: Individual):
        hijo1 = Individual(self.chromosome_lenght)
        hijo2 = Individual(self.chromosome_lenght)
        
        i = 0
        if flip(self.crossover_probability) == 1:
            p = rnd.randint(1, self.chromosome_lenght - 2)
            i = 0
            while(i <= p):
                hijo1.cromosoma[i] = father.cromosoma[i]
                if i+p < self.chromosome_lenght:
                    hijo2.cromosoma[i+p] = mother.cromosoma[i]
                i+=1
                
            i = p+1
            while(i < self.chromosome_lenght):
                hijo1.cromosoma[i] = mother.cromosoma[i]
                hijo2.cromosoma[i-p-1] = father.cromosoma[i]
                i+=1
            
            hijo1.crossover_place = hijo2.crossover_place = p
        else:
            i = 0
            while(i < self.chromosome_lenght):
                hijo1.cromosoma[i] = father.cromosoma[i]
                hijo2.cromosoma[i] = mother.cromosoma[i]
                i+=1
            hijo1.crossover_place = hijo2.crossover_place = -1
        return hijo1, hijo2

        #Realizar mutacion
    def mutation(self, individual: Individual):

        if flip(self.mutation_probability) == 1:
            p = rnd.uniform(0, self.chromosome_lenght - 1)
            p = int(p)
            individual.cromosoma[p] = 1 - individual.cromosoma[p]
            individual.mutation_place = p
        else:
            individual.mutation_place = -1
        return individual

    #Ley del mas fuerte
    def elitism(self):
        worst_child1 = worst_child2 = 0
        best_parent = 0
        i = 0
        while i < self.population_size:
            if self.offspring[i].fitness > self.offspring[worst_child1].fitness:
                worst_child1 = i
            elif self.offspring[i].fitness > self.offspring[worst_child2].fitness:
                worst_child2 = i
            if self.parents[i].fitness > self.parents[best_parent].fitness:
                best_parent = i
            i+=1

        self.offspring[worst_child1] = self.parents[best_parent]
        self.offspring[worst_child2] = self.parents[best_parent]


    def printPopulationDetail(self):
        i = 0
        current_best = 0
        fitness_avg = 0.0
        t = PrettyTable(['#', 'Cromosoma', 'x', 'Aptitud', 'Padres'])
        
        while i < self.population_size:
            padre = self.parents[i].parents[0] if (self.parents[i].parents[0] >= 10 or self.parents[i].parents[0] < 0) else '0'+ str(self.parents[i].parents[0])
            madre = self.parents[i].parents[1] if (self.parents[i].parents[1] >= 10 or self.parents[i].parents[1] < 0) else '0'+ str(self.parents[i].parents[1])
            t.add_row([str(i+1), self.parents[i].cromosoma , self.parents[i].x, self.parents[i].fitness, ('[ '+str(padre)+ '     ' + str(madre) +' ]')])
            fitness_avg += self.parents[i].fitness
            if self.parents[i].fitness > self.parents[current_best].fitness:
                current_best = i
            if self.parents[current_best].fitness > self.the_best.fitness:
                self.the_best = self.parents[i]
            i+=1
        fitness_avg /= self.population_size
        print(t)
        print("\n\n---------------------------------------------\n")
        print("\nAptitud promedio (poblacion): " + str(fitness_avg) )
        print("\nMejor aptitud: " + str(self.parents[current_best].fitness)) 