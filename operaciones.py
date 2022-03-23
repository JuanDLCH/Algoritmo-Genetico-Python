import random as rnd
#Simular el lanzado de una moneda al aire
def flip(p: float):
    if rnd.random() <= float(p):
        return 1
    return 0