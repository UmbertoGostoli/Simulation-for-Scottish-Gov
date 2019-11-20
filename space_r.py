# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:01:53 2017

@author: ug4d
"""
import random
import numpy as np

class Town:
    counter = 1
    """Contains a collection of houses."""
    def __init__ (self, townGridDimension, tx, ty,
                  cdfHouseClasses, density, classBias, densityModifier ):
        self.x = tx
        self.y = ty
        self.houses = []
        self.name = str(tx) + "-" + str(ty)
        self.id = Town.counter
        Town.counter += 1
        if density > 0.0:
            adjustedDensity = density * densityModifier
            for hy in range(int(townGridDimension)):
                for hx in range(int(townGridDimension)):
                    if random.random() < adjustedDensity:
                        newHouse = House(self,cdfHouseClasses,
                                         classBias,hx,hy)
                        self.houses.append(newHouse)

class Map:
    """Contains a collection of towns to make up the whole country being simulated."""
    def __init__ (self, gridXDimension, gridYDimension,
                  townGridDimension, cdfHouseClasses,
                  ukMap, ukClassBias, densityModifier ):
        self.towns = []
        self.allHouses = []
        self.occupiedHouses = []
        ukMap = np.array(ukMap)
        ukMap.resize(int(gridYDimension), int(gridXDimension))
        ukClassBias = np.array(ukClassBias)
        ukClassBias.resize(int(gridYDimension), int(gridXDimension))
        for y in range(int(gridYDimension)):
            for x in range(int(gridXDimension)):
                newTown = Town(townGridDimension, x, y,
                               cdfHouseClasses, ukMap[y][x],
                               ukClassBias[y][x], densityModifier )
                self.towns.append(newTown)

        for t in self.towns:
            for h in t.houses:
                self.allHouses.append(h)
                        
class House:
    counter = 1
    """The house class stores information about a distinct house in the sim."""
    def __init__ (self, town, cdfHouseClasses, classBias, hx, hy):
        
        r = np.random.random()
        
        i = 0
        c = cdfHouseClasses[i] - classBias
        while r > c:
            i += 1
            c = cdfHouseClasses[i] - classBias
        self.size = i
        self.initialOccupants = 0
        self.occupants = []
        self.occupantsID = []
        self.town = town
        self.x = hx
        self.y = hy
        self.rank = None
        self.icon = None
        self.id = House.counter
        House.counter += 1
        self.name = self.town.name + "-" + str(hx) + "-" + str(hy)
        