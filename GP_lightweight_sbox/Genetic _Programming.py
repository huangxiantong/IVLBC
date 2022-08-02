from Sbox_properties import Sbox_properties
import operator
import math
import random
import numpy as np


from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import ctypes
from ctypes import *


Non_lin = ctypes.cdll.LoadLibrary('./non_lin.dll')
Diff_Unif = ctypes.cdll.LoadLibrary('./Diff_Unif.dll')
Max_Degree = ctypes.cdll.LoadLibrary('./Max_Degree.dll')
SZ1=c_int *16
sbox_4=SZ1()
S = Sbox_properties()
global number
number=0

s_box_tree=['xor(xor(y0, y1), y2)',
         'xor(and_(y0, y1), y2)',
         'xor(or_(y0, y1), y2)',
         'xor(nor_(y0, y1), y2)',
         'xor(nand_(y0, y1), y2)',
         'xor(nxor(y0, y1), y2)',
         'and_(xor(y0, y1), y2)',
        'and_(and_(y0, y1), y2)',
         'and_(or_(y0, y1), y2)',
         'and_(nor_(y0, y1), y2)',
         'and_(nand_(y0, y1), y2)',
         'and_(nxor(y0, y1), y2)',
          'or_(xor(y0, y1), y2)',
          'or_(and_(y0, y1), y2)',
          'or_(or_(y0, y1), y2)',
          'or_(nor_(y0, y1), y2)',
          'or_(nand_(y0, y1), y2)',
          'or_(nxor(y0, y1), y2)',
          'nor_(xor(y0, y1), y2)',
          'nor_(and_(y0, y1), y2)',
          'nor_(or_(y0, y1), y2)',
          'nor_(nor_(y0, y1), y2)',
          'nor_(nand_(y0, y1), y2)',
          'nor_(nxor(y0, y1), y2)',
          'nand_(xor(y0, y1), y2)',
          'nand_(and_(y0, y1), y2)',
          'nand_(or_(y0, y1), y2)',
          'nand_(nor_(y0, y1), y2)',
          'nand_(nand_(y0, y1), y2)',
          'nand_(nxor(y0, y1), y2)',
          'nxor(xor(y0, y1), y2)',
          'nxor(and_(y0, y1), y2)',
          'nxor(or_(y0, y1), y2)',
          'nxor(nor_(y0, y1), y2)',
          'nxor(nand_(y0, y1), y2)',
          'nxor(nxor(y0, y1), y2)'
          ]
p_arrangement=[[0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1],[1,0,2,3],[1,0,3,2],
               [1,2,0,3],[1,2,3,0],[1,3,0,2],[1,3,2,0],[2,0,1,3],[2,0,3,1],[2,1,0,3],[2,1,3,0],
               [2,3,0,1],[2,3,1,0],[3,0,1,2],[3,0,2,1],[3,1,0,2],[3,1,2,0],[3,2,0,1],[3,2,1,0]]
s_box_2=['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']


filename_FP="v.0_FP_round(4)_1.txt"
fileobj = open(filename_FP,  "w")
fileobj.close()

#1.Creating the primitives set
pset = gp.PrimitiveSet("MAIN",3)
pset.addPrimitive(operator.xor, 2)
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.nor_, 2)
pset.addPrimitive(operator.nand_, 2)
pset.addPrimitive(operator.nxor, 2)
pset.renameArguments(ARG0='y0')
pset.renameArguments(ARG1='y1')
pset.renameArguments(ARG2='y2')


# Creating FitnessMax Class
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness = creator.FitnessMax)

# Generate individual

toolbox = base.Toolbox()
toolbox.register("indices",  random.randint, 0,23)
toolbox.register('Individual', tools.initRepeat, creator.Individual, toolbox.indices, n=4)
toolbox.register('Population', tools.initRepeat, list, toolbox.Individual)



def F_randrom( ):
    a = random.randint(0, 12)
    return a


def Replacement(n,a):
    b = ['', '', '', '']
    b[0]=a[n[0]]
    b[1]=a[n[1]]
    b[2]=a[n[2]]
    b[3]=a[n[3]]
    return b


def round(individual,F_value,value):
    P_sub=individual
    F_sub=individual+F_value
    a=Replacement(p_arrangement[P_sub],value)
    new_tree = gp.PrimitiveTree.from_string(s_box_tree[F_sub], pset)
    function = gp.compile(new_tree, pset)
    a[0] = bin(function(int(a[1]), int(a[3]), int(a[0])))[-1]
    return a


def out_4(individual,F_sub,P_sub,i):
    return_value =round(individual[0],F_sub[0],i)

    for j in range(1,4):
        return_value=round(individual[j],F_sub[j],return_value)


    return_value = Replacement(p_arrangement[P_sub], return_value)

    c=return_value[0]+return_value[1]+return_value[2]+return_value[3]
    a = int(c, 2)
    return a


def sbox(individual,F_sub, P_sub):
    out=[]
    j=0

   # print("shuiji",F_sub)
    for i in s_box_2:
        a=out_4(individual,F_sub,P_sub,i)
        out.append(a)
        sbox_4[j]=a
        j=j+1
    # print(len(out))
    # print(max(out))
    # print(min(out))

    if S.Balancedness(out)==True:
        return out
    else:
        return 0

def evaluate(individual):
    F_sub = []
    for i in range(4):
        F_sub.append(F_randrom())
    P_sub=random.randint(0, 23)
    sbox_in=sbox(individual,F_sub,P_sub)
    Nonlin_Scoring=0
    Involutive_Scoring=0
    DiffUnif_Scoring=0
    Degree_Scoring = 0
    #fixedpoint_Scoring = 0
    sum_Scoring =0
    if sbox_in!=0:
        Nonlin_Scoring = Non_lin.SF_Walsh(sbox_4)*100
        if Nonlin_Scoring == 400:
            fileobj = open(filename_FP, "a")
            fileobj.write("\n")
            fileobj.write("F:\n")
            for i in range(4):
                fileobj.write('%s//' % s_box_tree[F_sub[i]+individual[i]])
            fileobj.write("\n")
            fileobj.write("P:\n")
            for i in range(4):
               fileobj.write('%s//' % individual[i])
            fileobj.write('%s//' % P_sub)
            fileobj.write("\n")
            fileobj.close()
            Involutive_Scoring = S.involutive_sbox(sbox_in)
            DiffUnif_Scoring = Diff_Unif.DC(sbox_4)*100
            Degree_Scoring = Max_Degree.max_degree(sbox_4) * 100
            #fixedpoint_Scoring=(16-S.fixed_point())*100

    sum_Scoring= Nonlin_Scoring+Involutive_Scoring+DiffUnif_Scoring+Degree_Scoring
    return sum_Scoring,
def mutUniform(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.randint(0,23)
    return individual,

toolbox.register('Evaluate', evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutUniform, indpb=0.09)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    pop = toolbox.Population(n=3000)
    CXPB, MUTPB = 0.5, 0.09

    fitnesses = list(map(toolbox.Evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values[0] for ind in pop]

    g = 0

    while max(fits) < 812 and g <3000:
        g += 1
        print("-- Generation %i --" % g)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))


        for i in range(1, len(offspring), 2):
            if offspring[i].fitness.values!=400 and offspring[i].fitness.values!=400:
                if random.random() < CXPB:
                    offspring[i - 1], offspring[i]=toolbox.mate(offspring[i - 1], offspring[i])
                    del offspring[i - 1].fitness.values, offspring[i].fitness.values

        for i in range(len(offspring)):
            if random.random() < MUTPB:
                offspring[i],=toolbox.mutate(offspring[i])
                del offspring[i].fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.Evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit


        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))

main()
