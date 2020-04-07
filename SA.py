import math
import random

import numpy as np
import pandas as pd
from scipy.constants import k

numberOfCities = 0
genEvolved = 0
minDist = math.inf
bestRoute = []

currentDist = 0

route = []

T = 25
scale_factor = 0.000125
alpha_temp = 0.9



def addCity_using_coords():
    
    global numberOfCities, cityCoord, distanceMatrix
    temp_list = []
    try:
        with open("./dataset/ch150_xy.txt", "r") as f:
            for line in f:
                x, y = line.split()
                temp_list.append([float(x),float(y)])  #Convert to float for accuracy
            cityCoord = pd.DataFrame(temp_list, columns = ["x-coord", "y-coord"])
            cityCoord = cityCoord.mul(scale_factor)       #Initiating pandas dataframe
    
        numberOfCities =  len(cityCoord) 
        if numberOfCities > 0:
            distanceMatrix = pd.DataFrame(columns = np.arange(numberOfCities))
            
            generateDistMatrix()

    except: pass

    

def generateDistMatrix():

    global distanceMatrix
    global numberOfCities

    for i in range(numberOfCities):
        temp_dist = []
        for j in range(numberOfCities):
            a = cityCoord.iloc[i].values 
            b = cityCoord.iloc[j].values   

            distance = np.linalg.norm(a-b)
            temp_dist.append(float(distance))  
         

        distanceMatrix.loc[len(distanceMatrix)] = temp_dist


def calculateSolutionFitness(arr):

    distance = 0
    for j in range(len(arr)-1):
        distance += distanceMatrix.iat[arr[j],arr[j+1]]

    return (distance)


def generateNeighbor(arr):
    r = random.random()
    size = len(arr)
    a = random.randint(1,size-2)
    b = random.randint(a+1, size-1)
    newarr = np.array([])

    x = arr[:a]
    y = arr[a:b+1]
    z = arr[b+1:]

    if r > 0.5:
        w = y[::-1]
        newarr = np.concatenate((x,w,z))

    else:
        u = random.randint(0,len(z))
        newarr = np.concatenate((x,z[:u],y,z[u:]))
    
    return newarr


def moveInSolution(arr):

    neighbor = generateNeighbor(arr)
    
    s = calculateSolutionFitness(arr)
    s_dash = calculateSolutionFitness(neighbor)
    
    del_e = s_dash - s

    if(del_e < 0):
    
        return (s_dash, neighbor,1)

    elif(del_e > 0):
        pr = math.exp((-del_e) / (k * T) ) 
        a = random.random()

        if (pr > a):
            
            return (s_dash, neighbor,1)
        else: return (s, arr,0)

    
    else: return (s, arr,0)


def SA(arr):
    global T

    accepted = 1

    while(accepted != 0):
        accepted = 0
        for i in range(100 * len(route)):
            currentDist, arr, status  = moveInSolution(arr)
            if(status == 1):
                accepted += 1

            if(accepted > 10 * len(route)):
                break
        
        print("Moves: ", accepted, "iterations: ", i)
        
        T *= alpha_temp 

    return (currentDist, arr)


addCity_using_coords()
route = np.arange(numberOfCities)
print("\nCity Count" ,numberOfCities)

a,b = SA(route)
print(a/scale_factor, b)
