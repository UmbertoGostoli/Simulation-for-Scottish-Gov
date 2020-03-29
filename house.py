
import random
import numpy as np
import networkx as nx

class House:
    counter = 1
    """The house class stores information about a distinct house in the sim."""
    def __init__ (self, town, hx, hy):

        self.sizeIndex = -1
        self.wealth = 0
        self.occupants = []
        self.occupantsID = []  # For pickle
        self.newOccupancy = False
        self.town = town
        self.x = hx
        self.y = hy
        self.icon = None
        self.display = False
        self.householdIncome = 0
        self.wealthForCare = 0
        self.householdCumulativeIncome = 0
        self.incomePerCapita = 0
        self.incomeQuintile = 0
        self.name = self.town.name + "-" + str(hx) + "-" + str(hy)
        self.sizeIndex = -1
        self.id = House.counter
        
        # House care variables
        self.careNetwork = nx.DiGraph()
        self.demandNetwork = nx.Graph()
        self.townAttractiveness = []
        self.totalSocialCareNeed = 0
        self.netCareDemand = 0
        self.careAttractionFactor = 0
        self.totalUnmetSocialCareNeed = 0
        self.totalChildCareNeed = 0
        self.childCareNeeds = []
        self.childCarePrices = []
        self.cumulatedChildren = []
        self.highPriceChildCare = 0
        self.lowPriceChildCare = 0
        self.residualIncomeForChildCare = 0
        self.initialResidualIncomeForChildCare = 0
        self.residualIncomeForSocialCare = []
        self.householdInformalSupplies = []
        self.householdFormalSupply = []
        self.networkSupply = 0
        self.suppliers = []
        self.receivers = []
        self.networkSupport = 0
        self.networkTotalSupplies = []
        self.totalSupplies = []
        self.netCareSupply = 0
        self.networkInformalSupplies = []
        self.formalChildCareSupply = 0
        self.networkFormalSocialCareSupplies = []
        self.childCareWeights = []
        self.formalCaresRatios = []
        self.informalChildCareReceived = 0
        self.informalSocialCareReceived = 0
        self.formalChildCareReceived = 0
        self.formalChildCareCost = 0
        self.formalSocialCareReceived = 0
        self.householdFormalSupplyCost = 0
        self.outOfWorkSocialCare = 0
        self.incomeByTaxBand = []
        self.averageChildCarePrice = 0
        
        House.counter += 1
                            
class Town:
    counter = 1
    """Contains a collection of houses."""
    def __init__ (self, townGridDimension, tx, ty, density,
                  lha1, lha2, lha3, lha4):
        self.name = 'Town_' + str(tx) + '_' + str(ty)
        self.x = tx
        self.y = ty
        self.houses = []
        self.neighboringTowns = []
        self.neighborsIDs = []
        self.LHA = [lha1, lha2, lha3, lha4]
        self.id = Town.counter
        Town.counter += 1
        if density > 0.0:
            for hy in range(int(townGridDimension)):
                for hx in range(int(townGridDimension)):
                    if np.random.random() < density:
                        newHouse = House(self, hx, hy)
                        self.houses.append(newHouse)

class Map:
    """Contains a collection of towns to make up the whole country being simulated."""
    def __init__ (self, gridXDimension, gridYDimension,
                  townGridDimension, scotlandGrid):
        self.towns = []
        self.allHouses = []
        self.occupiedHouses = []
        maxPop = float(max(scotlandGrid['pop']))
        for index, row in scotlandGrid.iterrows():
            density = float(row['pop'])/maxPop
            newTown = Town(townGridDimension, int(row['town_x']), int(row['town_y']), density,
                               row['lha_1'], row['lha_2'], row['lha_3'], row['lha_4'])
            self.towns.append(newTown)
        for t in self.towns:
            y_townRange = range(int(max(0, t.y-1)), int(min(gridYDimension-1, t.y+1)+1))
            x_townRange = range(int(max(0, t.x-1)), int(min(gridXDimension-1, t.x+1)+1))
            t.neighboringTowns = [k for k in self.towns if k.y in y_townRange and k.x in x_townRange]
            for h in t.houses:
                self.allHouses.append(h)




