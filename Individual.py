import numpy as np

class Individual: 
    def __init__(self, chromosome_lenght): 
        self.cromosoma = np.zeros(chromosome_lenght, dtype=int)
        self.chromosome_lenght = len(self.cromosoma)
        self.x = 0
        self.fitness = 0
        self.parents = [-1, -1]
        self.mutation_place = -1
        self.crossover_place = -1

    #Imprimir un cromosoma con indicadores
    def printChromosome(self):
        i = 0
        while(i < self.chromosome_lenght):
            if i == self.mutation_place: 
                print('(', end = '')
            print(self.cromosoma[i], end = '')
            if i == self.mutation_place: 
                print(')', end = '')
            if i == self.crossover_place:
                print('/', end = '')
            i+=1

        #Transforma genotipo en fenotipo y se hace ajuste
    def binary2Real(self, lower, upper):
        i = self.chromosome_lenght - 1
        aux = 0.0
        while i >= 0:
            if self.cromosoma[i] == 1:
                aux += pow(2, self.chromosome_lenght - i - 1)
            i-=1     
        return lower + ((aux * (upper-lower))/(pow(2, self.chromosome_lenght)-1))