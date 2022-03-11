from ast import If
from typing import List
import math as mt
from operator import mod
import random as rnd
import sys
from typing import List
from ctypes import *
import numpy as np
import time

#Definicion del individuo
class Individual: 
    def __init__(self, cromosoma, x, fitness, parents, mutation_place, crossover_place): 
        self.cromosoma = list()
        self.cromosoma = cromosoma
        self.x = x
        self.fitness = fitness
        self.parents = list()
        self.parents = parents
        self.mutation_place = mutation_place
        self.crossover_place = crossover_place

#Variables
POPULATION_SIZE = 100
FX_LOWER_BOUND  = -20
FX_UPPER_BOUND = 20
PRECISION = 3

crossover_probability: 0
mutation_probability: 0
max_generations: 0
selected_father = 0
selected_mother = 0
chromosome_lenght = mt.ceil(mt.log2((FX_UPPER_BOUND - FX_LOWER_BOUND) * pow(10, PRECISION)))

#Poblaciones, ruleta y elitista
parents: List[Individual]
parents = list()
offspring: List[Individual]
offspring = list()
the_best = Individual(np.zeros(chromosome_lenght), sys.maxsize, 0, [-1, -1], -1, -1)
roulette = list()

def getParameters():
    global max_generations
    global crossover_probability
    global mutation_probability
    global chromosome_lenght

    max_generations = input('\nNúmero de generaciones: ')
    crossover_probability = input('\nProbabilidad de cruce: ')
    mutation_probability = input('\nProbabilidad de mutación: ')

def allocateMemory():
    global parents
    global offspring
    global the_best
    global roulette
    global chromosome_lenght
    global POPULATION_SIZE
    
    parents = list()
    offspring = list()

    i = 0
    x = sys.maxsize
    objeto = Individual([0]*chromosome_lenght, x, 0, [-1, -1], -1, -1)
    i = 0

    while(i < POPULATION_SIZE):
        parents.append(objeto)
        offspring.append(objeto)
        i+=1

    the_best = objeto
    roulette = [0] * POPULATION_SIZE

#Devuelve un aleatorio sobre un intervalo
def randomDouble(a: int,b: int):
    return rnd.uniform(a, b)

#Simular el lanzado de una moneda al aire
def flip(p: float):
    rnd.seed(time.time())
    if randomDouble(0,1) <= float(p):
        return 1
    else:
        return 0

#Se crea la primera generacion
def createFirstGeneration():
    global chromosome_lenght
    global POPULATION_SIZE
    padres = list()
    i = 0
    while i < POPULATION_SIZE:
        j = 0
        cromosomas = list()
        while j < chromosome_lenght:
            cromosomas.append(flip(0.5))
            j+=1
        padres.append(Individual(cromosomas, sys.maxsize, 0, [-1, -1], -1, -1))
        i+=1
    return padres
        
#Transforma genotipo en fenotipo y se hace ajuste
def binary2Real(cromosoma: list()):
    global chromosome_lenght
    global FX_LOWER_BOUND
    global FX_UPPER_BOUND
    
    i = chromosome_lenght - 1
    aux = 0.0
    while i >= 0:
        if cromosoma[i] == 1:
            aux += pow(2, chromosome_lenght - i - 1)
        i-=1     
    return FX_LOWER_BOUND + ((aux * (FX_UPPER_BOUND-FX_LOWER_BOUND))/(pow(2,chromosome_lenght)-1))

#Evalua aptitud del individuo
def evaluateTargetFunction(individual: Individual):
    individual.x = binary2Real(individual.cromosoma)
    individual.fitness = 1 / (pow(individual.x, 2) + 0.001)
    return individual
    
#Evaluar la aptitud de una poblacion
def evaluatePopulation(population: List[Individual]):
    global POPULATION_SIZE
    i = 0
    while (i < POPULATION_SIZE):
        population[i] = evaluateTargetFunction(population[i])
        i+=1
    return population
        
#Llenar la ruleta con la probabilidad de cada individuo para ser seleccionado
def updateRoulette(population: List[Individual] ):
    global POPULATION_SIZE
    global roulette
    
    i = 0
    sum_fitness = 0.0
    for i in range(POPULATION_SIZE):
        sum_fitness += population[i].fitness
    
    i = 0
    for i in range(POPULATION_SIZE):
        roulette[i] = population[i].fitness / sum_fitness 
        
#Se hace la seleccion por ruleta
def rouletteWheelSelection():
    global POPULATION_SIZE
    global roulette
    
    r = randomDouble(0,1)
    sum = 0.0
    i = POPULATION_SIZE
    current_individual = 0
    while(sum < r):
        current_individual = i % POPULATION_SIZE
        sum += roulette[current_individual]
        i+=1   
    return current_individual


#Recombinacion de los padres seleccionados
def crossover(father: Individual, mother: Individual):
    global selected_father
    global selected_mother
    global chromosome_lenght
    global POPULATION_SIZE 
    global crossover_probability
    
    hijo1 = Individual([0] * chromosome_lenght, sys.maxsize, 0, [selected_father, selected_mother], -1, -1)
    hijo2 = Individual([0] * chromosome_lenght, sys.maxsize, 0, [selected_father, selected_mother], -1, -1)
    
    i = 0
    if flip(crossover_probability) == 1:
        p = rnd.randint(1, chromosome_lenght - 2)
        i = 0
        while(i <= p):
            hijo1.cromosoma[i] = father.cromosoma[i]
            if i+p < chromosome_lenght:
                hijo2.cromosoma[i+p] = mother.cromosoma[i]
            i+=1
            
        i = p+1
        while(i < chromosome_lenght):
            hijo1.cromosoma[i] = mother.cromosoma[i]
            hijo2.cromosoma[i-p-1] = father.cromosoma[i]
            i+=1
        
        hijo1.crossover_place = hijo2.crossover_place = p
        hijo1.parents[0] = hijo2.parents[1] = selected_father + 1
        hijo1.parents[1] = hijo2.parents[1] = selected_mother + 1
    else:
        i = 0
        while(i < chromosome_lenght):
            hijo1.cromosoma[i] = father.cromosoma[i]
            hijo2.cromosoma[i] = mother.cromosoma[i]
            i+=1
        hijo1.crossover_place = hijo2.crossover_place = -1
        #child1.parents[0] = child2.parents[0] = 0
        #child1.parents[1] = child2.parents[1] = 0
    return hijo1, hijo2
        
#Realizar mutacion
def mutation(individual: Individual):
    global mutation_probability
    global chromosome_lenght
    
    if flip(mutation_probability) == 1:
        p = randomDouble(0, chromosome_lenght - 1)
        p = int(p)
        individual.cromosoma[p] = 1 - individual.cromosoma[p]
        individual.mutation_place = p
    else:
        individual.mutation_place = -1
    return individual

#Ley del mas fuerte
def elitism():
    global offspring
    global POPULATION_SIZE
    global parents

    worst_child1 = worst_child2 = 0
    best_parent = 0
    i = 0
    while i < POPULATION_SIZE:
        if offspring[i].fitness < offspring[worst_child1].fitness:
            worst_child1 = i
        elif offspring[i].fitness < offspring[worst_child2].fitness:
            worst_child2 = i
        if parents[i].fitness > parents[best_parent].fitness:
            best_parent = i
        i+=1

    offspring[worst_child1] = parents[best_parent]
    offspring[worst_child2] = parents[best_parent]
    
#Imprimir un cromosoma con indicadores
def printChromosome(individual: Individual):
    global chromosome_lenght
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
        
def printPopulationDetail(population: List[Individual]):
    global the_best
    global POPULATION_SIZE
    i = 0
    current_best = 0
    fitness_avg = 0.0
    print('\n\n------------------------------------------------------------------------------------------\n')
    print('#\tCromosoma\t\t\tx\tAptitud\t\t  Padres')
    print('\n------------------------------------------------------------------------------------------\n')
    
    while i < POPULATION_SIZE:
        print('\n ' + str(i+1) + '\t', end = '')
        printChromosome(population[i])
        print('\t' + '%.10f'%population[i].x + '\t' + '%.10f'%population[i].fitness + '\t' + '[' + str(population[i].parents[0]) + '\t' + str(population[i].parents[1]) + ']')
        fitness_avg += population[i].fitness
        if population[i].fitness > population[current_best].fitness:
            current_best = i
        if population[current_best].fitness > the_best.fitness:
            the_best = population[i]
        i+=1
    fitness_avg /= POPULATION_SIZE
    print("\n\n---------------------------------------------\n")
    print("\nAptitud promedio (poblacion): " + str(fitness_avg) )
    print("\nMejor aptitud: " + str(population[current_best].fitness)) 
    
def generarHijos():
    global offspring  
    global parents
    global the_best
    global selected_father
    global selected_mother
    
    lista = [Individual([0] * chromosome_lenght, sys.maxsize, 0, [-1, -1], -1, -1)] * POPULATION_SIZE
    i = 0
    while i < (POPULATION_SIZE - 1):
        selected_father = rouletteWheelSelection()
        selected_mother = rouletteWheelSelection()
        
        lista[i], lista[i+1] = crossover(parents[selected_father], parents[selected_mother])
        
        lista[i] = mutation(lista[i])
        lista[i] = evaluateTargetFunction(lista[i])

        lista[i+1] = mutation(lista[i+1])
        lista[(i+1)] = evaluateTargetFunction(lista[(i+1)])
        i+=2
    return lista
        
    
def principal():
    global selected_father
    global selected_mother
    global offspring
    global the_best
    global parents
    
    getParameters()
    rnd.seed(time.time())
    allocateMemory()
    parents = createFirstGeneration()
    evaluatePopulation(parents)
    temp_helper = list()
    generation = 0
    i = 0
    #Proceso de generacion
    while(generation < int(max_generations)):
        updateRoulette(parents)
        printPopulationDetail(parents)  
        offspring = generarHijos() 
        elitism()
        temp_helper = parents
        parents = offspring
        offspring = temp_helper
        print("\n\nTermino con éxito generación " + str(generation + 1) + "\n")
        generation += 1
        
    print("\n\n************************************************************")
    print("\n\t\t\tEL MEJOR")
    print("\n************************************************************")
    print("\n\tCadena binaria:  ", end = ' ')
    printChromosome(the_best)
    print()
    print("\n\tx = " + str(the_best.x) + "\tAptitud = " + str(the_best.fitness))
    print('\n\tPadres: ' + str(the_best.parents[0]) + "," + str(the_best.parents[1]))
    
principal()