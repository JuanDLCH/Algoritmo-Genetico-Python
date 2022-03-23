from Population import *

def getParameters():
    max_generations = input('\nNúmero de generaciones: ')
    crossover_probability = input('\nProbabilidad de cruce: ')
    mutation_probability = input('\nProbabilidad de mutación: ')
    return Poblacion(crossover_probability, mutation_probability, max_generations)
        
    
def principal():
    Poblacion = getParameters() #Crear la población con los parámetros dados
    Poblacion.createFirstGeneration()
    Poblacion.evaluatePopulation()
    generation = 0
    i = 0
    #Proceso de generacion
    while(generation < int(Poblacion.max_generations)):
        Poblacion.updateRoulette()
        Poblacion.printPopulationDetail() 
        Poblacion.generarHijos() 
        Poblacion.elitism()
        temp_helper = Poblacion.parents
        Poblacion.parents = Poblacion.offspring
        Poblacion.offspring = temp_helper
        print("\n\nTermino con éxito generación " + str(generation + 1) + "\n")
        generation += 1
        
    print("\n\n************************************************************")
    print("\n\t\t\tEL MEJOR")
    print("\n************************************************************")
    print("\n\tCadena binaria:  ", end = ' ')
    Poblacion.the_best.printChromosome()
    print()
    print("\n\tx = " + str(Poblacion.the_best.x) + "\tAptitud = " + str(Poblacion.the_best.fitness))
    print('\n\tPadres: ' + str(Poblacion.the_best.parents[0]) + "," + str(Poblacion.the_best.parents[1]))
    
principal()