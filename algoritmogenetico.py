from typing import List
import random as rnd
import sys
import time
import math as mt

#Definicion del individuo
class Individual: 
    def __init__(self, cromosoma, x, fitness, parents, mutation_place, crossover_place): 
        self.cromosoma = list()
        self.cromosoma = cromosoma
        self.x = x
        self.fitness = fitness
        self.parents = parents
        self.mutation_place = mutation_place
        self.crossover_place = crossover_place

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
        self.parents = [Individual([0] * self.population_size, sys.maxsize, 0, [-1, -1], -1, -1)] * self.population_size
        self.offspring = [Individual([0] * self.population_size, sys.maxsize, 0, [-1, -1], -1, -1)] * self.population_size
        self.roulette = [0] * self.population_size
        self.the_best = Individual([0] * self.population_size, sys.maxsize, 0, [-1, -1], -1, -1)
        self.current_best = Individual([0] * self.population_size, sys.maxsize, 0, [-1, -1], -1, -1)
        self.selected_Father = 0
        self.selected_Mother = 0

def getParameters():
    max_generations = input('\nNúmero de generaciones: ')
    crossover_probability = input('\nProbabilidad de cruce: ')
    mutation_probability = input('\nProbabilidad de mutación: ')
    return Poblacion(crossover_probability, mutation_probability, max_generations)

#Devuelve un aleatorio sobre un intervalo
def randomDouble(a: int,b: int):
    return rnd.uniform(a, b)

#Simular el lanzado de una moneda al aire
def flip(p: float):
    if rnd.random() <= float(p):
        return 1
    return 0

#Se crea la primera generacion
def createFirstGeneration(pob: Poblacion):
    padres = list()
    i = 0
    while i < pob.population_size:
        j = 0
        cromosomas = list()
        while j < pob.chromosome_lenght:
            cromosomas.append(flip(0.5))
            j+=1
        padres.append(Individual(cromosomas, sys.maxsize, 0, [-1, -1], -1, -1))
        i+=1
    return padres
        
#Transforma genotipo en fenotipo y se hace ajuste
def binary2Real(cromosoma: list(), pob: Poblacion):
    i = pob.chromosome_lenght - 1
    aux = 0.0
    while i >= 0:
        if cromosoma[i] == 1:
            aux += pow(2, pob.chromosome_lenght - i - 1)
        i-=1     
    return pob.fx_lower_bound + ((aux * (pob.fx_upper_bound-pob.fx_lower_bound))/(pow(2,pob.chromosome_lenght)-1))

#Evalua aptitud del individuo
def evaluateTargetFunction(individual: Individual, pob: Poblacion):
    individual.x = binary2Real(individual.cromosoma, pob)
    individual.fitness = 1 / (pow(individual.x, 2) + 0.001)
    return individual
    
#Evaluar la aptitud de una poblacion
def evaluatePopulation(population: Poblacion):
    i = 0
    while (i < population.population_size):
        population.parents[i] = evaluateTargetFunction(population.parents[i], population)
        i+=1
    return population
        
#Llenar la ruleta con la probabilidad de cada individuo para ser seleccionado
def updateRoulette(population: Poblacion):
    i = 0
    sum_fitness = 0
    for i in range(population.population_size):
        sum_fitness += population.parents[i].fitness
    
    i = 0
    for i in range(population.population_size):
        population.roulette[i] = population.parents[i].fitness / sum_fitness 
    return population
        
#Se hace la seleccion por ruleta
def rouletteWheelSelection(pob: Poblacion):
    r = rnd.random()
    suma = 0
    i = 0
    while(suma < r):
        suma += pob.roulette[i]
        i+=1  
    return i-1


#Recombinacion de los padres seleccionados
def crossover(father: Individual, mother: Individual, pob: Poblacion):
    hijo1 = Individual([0] * pob.chromosome_lenght, sys.maxsize, 0, [pob.selected_Father, pob.selected_Mother], -1, -1)
    hijo2 = Individual([0] * pob.chromosome_lenght, sys.maxsize, 0, [pob.selected_Father, pob.selected_Mother], -1, -1)
    
    i = 0
    if flip(pob.crossover_probability) == 1:
        p = rnd.randint(1, pob.chromosome_lenght - 2)
        i = 0
        while(i <= p):
            hijo1.cromosoma[i] = father.cromosoma[i]
            if i+p < pob.chromosome_lenght:
                hijo2.cromosoma[i+p] = mother.cromosoma[i]
            i+=1
            
        i = p+1
        while(i < pob.chromosome_lenght):
            hijo1.cromosoma[i] = mother.cromosoma[i]
            hijo2.cromosoma[i-p-1] = father.cromosoma[i]
            i+=1
        
        hijo1.crossover_place = hijo2.crossover_place = p
    else:
        i = 0
        while(i < pob.chromosome_lenght):
            hijo1.cromosoma[i] = father.cromosoma[i]
            hijo2.cromosoma[i] = mother.cromosoma[i]
            i+=1
        hijo1.crossover_place = hijo2.crossover_place = -1
    hijo1.parents[0] = hijo2.parents[1] = pob.selected_father + 1
    hijo1.parents[1] = hijo2.parents[1] = pob.selected_mother + 1
    return hijo1, hijo2
        
#Realizar mutacion
def mutation(individual: Individual, pob: Poblacion):

    if flip(pob.mutation_probability) == 1:
        p = randomDouble(0, pob.chromosome_lenght - 1)
        p = int(p)
        individual.cromosoma[p] = 1 - individual.cromosoma[p]
        individual.mutation_place = p
    else:
        individual.mutation_place = -1
    return individual

#Ley del mas fuerte
def elitism(Pob: Poblacion):
    worst_child1 = worst_child2 = 0
    best_parent = 0
    i = 0
    while i < Pob.population_size:
        if Pob.offspring[i].fitness > Pob.offspring[worst_child1].fitness:
            worst_child1 = i
        elif Pob.offspring[i].fitness > Pob.offspring[worst_child2].fitness:
            worst_child2 = i
        if Pob.parents[i].fitness < Pob.parents[best_parent].fitness:
            best_parent = i
        i+=1

    Pob.offspring[worst_child1] = Pob.parents[best_parent]
    Pob.offspring[worst_child2] = Pob.parents[best_parent]
    return Pob
    
#Imprimir un cromosoma con indicadores
def printChromosome(individual: Individual):
    chromosome_lenght = len(individual.cromosoma)
    i = 0
    while(i < chromosome_lenght):
        if i == individual.mutation_place: 
            print('(', end = '')
        print(individual.cromosoma[i], end = '')
        if i == individual.mutation_place: 
            print(')', end = '')
        if i == individual.crossover_place:
            print('/', end = '')
        i+=1
        
def printPopulationDetail(population: Poblacion):
    i = 0
    current_best = 0
    fitness_avg = 0.0
    print('\n\n------------------------------------------------------------------------------------------\n')
    print('#\tCromosoma\t\t\tx\tAptitud\t\t  Padres')
    print('\n------------------------------------------------------------------------------------------\n')
    
    while i < population.population_size:
        print('\n ' + str(i+1) + '\t', end = '')
        printChromosome(population.parents[i])
        print('\t' + '%.10f'%population.parents[i].x + '\t' + '%.10f'%population.parents[i].fitness + '\t' + '[' + str(population.parents[i].parents[0]) + '\t' + str(population.parents[i].parents[1]) + ']')
        fitness_avg += population.parents[i].fitness
        if population.parents[i].fitness > population.parents[current_best].fitness:
            current_best = i
        if population.parents[current_best].fitness > population.the_best.fitness:
            population.the_best = population.parents[i]
        i+=1
    fitness_avg /= population.population_size
    print("\n\n---------------------------------------------\n")
    print("\nAptitud promedio (poblacion): " + str(fitness_avg) )
    print("\nMejor aptitud: " + str(population.parents[current_best].fitness)) 
    
def generarHijos(pob: Poblacion):
    i = 0
    while i < (pob.population_size - 1):
        pob.selected_father = rouletteWheelSelection(pob)
        pob.selected_mother = rouletteWheelSelection(pob)
        
        pob.offspring[i], pob.offspring[i+1] = crossover(pob.parents[pob.selected_father], pob.parents[pob.selected_mother], pob)
        
        pob.offspring[i] = mutation(pob.offspring[i], pob)
        pob.offspring[i] = evaluateTargetFunction(pob.offspring[i], pob)

        pob.offspring[i+1] = mutation(pob.offspring[i+1], pob)
        pob.offspring[(i+1)] = evaluateTargetFunction(pob.offspring[(i+1)], pob)
        i+=2
    return pob
        
    
def principal():
    Poblacion = getParameters()
    Poblacion.parents = createFirstGeneration(Poblacion)
    Poblacion = evaluatePopulation(Poblacion)
    temp_helper = list()
    generation = 0
    i = 0
    #Proceso de generacion
    while(generation < int(Poblacion.max_generations)):
        Poblacion = updateRoulette(Poblacion)
        printPopulationDetail(Poblacion)  
        Poblacion = generarHijos(Poblacion) 
        Poblacion = elitism(Poblacion)
        temp_helper = Poblacion.parents
        Poblacion.parents = Poblacion.offspring
        Poblacion.offspring = temp_helper
        print("\n\nTermino con éxito generación " + str(generation + 1) + "\n")
        generation += 1
        
    print("\n\n************************************************************")
    print("\n\t\t\tEL MEJOR")
    print("\n************************************************************")
    print("\n\tCadena binaria:  ", end = ' ')
    printChromosome(Poblacion.the_best)
    print()
    print("\n\tx = " + str(Poblacion.the_best.x) + "\tAptitud = " + str(Poblacion.the_best.fitness))
    print('\n\tPadres: ' + str(Poblacion.the_best.parents[0]) + "," + str(Poblacion.the_best.parents[1]))
    
principal()