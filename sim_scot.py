
from person import Person
from person import Population
from house import House
from house import Town
from house import Map
import random
import math
import pylab
# import Tkinter
import struct
import time
import sys
import pprint
import pickle
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import csv
import os
from collections import OrderedDict
import operator
import itertools
from itertools import izip_longest
import networkx as nx
# from PIL import ImageTk         
# from PIL import Image



class Sim:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, scenario, params, folder):
        
        self.p = OrderedDict(params)
        
        self.dataMap = ['town', 'town_x', 'town_y', 'x', 'y', 'size', 'unmetNeed'] 
        
        self.dataPyramid = ['year', 'Class Age 0', 'Class Age 1', 'Class Age 2', 'Class Age 3', 'Class Age 4', 'Class Age 5', 'Class Age 6', 'Class Age 7',
                            'Class Age 8', 'Class Age 9', 'Class Age 10', 'Class Age 11', 'Class Age 12', 'Class Age 13', 'Class Age 14', 'Class Age 15',
                            'Class Age 16', 'Class Age 17', 'Class Age 18', 'Class Age 19', 'Class Age 20', 'Class Age 21', 'Class Age 22', 'Class Age 23', 
                            'Class Age 24']
        
        self.houseData = ['year', 'House name', 'size']
        
        self.householdData = ['ID', 'Sex', 'Age', 'Health']
        
        self.log = ['year', 'message']
        
        self.Outputs = ['year', 'currentPop', 'normalizedPop', 'popFromStart', 'deaths', 'shareDeaths', 'births', 'shareBirths', 
                        'numHouseholds', 'averageHouseholdSize', 'marriageTally', 'marriagePropNow', 'divorceTally', 'shareSingleParents', 
                        'shareFemaleSingleParent', 'taxPayers', 'taxBurden', 'familyCareRatio', 'employmentRate', 'shareWorkingHours', 
                        'publicSocialCare', 'costPublicSocialCare', 'sharePublicSocialCare', 'publicCareExpenses', 
                        'costTaxFreeSocialCare', 'publicChildCare', 'costPublicChildCare', 'sharePublicChildCare', 'costTaxFreeChildCare', 
                        'totalTaxRevenue', 'totalPensionRevenue', 'pensionExpenditure', 'totalHospitalizationCost', 
                        'classShare_1', 'classShare_2', 'classShare_3', 'classShare_4', 'classShare_5', 'totalInformalChildCare', 
                        'formalChildCare', 'childcareIncomeShare', 'shareInformalChildCare', 'shareCareGivers', 
                        'ratioFemaleMaleCarers', 'shareMaleCarers', 'shareFemaleCarers', 'ratioWage', 'ratioIncome', 
                        'shareFamilyCarer', 'share_over20Hours_FamilyCarers', 'averageHoursOfCare', 'share_40to64_carers', 
                        'share_over65_carers', 'share_10PlusHours_over70', 'totalSocialCareNeed', 
                        'totalInformalSocialCare', 'totalFormalSocialCare', 'totalUnmetSocialCareNeed', 
                        'totalSocialCare', 'share_InformalSocialCare', 'share_UnmetSocialCareNeed',
                        'totalOWSC', 'shareOWSC', 'totalCostOWSC',
                        'q1_socialCareNeed', 'q1_informalSocialCare', 'q1_formalSocialCare', 'q1_unmetSocialCareNeed', 'q1_outOfWorkSocialCare',
                        'q2_socialCareNeed', 'q2_informalSocialCare', 'q2_formalSocialCare', 'q2_unmetSocialCareNeed', 'q2_outOfWorkSocialCare',
                        'q3_socialCareNeed', 'q3_informalSocialCare', 'q3_formalSocialCare', 'q3_unmetSocialCareNeed', 'q3_outOfWorkSocialCare',
                        'q4_socialCareNeed', 'q4_informalSocialCare', 'q4_formalSocialCare', 'q4_unmetSocialCareNeed', 'q4_outOfWorkSocialCare',
                        'q5_socialCareNeed', 'q5_informalSocialCare', 'q5_formalSocialCare', 'q5_unmetSocialCareNeed', 'q5_outOfWorkSocialCare',
                        'grossDomesticProduct', 'publicCareToGDP', 'popEdinburgh', 'fromEdinbugh', 'toEdinburgh', 'popGlasgow', 'fromGlasgow', 
                        'toGlasgow', 'popAberdeen', 'fromAberdeen', 'toAberdeen']
        
        self.outputData = pd.DataFrame()
        # Save initial parametrs into Scenario folder
        self.folder = folder + '/Scenario_' + str(scenario)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        filePath = self.folder + '/scenarioParameters.csv'
        c = params.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filePath, "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        
        ####  SES variables   #####
        self.socialClassShares = []
        self.careNeedShares = []
        self.householdIncomes = []
        self.individualIncomes = []
        self.incomeFrequencies = []
        self.sesPops = []
        self.sesPopsShares = []
        ## Statistical tallies
        self.times = []
        self.pops = []
        self.deaths = 0
        self.births = 0
        self.shareDeaths = 0
        self.shareBirths = 0
        self.avgHouseholdSize = []
        self.marriageTally = 0
        self.numMarriages = []
        self.divorceTally = 0
        self.numDivorces = []
        self.totalCareDemand = []
        self.totalCareSupply = []
        self.informalSocialCareSupply = 0
        self.totalHospitalizationCost = 0
        self.hospitalizationCost = []
        self.numTaxpayers = []
        self.totalUnmetNeed = []
        self.shareUnmetNeed = []
        self.totalFamilyCare = []
        self.inHouseInformalCare = 0
        self.totalTaxBurden = []
        self.marriageProp = []
        self.shareLoneParents = []
        self.shareFemaleLoneParents = []
        self.employmentRate = []
        self.shareWorkingHours = []
        self.publicCareProvision = []
        self.publicSocialCare = 0
        self.publicCareExpenses = 0
        self.costPublicSocialCare = 0
        self.grossDomesticProduct = 0
        self.costTaxFreeSocialCare = 0
        self.costTaxFreeChildCare = 0
        self.costPublicChildCare = 0
        self.publicChildCare = 0
        self.sharePublicSocialCare = 0
        self.sharePublicChildCare = 0
        self.stateTaxRevenue = []
        self.totalTaxRevenue = 0
        self.statePensionRevenue = []
        self.totalPensionRevenue = 0
        self.statePensionExpenditure = []
        self.pensionExpenditure = 0
        
        self.preEdinburghers = []
        self.postEdinburgers = []
        self.preGlaswegians = []
        self.postGlaswegians = []
        self.preAberdonians = []
        self.postAberdonians = []
        
        self.popEdinburgh = 0
        self.popGlasgow = 0
        self.popAberdeedn = 0
        
        self.fromEdinburgh = 0
        self.toEdinburgh = 0
        self.fromGlasgow = 0
        self.toGlasgow = 0
        self.fromAberdeedn = 0
        self.toAberdeen = 0
        
        self.share_fromEdinburgh = 0
        self.share_toEdinburgh = 0
        self.share_fromGlasgow = 0
        self.share_toGlasgow = 0
        self.share_fromAberdeedn = 0
        self.share_toAberdeen = 0
        
        ## Counters and storage
        self.year = self.p['startYear']
        self.pyramid = PopPyramid(self.p['num5YearAgeClasses'],
                                  self.p['numCareLevels'])
        self.textUpdateList = []
        
        self.socialCareNetwork = nx.DiGraph()

        # if self.p['interactiveGraphics']:
#        self.window = Tkinter.Tk()
#        self.canvas = Tkinter.Canvas(self.window,
#                                width=self.p['screenWidth'],
#                                height=self.p['screenHeight'],
#                                background=self.p['bgColour'])


    def run(self, policy, policyParams, seed):
        """Run the simulation from year start to year end."""

        #pprint.pprint(self.p)
        #raw_input("Happy with these parameters?  Press enter to run.")
        self.randSeed = seed
        random.seed(self.randSeed)
        np.random.seed(self.randSeed)

        self.initializePop()
        
        if self.p['interactiveGraphics']:
            self.initializeCanvas()     
            
        # Save policy parameters in Policy folder
        policyFolder = self.folder + '/Policy_' + str(policy)
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        filePath = policyFolder + '/policyParameters.csv'
        c = policyParams.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filePath, "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        if policy == 0:
            startYear = int(self.p['startYear'])
        else:
            startYear = int(self.p['policyStartYear'])
        
        
        startSim = time.time()
        
        dataHouseholdFolder = os.path.join(policyFolder, 'DataHousehold')
        if not os.path.exists(dataHouseholdFolder):
            os.makedirs(dataHouseholdFolder)
        
        dataMapFolder = os.path.join(policyFolder, 'DataMap')
        if not os.path.exists(dataMapFolder):
            os.makedirs(dataMapFolder)
        
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Log.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.log))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "HouseData.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.houseData))
        
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_0.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_1.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_2.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_3.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_4.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_0.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_1.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_2.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_3.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_4.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
        
        
        for self.year in range(startYear, int(self.p['endYear']+1)):
            
            print 'Policy: ' + str(policy)
            print self.year
            
            if policyParams and self.year == self.p['policyStartYear']:
                keys = policyParams.keys()
                for k in keys[1:]:
                    self.p[k] = policyParams[k]
                
                # From list of agents to list of indexes
                if policy == 0:
                    
                    print 'Saving the simulation....'
                    
                    self.from_Agents_to_IDs()
                    
                    # Save outputs
                    self.outputData = pd.read_csv(policyFolder + '/Outputs.csv')
                    self.outputData.to_csv(policyFolder + '/tempOutputs.csv', index=False)
                    # Save simulation
                    pickle.dump(self.pop, open(policyFolder + '/save.p', 'wb'))
                    pickle.dump(self.map, open(policyFolder + '/save.m', 'wb'))
                
                # Upload simulation
                print 'Uploading the simulation....'
                
                self.pop = pickle.load(open(self.folder + '/Policy_0/save.p', 'rb'))
                self.map = pickle.load(open(self.folder + '/Policy_0/save.m', 'rb'))
                
                self.from_IDs_to_Agents()
                
                # Upload outputs
                if policy != 0:
                    self.outputData = pd.read_csv(self.folder + '/Policy_0/tempOutputs.csv')
                    self.outputData.to_csv(policyFolder + '/Outputs.csv', index=False)
      
            self.doOneYear(policyFolder, dataMapFolder, dataHouseholdFolder)
            
#            self.from_Agents_to_IDs()
#            pickle.dump(self.pop, open('Canvas_Pop/save.p_'+str(self.year), 'wb'))
#            pickle.dump(self.map, open('Canvas_Map/save.m_'+str(self.year), 'wb'))
#            self.from_IDs_to_Agents()
          
            print ''
            
        endSim = time.time()
        
        simulationTime = endSim - startSim
        
        print 'Simulation time: ' + str(simulationTime)
        
        if self.p['singleRunGraphs']:
            self.doGraphs()
    
        if self.p['interactiveGraphics']:
            print "Entering main loop to hold graphics up there."
            self.window.mainloop()

        return self.totalTaxBurden[-1]


    def initializePop(self):
        """
        Set up the initial population and the map.
        We may want to do this from scratch, and we may want to do it
        by loading things from a pre-generated file.
        """
        
        self.popData = pd.read_csv("Population_Scotland.txt", header=None, names = ['year', 'age', 'female', 'male', 'total'], delim_whitespace=True)
        
        self.scotlandMap = pd.read_csv("scotlandMap.csv", header=None, names = ['town', 'pop', 'x', 'y', 'lha_1', 'lha_2', 'lha_3', 'lha_4'], delim_whitespace=False)
        
        self.initialPop = sum(self.popData[self.popData.year == self.p['startYear']]['total'])
        
        # Format pop column
        valid = '1234567890.'
        def sanitize(data):
            return float(''.join(filter(lambda char: char in valid, data)))
        pop = np.array(self.scotlandMap['pop'].apply(sanitize))
        self.scotlandMap['pop'] = pop
        
        # Create Scotland 20x25 grid from towns' map
        # The population of each cell is the sum of the populations of the towns with those coordinates
        self.scotlandGrid = pd.DataFrame(columns = ['cell', 'town_x', 'town_y', 'pop', 'lha_1', 'lha_2', 'lha_3', 'lha_4'])
        numCell = 0
        for i in range(int(self.p['mapGridXDimension'])):
            for j in range(int(self.p['mapGridYDimension'])):
                popCell = 0
                lha_1 = 0
                lha_2 = 0
                lha_3 = 0
                lha_4 = 0
                for index, row in self.scotlandMap.iterrows():
                    if row['x'] == i and row['y'] == j:
                        popCell += row['pop']
                    if popCell > 0 and lha_1 != 0:
                        lha_1 = row['lha_1']
                        lha_2 = row['lha_2']
                        lha_3 = row['lha_3']
                        lha_4 = row['lha_4']
                self.scotlandGrid.loc[numCell] = [numCell, i, j, popCell, lha_1, lha_2, lha_3, lha_4]
                numCell += 1
                

        if self.p['loadFromFile'] == False:
            self.map = Map(self.p['mapGridXDimension'],
                           self.p['mapGridYDimension'],
                           self.p['townGridDimension'],
                           self.scotlandGrid)
        else:
            self.map = pickle.load(open("initMap.txt","rb"))

        
        
        ## Now the people who will live on it

        if self.p['loadFromFile'] == False:
            self.pop = Population(self.p['initialPop'],
                                  self.p['startYear'],
                                  self.p['minStartAge'],
                                  self.p['maxStartAge'],
                                  self.p['workingAge'],
                                  self.p['incomeInitialLevels'],
                                  self.p['incomeFinalLevels'],
                                  self.p['incomeGrowthRate'],
                                  self.p['workDiscountingTime'],
                                  self.p['wageVar'],
                                  self.p['weeklyHours'][0])
            ## Now put the people into some houses
            ## They've already been partnered up so put the men in first, then women to follow
            men = [x for x in self.pop.allPeople if x.sex == 'male']

            remainingHouses = []
            remainingHouses.extend(self.map.allHouses)
        
            for man in men:
                man.house = random.choice(remainingHouses)
                self.map.occupiedHouses.append(man.house)            
                remainingHouses.remove(man.house)
                woman = man.partner
                woman.house = man.house
                man.yearMarried.append(int(self.p['startYear']))
                woman.yearMarried.append(int(self.p['startYear']))
                man.house.occupants.append(man)
                man.house.occupants.append(woman)

        else:
            self.pop = pickle.load(open("initPop.txt","rb"))

        ## Choose one house to be the display house
        self.displayHouse = self.pop.allPeople[0].house
        self.displayHouse.display = True
        self.nextDisplayHouse = None

        #reading JH's fertility projections from a CSV into a numpy array
        self.fert_data = np.genfromtxt('birthRates.csv', skip_header=0, delimiter=',')

        #reading JH's fertility projections from two CSVs into two numpy arrays
        self.death_female = np.genfromtxt('female_deathRates.csv', skip_header=0, delimiter=',')
        self.death_male = np.genfromtxt('male_DeathRates.csv', skip_header=0, delimiter=',')
        
        self.incomeDistribution = np.genfromtxt('incomeDistribution.csv', skip_header=0, delimiter=',')
        
        self.incomesPercentiles = np.genfromtxt('incomesPercentiles.csv', skip_header=0, delimiter=',')
        
        self.wealthPercentiles = np.genfromtxt('wealthDistribution.csv', skip_header=0, delimiter=',')
    
        # Assign wealth
        self.updateWealth()
        
    def from_Agents_to_IDs(self):
        for person in self.pop.allPeople:
            if person.mother != None:
                person.motherID = person.mother.id
            else:
                person.motherID = -1
            if person.father != None:
                person.fatherID = person.father.id
            else:
                person.fatherID = -1
            person.childrenID = [x.id for x in person.children]
            person.houseID = person.house.id
            person.mother = None
            person.father = None
            person.children = []
            person.house = None
        
        for house in self.map.allHouses:
            house.occupantsID = [x.id for x in house.occupants]
            house.occupants = []
            
        for town in self.map.towns:
            town.neighborsIDs = [x.id for x in town.neighboringTowns]
            town.neighboringTowns = []
        
    def from_IDs_to_Agents(self):
        for person in self.pop.allPeople:
            if person.motherID != -1:
                person.mother = [x for x in self.pop.allPeople if x.id == person.motherID][0]
            else:
                person.mother = None
            if person.fatherID != -1:
                person.father = [x for x in self.pop.allPeople if x.id == person.fatherID][0]
            else:
                person.father = None
                
            person.children = [x for x in self.pop.allPeople if x.id in person.childrenID]
            
        for person in self.pop.allPeople:
            person.house = [x for x in self.map.allHouses if x.id == person.houseID][0]
            if person in self.pop.livingPeople:
                person.house.occupants.append(person)
        
        for town in self.map.towns:
            town.neighboringTowns = [x for x in self.map.towns if x.id in town.neighborsIDs]
    

    def doOneYear(self, policyFolder, dataMapFolder, dataHouseholdFolder):
        """Run one year of simulated time."""

        ##print "Sim Year: ", self.year, "OH count:", len(self.map.occupiedHouses), "H count:", len(self.map.allHouses)
      
        startYear = time.time()
        
        
        # print 'Doing fucntion 1...'
        
        self.computeClassShares()
        
        # print 'Doing fucntion 2...'
      
        ###################   Do Deaths   #############################
      
        self.doDeaths(policyFolder)
        
        # print 'Doing fucntion 3...'
        
        ###################   Do Care Transitions   ##########################
        
        # self.doCareTransitions()
        
        # print 'Doing fucntion 4...'
        
        self.doCareTransitions_UCN(policyFolder)
        
        # print 'Doing fucntion 5...'
        
 # Temporarily shutting down social care provision
 
 
        self.startCareAllocation()
        
        self.allocateChildCare() 
       
        self.allocateSocialCare_Ind()
        
        self.updateUnmetCareNeed()
        
        
        # print 'Doing fucntion 9...'
        
        self.doAgeTransitions(policyFolder)
        
      
        self.doBirths(policyFolder)
        
        # print 'Doing fucntion 11...'
  
        self.updateIncome()
        
        # print 'Doing fucntion 12...'
        
        # self.updateWealth()
        
        self.updateWealth_Ind()
      
        # print 'Doing fucntion 13...'
        
        # self.doSocialTransition_TD()
        
        self.doSocialTransition(policyFolder)
        
        
        self.migrationStats_Pre()
        
        # print 'Doing fucntion 14...'
        
        self.doDivorces(policyFolder)
        
        # print 'Doing fucntion 15...'
        
        self.doMarriages(policyFolder)
        
        # print 'Doing fucntion 16...'
    
        
        self.doMovingAround(policyFolder)
        
        
        self.migrationStats_Post()
        # self.householdRelocation(policyFolder)
        
        # print 'Doing fucntion 17...'
        
#        self.pyramid.update(self.year, self.p['num5YearAgeClasses'], self.p['numCareLevels'],
#                            self.p['pixelsInPopPyramid'], self.pop.livingPeople)
        
        
        # print 'Doing fucntion 18...'
        
        self.healthCareCost()
        
        # print 'Doing fucntion 19...'
        
        self.doStats(policyFolder, dataMapFolder, dataHouseholdFolder)
        
        if (self.p['interactiveGraphics']):
            self.updateCanvas()
            
        endYear = time.time()
        
        print 'Year execution time: ' + str(endYear - startYear)

            
####################   doDeath - SES version    ################################################
    def computeClassShares(self):
        
        self.socialClassShares[:] = []
        self.careNeedShares[:] = []
        peopleWithRank = [x for x in self.pop.livingPeople if x.classRank != -1]
        numPop = float(len(peopleWithRank))
        for c in range(int(self.p['numberClasses'])):
            classPop = [x for x in peopleWithRank if x.classRank == c]
            numclassPop = float(len(classPop))
            self.socialClassShares.append(numclassPop/numPop)
            
            needShares = []
            for b in range(int(self.p['numCareLevels'])):
                needPop = [x for x in classPop if x.careNeedLevel == b]
                numNeedPop = float(len(needPop))
                if numclassPop > 0:
                    needShares.append(numNeedPop/numclassPop)
                else:
                    needShares.append(0.0)
            self.careNeedShares.append(needShares)    
            
        print self.socialClassShares
    
    def deathProb(self, baseRate, person):  ##, shareUnmetNeed, classPop):
        
        classRank = person.classRank
        if person.status == 'child' or person.status == 'student':
            classRank = person.parentsClassRank
        
        if person.sex == 'male':
            mortalityBias = self.p['maleMortalityBias']
        else:
            mortalityBias = self.p['femaleMortalityBias']
        
        deathProb = baseRate
        
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(mortalityBias, i)
            
        if a > 0:
            
            lowClassRate = baseRate/a
            
            classRate = lowClassRate*math.pow(mortalityBias, classRank)
            
            deathProb = classRate
           
            b = 0
            for i in range(int(self.p['numCareLevels'])):
                b += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
                
            if b > 0:
                
                higherNeedRate = classRate/b
               
                deathProb = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - person.careNeedLevel) # deathProb
      
        # Add the effect of unmet care need on mortality rate for each care need level
        
        ##### Temporarily by-passing the effect of Unmet Care Need   #############
        
#        a = 0
#        for x in classPop:
#            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
#        higherUnmetNeed = (classRate*len(classPop))/a
#        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
        return deathProb
    
    def deathProb_UCN(self, baseRate, sex, classRank, needLevel, shareUnmetNeed, classPop):
        
        if sex == 'male':
            mortalityBias = self.p['maleMortalityBias']
        else:
            mortalityBias = self.p['femaleMortalityBias']
        
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow( mortalityBias, i)
        lowClassRate = baseRate/a
        
        classRate = lowClassRate*math.pow(mortalityBias, classRank)
       
        a = 0
        for i in range(self.p['numCareLevels']):
            a += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
        higherNeedRate = classRate/a
       
        classRate = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - needLevel) # deathProb
      
        # Add the effect of unmet care need on mortality rate for each care need level
        
        ##### Temporarily by-passing the effect of Unmet Care Need   #############
        
        a = 0
        for x in classPop:
            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
        higherUnmetNeed = (classRate*len(classPop))/a
        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
        return deathProb
    
    def doDeaths(self, policyFolder):
        
        preDeath = len(self.pop.livingPeople)
        
        deaths = [0, 0, 0, 0, 0]
        """Consider the possibility of death for each person in the sim."""
        for person in self.pop.livingPeople:
            age = person.age
            
            ####     Death process with histroical data  after 1950   ##################
            if self.year >= self.p['mortalityDataFrom']:
                if age > 110:
                    age = 110
                if person.sex == 'male':
                    rawRate = self.death_male[age, self.year-int(self.p['mortalityDataFrom'])]
                if person.sex == 'female':
                    rawRate = self.death_female[age, self.year-int(self.p['mortalityDataFrom'])]
                    
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                
                dieProb = self.deathProb(rawRate, person)
                
                person.lifeExpectancy = max(90-person.age, 5)
                # dieProb = self.deathProb_UCN(rawRate, person, person.averageShareUnmetNeed, classPop)

            #############################################################################
            
                if random.random() < dieProb:
                    person.dead = True
                    person.deadYear = self.year
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                
            else: 
                #######   Death process with made-up rates  ######################
                babyDieProb = 0.0
                if age < 1:
                    babyDieProb = self.p['babyDieProb']
                if person.sex == 'male':
                    ageDieProb = (math.exp(age/self.p['maleAgeScaling']))*self.p['maleAgeDieProb'] 
                else:
                    ageDieProb = (math.exp(age/self.p['femaleAgeScaling']))* self.p['femaleAgeDieProb']
                rawRate = self.p['baseDieProb'] + babyDieProb + ageDieProb
                
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                
                dieProb = self.deathProb(rawRate, person)
                
                person.lifeExpectancy = max(90-person.age, 5)
                #### Temporarily by-passing the effect of unmet care need   ######
                # dieProb = self.deathProb_UCN(rawRate, person.parentsClassRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                if random.random() < dieProb:
                    person.dead = True
                    person.deadYear = self.year
                    deaths[person.classRank] += 1
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
        
                  
                  
        self.pop.livingPeople[:] = [x for x in self.pop.livingPeople if x.dead == False]
        
        postDeath = len(self.pop.livingPeople)
        
        self.deaths = preDeath - postDeath
        self.shareDeaths = float(self.deaths)/float(postDeath+self.deaths)
        
        print('the number of deaths is: ' + str(preDeath - postDeath))            

    def doCareTransitions(self, policyFolder):
        """Consider the possibility of each person coming to require care."""
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        for person in peopleNotInCriticalCare:
            age = self.year - person.birthdate
            if person.sex == 'male':
                ageCareProb = ( ( math.exp( age /
                                            self.p['maleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            else:
                ageCareProb = ( ( math.exp( age /
                                           self.p['femaleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            careProb = self.p['baseCareProb'] + ageCareProb
            
            if random.random() < careProb:
                multiStepTransition = random.random()
                if multiStepTransition < self.p['cdfCareTransition'][0]:
                    person.careNeedLevel += 1
                elif multiStepTransition < self.p['cdfCareTransition'][1]:
                    person.careNeedLevel += 2
                elif multiStepTransition < self.p['cdfCareTransition'][2]:
                    person.careNeedLevel += 3
                else:
                    person.careNeedLevel += 4
                    
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = int(self.p['numCareLevels'] - 1)
                            
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " now has "
                    messageString += self.p['careLevelNames'][int(person.careNeedLevel)] + " care needs." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
    

           
    def doCareTransitions_UCN(self, policyFolder):
        """Consider the possibility of each person coming to require care."""
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        for person in peopleNotInCriticalCare:
            age = self.year - person.birthdate
            if person.sex == 'male':
                ageCareProb = ( ( math.exp( age /
                                            self.p['maleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            else:
                ageCareProb = ( ( math.exp( age /
                                           self.p['femaleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            baseProb = self.p['baseCareProb'] + ageCareProb
            
            baseProb = self.baseRate(self.p['careBias'], baseProb)
            
            unmetNeedFactor = 1.0/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
            
            
            classRank = person.classRank
            if person.status == 'child' or person.status == 'student':
                classRank = person.parentsClassRank
            
            careProb = baseProb*math.pow(self.p['careBias'], classRank)/unmetNeedFactor 
            
            
            #### Alternative prob which depends on care level and unmet care need   #####################################
            # careProb = baseProb # baseProb*math.pow(self.p['careBias'], person.classRank)/unmetNeedFactor
            
            
            if np.random.random() < careProb:
                baseTransition = self.baseRate(self.p['careBias'], 1.0-self.p['careTransitionRate'])
                if baseTransition >= 1.0:
                    print 'Error: base transition >= 1'
                    # sys.exit()
                    
                    
                if person.careNeedLevel > 0:
                    unmetNeedFactor = 1.0/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
                else:
                    unmetNeedFactor = 1.0
                transitionRate = (1.0 - baseTransition*math.pow(self.p['careBias'], classRank))*unmetNeedFactor
                
                stepCare = 1
                bound = transitionRate
                
                while np.random.random() > bound and stepCare < self.p['numCareLevels'] - 1:
                    stepCare += 1
                    bound += (1.0-bound)*transitionRate
                person.careNeedLevel += stepCare
                    
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = int(self.p['numCareLevels'] - 1)
                if person.careNeedLevel > 1:
                    person.wage = 0
                            
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " now has "
                    messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
    
    def baseRate(self, bias, cp):
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(bias, i)
        baseRate = cp/a
        return (baseRate)
    
    def updateUnmetCareNeed(self):
        
        for house in self.map.occupiedHouses:
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in house.occupants])
            house.careNetwork.clear()
            house.suppliers[:] = []
            house.demandNetwork.clear()
            house.receivers[:] = []
        
        for person in self.pop.livingPeople:
            person.careNetwork.clear()
            person.suppliers[:] = []
            if person.careNeedLevel > 0:
                person.cumulativeUnmetNeed *= self.p['unmetCareNeedDiscountParam']
                person.cumulativeUnmetNeed += person.unmetSocialCareNeed
                person.totalDiscountedShareUnmetNeed *= self.p['shareUnmetNeedDiscountParam']
                person.totalDiscountedTime *= self.p['shareUnmetNeedDiscountParam']
                person.totalDiscountedShareUnmetNeed += person.unmetSocialCareNeed/person.hoursSocialCareDemand
                person.totalDiscountedTime += 1
                person.averageShareUnmetNeed = person.totalDiscountedShareUnmetNeed/person.totalDiscountedTime
    
    
    def startCareAllocation(self):
        # print 'Doing fucntion 5-a...'
        self.resetCareVariables_KN()
        # print 'Doing fucntion 5-b...'
        
        # print 'Doing fucntion 5.c...'
        self.computeSocialCareNeeds_Scot() # self.computeSocialCareNeeds_W() if social care paid with wealth
        # print 'Doing fucntion 5.d...'
        self.computeChildCareNeeds()
        # print 'Doing fucntion 5-e...'
        self.householdCareSupply()
        
        self.householdCareNetwork()
        
        self.computeNetCareDemand()
        
        # self.computeTownAttractiveness()
        
        
    def allocateChildCare(self):
        
        self.costTaxFreeChildCare = 0

        receivers = [x for x in self.map.occupiedHouses if x.totalChildCareNeed > 0]
        for receiver in receivers:
            self.computeChildCareNetworkSupply(receiver)
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        while len(residualReceivers) > 0:
    
            #################    Check if transfer is done: Pre need and supply   ######################################
            
            preChildCareNeed = sum([x.totalChildCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            #########################################################################################
            
            # An household is selected depending on total child care need
            childCareNeeds = [x.totalChildCareNeed for x in residualReceivers]
            probReceivers = [i/sum(childCareNeeds) for i in childCareNeeds]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
#            print 'High price care: ' + str(receiver.highPriceChildCare)
#            print 'Low price care: ' + str(receiver.lowPriceChildCare)
#            
#            if receiver.highPriceChildCare + receiver.lowPriceChildCare == 0:
#                print 'Error: receiver has not child care!'
#                sys.exit()
#            
#            print ''
            
            ###    Individual check   ##########################
            
            preReceiverCareNeed = receiver.totalChildCareNeed
            
            ###########################################################
            case = 0
            
            income = self.computeHouseholdIncome(receiver)
            # print 'Household income: ' + str(income)
            residualIncome = receiver.residualIncomeForChildCare
            
#            if int(receiver.residualIncomeForChildCare) > int(self.computeHouseholdIncome(receiver)):
#                print 'Error: residual income greater than income (1)'
#                print receiver.residualIncomeForChildCare
#                print self.computeHouseholdIncome(receiver)
#                print receiver.householdFormalSupplyCost
#                print receiver.initialResidualIncomeForChildCare
#                
#                for x in receiver.occupants:
#                    print x.status
#                    print x.careNeedLevel
#                    print x.potentialIncome
#                    print x.residualWorkingHours
#                    print x.income
#                
#                sys.exit()
                
            # print 'Residual Income for child care: ' + str(residualIncome) 
            childcareExpense = receiver.householdFormalSupplyCost
            # print 'Childcare expense: ' + str(childcareExpense)
            total = residualIncome+childcareExpense
            # print 'Total: ' + str(total)
            
#            if int(income) != int(total):
#                print 'Error receiver'
#                print receiver.id
#                print receiver.totalChildCareNeed
#                print receiver.highPriceChildCare
#                print receiver.lowPriceChildCare
#                print sum(receiver.networkInformalSupplies)
#                if receiver.totalSocialCareNeed > 0:
#                    print sum(receiver.networkInformalSupplies)/receiver.totalSocialCareNeed
#                print 'Household income: ' + str(income)
#                print 'Residual Income for child care: ' + str(residualIncome) 
#                print 'Childcare expense: ' + str(childcareExpense)
#                print 'Total: ' + str(total)
#                print receiver.networkSupply
#                for x in receiver.occupants:
#                    print x.status
#                    print x.careNeedLevel
#                    if x.status == 'worker':
#                        print x.potentialIncome
#                        print x.residualWorkingHours
#                    print x.income
#                sys.exit()
            
            
            if receiver.highPriceChildCare > 0:
            # If the receiver has childcare need more expensive than social care, it will try to satisfy it with informal care. 
            # Only if there in no enough informal care the formal care will be suppllied.
            # Therefore, the supplier will be chosen according to the informal care availability, and only if there is no informal care availability left,
            # it will be chosen according to the formal care availability.
                # Select a supplier based on availability of informal supply.
                if sum(receiver.networkInformalSupplies) > 0:
                    # A supplier is selected based on informal care availability
                    probSuppliers = [i/sum(receiver.networkInformalSupplies) for i in receiver.networkInformalSupplies]
                    supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
                    
                    case = 1
#                    print 'tranfer child care: formal (1)'
#                    print sum(receiver.networkInformalSupplies)
                    
                    self.transferInformalChildCare(receiver, supplier)
                    
                    
                elif receiver.formalChildCareSupply > 0:
                    supplier = receiver
                    # Formal supply: the supplier can only be the household itself.
                    case = 2
#                    print 'tranfer child care: formal (2)'
#                    print receiver.formalChildCareSupply
                    
                    self.outOfIncomeChildCare(receiver)
                    
                    
                    
            elif receiver.lowPriceChildCare > 0:
                # In this case, a random selection based on relative availability will be done until the ratio between 
                # the available informal care and the household's social care is above 1, i.e. there is enough informal care.
                # As the ratio goes below 1, only out-of-income care will be supplied.
                totalCare = sum(receiver.networkInformalSupplies) + receiver.formalChildCareSupply
                typesOfCare = ['informal care', 'formal care']
                if totalCare > 0:
                    probInformalCare = max(sum(receiver.networkInformalSupplies)-receiver.totalUnmetSocialCareNeed, 0)/totalCare
                    probs = [probInformalCare, 1-probInformalCare]
                    # print 'Care probs: ' + str(probs)
                    # print 'Formal supply: ' + str(receiver.formalChildCareSupply)
                    care = np.random.choice(typesOfCare, p = probs)
                    if receiver.formalChildCareSupply == 0 or care == 'informal care':
                        probSuppliers = [i/sum(receiver.networkInformalSupplies) for i in receiver.networkInformalSupplies]
                        supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
                    
                        case = self.transferInformalChildCare(receiver, supplier)
                    else:
                        supplier = receiver
                        case = 5
                        self.outOfIncomeChildCare(receiver)
#            else:
#                
#                print 'Error: receiver does not have child care need'
#                sys.exit()
                    
             ###    Individual check   ##########################
             
#            if case == 0:
#                print 'Error: no allocation function called!'
#                sys.exit()
            
            postReceiverCareNeed = receiver.totalChildCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print case
                print 'Error: child care iteration withount allocation!'
                # sys.exit()
            
            ########################################################### 
        
            receivers = [x for x in self.map.occupiedHouses if x.totalChildCareNeed > 0]
            
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateChildCareNetworkSupply(otherReceiver, supplier, 4)
           
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postChildCareNeed = sum([x.totalChildCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            # print [x.totalChildCareNeed for x in residualReceivers]
            
            
#            print postChildCareNeed
#            print preChildCareNeed
#            print ''
            if postChildCareNeed >= preChildCareNeed:
                print 'Error: child care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
            
#        if self.year == 1862:
#            sys.exit()
        
    def allocateSocialCare(self):
        
        self.inHouseInformalCare = 0
        
        self.computeResidualIncomeForSocialCare() # self.computeResidualIncomeForSocialCare()
        
        # self.householdCareNetwork_netSupply()
        
        receivers = [x for x in self.map.occupiedHouses if x.totalUnmetSocialCareNeed > 0]
        for receiver in receivers:
            self.computeSocialCareNetworkSupply_W(receiver) ###  Add social care from wealth.....
            
            #######    Temporarily excluding out-of-wealth care   ##########
            # self.computeSocialCareNetworkSupply_W(receiver)
            
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        
        
        while len(residualReceivers) > 0:
            
            #################    Check if transfer is done: Pre need and supply   ######################################
            
            preSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            #########################################################################################
            
            
            socialCareNeeds = [x.totalUnmetSocialCareNeed for x in residualReceivers]
            probReceivers = [i/sum(socialCareNeeds) for i in socialCareNeeds]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            if self.socialCareNetwork.has_node(receiver) == False:
                self.socialCareNetwork.add_node(receiver, internalSupply = 0)
            
            ###    Individual check   ##########################
            
            preReceiverCareNeed = receiver.totalUnmetSocialCareNeed
            
            ###########################################################
            suppliersWeights = []
            for supplier in receiver.suppliers:
                indexSupplier = receiver.suppliers.index(supplier)
                informalSupply = receiver.networkInformalSupplies[indexSupplier]
                formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
                careFromWealth = 0
                if receiver == supplier:
                    careFromWealth = receiver.careSupplyFromWealth
                totalFormaCare = formalSocialCare + careFromWealth
                informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
                formalFactor = math.pow(totalFormaCare, (1-self.p['betaInformalCare']))
                suppliersWeights.append(informalFactor+formalFactor)
            
            probSuppliers = [i/sum(suppliersWeights) for i in suppliersWeights]
            
            
            supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
            
            if self.socialCareNetwork.has_node(supplier) == False:
                self.socialCareNetwork.add_node(supplier, internalSupply = 0)
            
            if self.socialCareNetwork.has_edge(receiver, supplier) == False:
                self.socialCareNetwork.add_edge(receiver, supplier, careTransferred = 0)
        
            self.transferSocialCare_W(receiver, supplier) # self.transferSocialCare(receiver, supplier)
            
            ###    Individual check   ##########################
            
            postReceiverCareNeed = receiver.totalUnmetSocialCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print 'Error: social care iteration withount allocation!'
                sys.exit()
            
            ########################################################### 
            
            receivers = [x for x in self.map.occupiedHouses if x.totalUnmetSocialCareNeed > 0]
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateSocialCareNetworkSupply_W(otherReceiver, supplier, 0) # self.updateSocialCareNetworkSupply(receiver, supplier, 0)
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
        
            if postSocialCareNeed >= preSocialCareNeed:
                print 'Error: social care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
    
    
    def allocateSocialCare_Ind(self):
        
        self.inHouseInformalCare = 0
        
        self.computeResidualIncomeForSocialCare()
        
        receivers = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
        for receiver in receivers:
            self.computeSocialCareNetworkSupply_Ind(receiver)
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        while len(residualReceivers) > 0:
            
            #################    Check if transfer is done: Pre need and supply   ######################################
            
            preSocialCareNeed = sum([x.unmetSocialCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            #########################################################################################
            
            
            socialCareNeeds = [x.unmetSocialCareNeed for x in residualReceivers]
            probReceivers = [i/sum(socialCareNeeds) for i in socialCareNeeds]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            if self.socialCareNetwork.has_node(receiver) == False:
                self.socialCareNetwork.add_node(receiver, internalSupply = 0)
            
            ###    Individual check   ##########################
            
            preReceiverCareNeed = receiver.unmetSocialCareNeed
            
            ###########################################################
            suppliersWeights = list(receiver.weightedTotalSupplies)
            potentialSuppliers = list(receiver.suppliers)
            suppliersWeights.append(receiver.careSupplyFromWealth)
            potentialSuppliers.append(receiver)
            
            probSuppliers = [i/sum(suppliersWeights) for i in suppliersWeights]
            supplier = np.random.choice(potentialSuppliers, p = probSuppliers)
            
            if self.socialCareNetwork.has_node(supplier) == False:
                self.socialCareNetwork.add_node(supplier, internalSupply = 0)
            
            if self.socialCareNetwork.has_edge(receiver, supplier) == False:
                self.socialCareNetwork.add_edge(receiver, supplier, careTransferred = 0)
        
            self.transferSocialCare_Ind(receiver, supplier) # self.transferSocialCare(receiver, supplier)
            
            ###    Individual check   ##########################
            
            postReceiverCareNeed = receiver.unmetSocialCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print 'Error: social care iteration withount allocation!'
                sys.exit()
            
            ########################################################### 
            
            receivers = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateSocialCareNetworkSupply_Ind(otherReceiver, supplier, 0) # self.updateSocialCareNetworkSupply(receiver, supplier, 0)
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postSocialCareNeed = sum([x.unmetSocialCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
        
            if postSocialCareNeed >= preSocialCareNeed:
                print 'Error: social care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
    
    
    def transferSocialCare(self, receiver, supplier):
        
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        indexSupplier = receiver.suppliers.index(supplier)
        informalSupply = receiver.networkInformalSupplies[indexSupplier]
        formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
        
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'out-of-income care'] # Add an 'out-of-wealth' care............
        care = 'out-of-income care'
        if supplier.town in receiver.town.neighboringTowns:
            careWeights = [informalSupply, formalSocialCare]
            careProbs = [x/sum(careWeights) for x in careWeights]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        if care == 'informal care':
        
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # If informal care is provided, it satisfies the most expensive cumulated child care need.
            for member in householdCarers:
                member.residualInformalSupply = member.residualInformalSupplies[distance]
            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed)
            if residualCare < 1.0:
                residualCare = 1.0
            
            careTransferred = 0
            for i in householdCarers:
                careForNeed = min(i.residualInformalSupply, residualCare)
                if careForNeed < 1.0:
                    careForNeed = 1.0
                if i in receiver.occupants and careForNeed > 0:
                    i.careForFamily = True
                i.socialWork += careForNeed
                if careForNeed > 0:
                    for j in range(4):
                        i.residualInformalSupplies[j] -= careForNeed
                        i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                    careTransferred += careForNeed
                    residualCare -= careForNeed
                    if residualCare <= 0:
                        break
                    
            if receiver == supplier:
                self.inHouseInformalCare += careTransferred
                
            if  receiver != supplier:
                receiver.networkSupport += careTransferred
            
            receiverOccupants = list(receiver.occupants)
            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
            residualCare = careTransferred
            for person in careTakers:
                personalCare = min(person.unmetSocialCareNeed, residualCare)
                person.unmetSocialCareNeed -= personalCare
                person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                person.informalSocialCareReceived += personalCare
                residualCare -= personalCare
                if residualCare <= 0:
                    break
            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
            receiver.informalSocialCareReceived += careTransferred
            
            self.updateSocialCareNetworkSupply(receiver, supplier, 1)
            
        elif care == 'out-of-income care':
            household = list(supplier.occupants)
            employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
            
            maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed, maxFormalCare)
            if residualCare < 1.0:
                residualCare = 1.0
            
            costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
            priceSocialCare = costQuantumSocialCare/residualCare
            
            if supplier.town not in receiver.town.neighboringTowns or len(employed) == 0: # Only formal care is possible
                
#                print 'Supplier id: ' + str(supplier.id)
#                print 'Pre income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                print 'Cost quantum social care: ' + str(costQuantumSocialCare)
                
                for j in range(4):
                    supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                    supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                supplier.householdFormalSupplyCost += costQuantumSocialCare
                
                careTransferred = 0
                if len(employed) > 0:
                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
                    residualCare = self.p['quantumCare']
                    for worker in employed:
                        maxCare = costQuantumSocialCare/worker.wage
                        workerCare = min(maxCare, residualCare)
                        if workerCare < 1.0:
                            workerCare = 1.0
                        worker.availableWorkingHours -= workerCare
                        worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                        careTransferred += workerCare
                        costQuantumSocialCare -= workerCare*worker.wage
                        residualCare -= workerCare
                        if residualCare <= 0:
                            break
                
                # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                
                receiverOccupants = list(receiver.occupants)                
                careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                residualCare = careTransferred
                for person in careTakers:
                    personalCare = min(person.unmetSocialCareNeed, residualCare)
                    person.unmetSocialCareNeed -= personalCare
                    person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                    person.formalSocialCareReceived += personalCare
                    residualCare -= personalCare
                    if residualCare <= 0:
                        break
                receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                receiver.formalSocialCareReceived += careTransferred
                
                self.updateSocialCareNetworkSupply(receiver, supplier, 2)
                
            else:
                # Select the worker with the lowest pay
                employed.sort(key=operator.attrgetter("wage"))
                
                carer = employed[0]
                if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                    supplier.householdFormalSupplyCost += costQuantumSocialCare
                    
                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
                    careToAllocate = residualCare
                    careTransferred = 0
                    for worker in employed:
                        maxCare = costQuantumSocialCare/worker.wage
                        workerCare = min(maxCare, careToAllocate)
                        if workerCare < 1.0:
                            workerCare = 1.0
                        careTransferred += workerCare
                        worker.availableWorkingHours -= workerCare
                        worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                        costQuantumSocialCare -= workerCare*worker.wage
                        careToAllocate -= workerCare
                        if careToAllocate <= 0:
                            break
                        
                    # employed[0].availableWorkingHours -= costQuantumSocialCare/employed[0].wage
                    # employed[0].availableWorkingHours = max(employed[0].availableWorkingHours, 0)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply(receiver, supplier, 3)
                    
                else: # In this case, it is more convenient to take time off work to provide informal care.
                    print 'Case 4'
                    print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                    
                    if receiver == supplier:
                        self.inHouseInformalCare += self.p['quantumCare']
                    
                    careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours)
                    if careTransferred == 0:
                        print 'No residual working hours in carer'
                        sys.exit()
                    if careTransferred < 1.0:
                        careTransferred = 1.0
                    if carer in receiver.occupants and careTransferred > 0:
                        carer.careForFamily = True
                    incomeForCare = careTransferred*carer.wage
                    carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                    carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
                    carer.residualWorkingHours -= careTransferred
                    carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
                    carer.outOfWorkSocialCare += careTransferred
                    carer.socialWork += careTransferred
                    
                    print 'Care transferred: ' + str(careTransferred)
                    print 'Carer wage: ' + str(carer.wage)
                    print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
                    print 'Pre-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= incomeForCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                        
                    print 'Post-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.informalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.informalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply(receiver, supplier, 4)
            
            
    def transferSocialCare_W(self, receiver, supplier):
        
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        indexSupplier = receiver.suppliers.index(supplier)
        informalSupply = receiver.networkInformalSupplies[indexSupplier]
        formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
        careFromWealth = 0
        if receiver == supplier:
            careFromWealth = receiver.careSupplyFromWealth
        totalFormaCare = formalSocialCare + careFromWealth
        informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
        formalFactor = math.pow(totalFormaCare, (1-self.p['betaInformalCare']))
        probInformalCare = informalFactor/(informalFactor+formalFactor)
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'formal care'] # Add an 'out-of-wealth' care............
        care = 'out-of-income care'
        if supplier.town in receiver.town.neighboringTowns:
            # careWeights = [informalSupply, formalSocialCare, careFromWealth]
            # careProbs = [x/sum(careWeights) for x in careWeights]
            careProbs = [probInformalCare, 1-probInformalCare]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        if care == 'informal care':
            
            
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # If informal care is provided, it satisfies the most expensive cumulated child care need.
            for member in householdCarers:
                member.residualInformalSupply = member.residualInformalSupplies[distance]
            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed)
            if residualCare < 1.0:
                residualCare = 1.0
            
            careTransferred = 0
            for i in householdCarers:
                careForNeed = min(i.residualInformalSupply, residualCare)
                if careForNeed < 1.0:
                    careForNeed = 1.0
                if i in receiver.occupants and careForNeed > 0:
                    i.careForFamily = True
                i.socialWork += careForNeed
                if careForNeed > 0:
                    for j in range(4):
                        i.residualInformalSupplies[j] -= careForNeed
                        i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                    careTransferred += careForNeed
                    residualCare -= careForNeed
                    if residualCare <= 0:
                        break
                    
            if receiver == supplier:
                self.inHouseInformalCare += careTransferred
                
            if  receiver != supplier:
                receiver.networkSupport += careTransferred
                
            if receiver != supplier:
                self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
            else:
                self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred
            
            receiverOccupants = list(receiver.occupants)
            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
            residualCare = careTransferred
            for person in careTakers:
                personalCare = min(person.unmetSocialCareNeed, residualCare)
                person.unmetSocialCareNeed -= personalCare
                person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                person.informalSocialCareReceived += personalCare
                residualCare -= personalCare
                if residualCare <= 0:
                    break
            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
            receiver.informalSocialCareReceived += careTransferred
            
            self.updateSocialCareNetworkSupply_W(receiver, supplier, 1)
            
            
#            if receiver == supplier:
#                self.inHouseInformalCare += self.p['quantumCare']
#                
#            household = list(supplier.occupants)
#            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
#            # If informal care is provided, it satisfies the most expensive cumulated child care need.
#            for member in householdCarers:
#                member.residualInformalSupply = member.residualInformalSupplies[distance]
#            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
#            
#            if  receiver != supplier:
#                receiver.networkSupport += self.p['quantumCare']
#                
#            residualCare = self.p['quantumCare']
#            for i in householdCarers:
#                careForNeed = min(i.residualInformalSupply, residualCare)
#                if i in receiver.occupants and careForNeed > 0:
#                    i.careForFamily = True
#                i.socialWork += careForNeed
#                if careForNeed > 0:
#                    for j in range(4):
#                        i.residualInformalSupplies[j] -= careForNeed
#                        i.residualInformalSupplies[j] = max(i.residualInformalSupplies[j], 0)
#                    residualCare -= careForNeed
#                    if residualCare <= 0:
#                        break
#            
#            if receiver != supplier:
#                self.socialCareNetwork[receiver][supplier]['careTransferred'] += self.p['quantumCare']
#            else:
#                self.socialCareNetwork.node[receiver]['internalSupply'] += self.p['quantumCare']
#            
#            receiverOccupants = list(receiver.occupants)
#            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#            residualCare = self.p['quantumCare']
#            for person in careTakers:
#                personalCare = min(person.unmetSocialCareNeed, residualCare)
#                person.unmetSocialCareNeed -= personalCare
#                person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                person.informalSocialCareReceived += personalCare
#                residualCare -= personalCare
#                if residualCare <= 0:
#                    break
#            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#            receiver.informalSocialCareReceived += self.p['quantumCare']
#            
#            self.updateSocialCareNetworkSupply_W(receiver, supplier, 1)
            
        else: 
        
            household = list(supplier.occupants)
            employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
            
            maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed, maxFormalCare)
            if residualCare < 1.0:
                residualCare = 1.0
            
            costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
            priceSocialCare = costQuantumSocialCare/residualCare
            
            if supplier.town not in receiver.town.neighboringTowns or len(employed) == 0 or formalSocialCare == 0: # Only formal care is possible
                kindsOfCare = ['out-of-income care', 'out-of-wealth care']
                weights = [formalSocialCare, careFromWealth]
                careProbs = [x/sum(weights) for x in weights]
                care = np.random.choice(kindsOfCare, p = careProbs)
                if care == 'out-of-income care':
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                    supplier.householdFormalSupplyCost += costQuantumSocialCare
                    
                    careTransferred = 0
                    if len(employed) > 0:
                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
                        residualCare = self.p['quantumCare']
                        for worker in employed:
                            maxCare = costQuantumSocialCare/worker.wage
                            workerCare = min(maxCare, residualCare)
                            if workerCare < 1.0:
                                workerCare = 1.0
                            worker.availableWorkingHours -= workerCare
                            worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                            worker.incomeExpenses += workerCare*worker.wage
                            careTransferred += workerCare
                            costQuantumSocialCare -= workerCare*worker.wage
                            residualCare -= workerCare
                            if residualCare <= 0:
                                break
                    
                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)                
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                
                
                
#                # Sample out-of-income/out-of-wealth according to quantity
#                kindsOfCare = ['out-of-income care', 'out-of-wealth care']
#                weights = [formalSocialCare, careFromWealth]
#                careProbs = [x/sum(weights) for x in weights]
#                care = np.random.choice(kindsOfCare, p = careProbs)
#                if care == 'out-of-income care':
#                    for j in range(4):
#                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                    supplier.householdFormalSupplyCost += costQuantumSocialCare
#                    
#                    if len(employed) > 0:
#                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                        residualCare = self.p['quantumCare']
#                        for worker in employed:
#                            maxCare = costQuantumSocialCare/worker.wage
#                            workerCare = min(maxCare, residualCare)
#                            worker.availableWorkingHours -= workerCare
#                            worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                            costQuantumSocialCare -= workerCare*worker.wage
#                        
#                            worker.careExpenses += workerCare*worker.wage
#                            
#                            residualCare -= workerCare
#                            if residualCare <= 0:
#                                break
#                    
#                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                    
#                    receiverOccupants = list(receiver.occupants)                
#                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for person in careTakers:
#                        personalCare = min(person.unmetSocialCareNeed, residualCare)
#                        person.unmetSocialCareNeed -= personalCare
#                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                        person.formalSocialCareReceived += personalCare
#                        residualCare -= personalCare
#                        if residualCare <= 0:
#                            break
#                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                    receiver.formalSocialCareReceived += self.p['quantumCare']
#                    
#                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                    
                else:
                    household = list(supplier.occupants)
                    householdCarers = [x for x in household if x.wealthForCare > 0]
                    householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
                    maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])) for x in householdCarers]))
                    residualCare = maxSupply
                    careSupplied = 0
                    for i in householdCarers:
                        careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])), residualCare)
                        if i in receiver.occupants and careForNeed > 0:
                            i.careForFamily = True
                        i.socialWork += careForNeed
                        if careForNeed > 0:
                            
                            i.wealthForCare -= careForNeed*self.p['priceSocialCare']
                            i.wealthForCare = max(i.wealthForCare, 0)
                            # i.financialWealth -= careForNeed*self.p['priceSocialCare']
                            # i.financialWealth = max(i.financialWealth, 0)
                            i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
                            i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
                            careSupplied += careForNeed
                            residualCare -= careForNeed
                            if residualCare <= 0:
                                break
                            
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careSupplied
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += self.p['quantumCare']
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
#                for j in range(4):
#                    supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                    supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                supplier.householdFormalSupplyCost += costQuantumSocialCare
#                
#                if len(employed) > 0:
#                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for worker in employed:
#                        maxCare = costQuantumSocialCare/worker.wage
#                        workerCare = min(maxCare, residualCare)
#                        worker.availableWorkingHours -= workerCare
#                        worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                        costQuantumSocialCare -= workerCare*worker.wage
#                        residualCare -= workerCare
#                        if residualCare <= 0:
#                            break
#             
#                receiverOccupants = list(receiver.occupants)                
#                careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                residualCare = self.p['quantumCare']
#                for person in careTakers:
#                    personalCare = min(person.unmetSocialCareNeed, residualCare)
#                    person.unmetSocialCareNeed -= personalCare
#                    person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                    person.formalSocialCareReceived += personalCare
#                    residualCare -= personalCare
#                    if residualCare <= 0:
#                        break
#                receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                receiver.formalSocialCareReceived += self.p['quantumCare']
#                
#                self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                
            else:
                employed.sort(key=operator.attrgetter("wage"))
                
                carer = employed[0]
                if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                    
                    # Sample out-of-income/out-of-wealth according to quantity
                    kindsOfCare = ['out-of-income care', 'out-of-wealth care']
                    weights = [formalSocialCare, careFromWealth]
                    careProbs = [x/sum(weights) for x in weights]
                    care = np.random.choice(kindsOfCare, p = careProbs)
                    if care == 'out-of-income care':
                        
                        for j in range(4):
                            supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                            supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                        supplier.householdFormalSupplyCost += costQuantumSocialCare
                        
                        careTransferred = 0
                        if len(employed) > 0:
                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
                            residualCare = self.p['quantumCare']
                            for worker in employed:
                                maxCare = costQuantumSocialCare/worker.wage
                                workerCare = min(maxCare, residualCare)
                                if workerCare < 1.0:
                                    workerCare = 1.0
                                worker.availableWorkingHours -= workerCare
                                worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                                worker.incomeExpenses += workerCare*worker.wage
                                careTransferred += workerCare
                                costQuantumSocialCare -= workerCare*worker.wage
                                residualCare -= workerCare
                                if residualCare <= 0:
                                    break
                        
                        # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                        
                        receiverOccupants = list(receiver.occupants)                
                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                        residualCare = careTransferred
                        for person in careTakers:
                            personalCare = min(person.unmetSocialCareNeed, residualCare)
                            person.unmetSocialCareNeed -= personalCare
                            person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                            person.formalSocialCareReceived += personalCare
                            residualCare -= personalCare
                            if residualCare <= 0:
                                break
                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                        receiver.formalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                        
                        
                    
#                        for j in range(4):
#                            supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                            supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                        supplier.householdFormalSupplyCost += costQuantumSocialCare
#                        
#                        if len(employed) > 0:
#                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                            residualCare = self.p['quantumCare']
#                            for worker in employed:
#                                maxCare = costQuantumSocialCare/worker.wage
#                                workerCare = min(maxCare, residualCare)
#                                worker.availableWorkingHours -= workerCare
#                                worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                                costQuantumSocialCare -= workerCare*worker.wage
#
#                                worker.careExpenses += workerCare*worker.wage
#                            
#                                residualCare -= workerCare
#                                if residualCare <= 0:
#                                    break
#                        
#                        # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                        
#                        receiverOccupants = list(receiver.occupants)                
#                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                        residualCare = self.p['quantumCare']
#                        for person in careTakers:
#                            personalCare = min(person.unmetSocialCareNeed, residualCare)
#                            person.unmetSocialCareNeed -= personalCare
#                            person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                            person.formalSocialCareReceived += personalCare
#                            residualCare -= personalCare
#                            if residualCare <= 0:
#                                break
#                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                        receiver.formalSocialCareReceived += self.p['quantumCare']
#                        
#                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                        
                    else:
                        household = list(supplier.occupants)
                        householdCarers = [x for x in household if x.wealthForCare > 0]
                        householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
                        maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])) for x in householdCarers]))
                        residualCare = maxSupply
                        careSupplied = 0
                        for i in householdCarers:
                            careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])), residualCare)
                            if i in receiver.occupants and careForNeed > 0:
                                i.careForFamily = True
                            i.socialWork += careForNeed
                            if careForNeed > 0:
                                
                                i.wealthForCare -= careForNeed*self.p['priceSocialCare']
                                i.wealthForCare = max(i.wealthForCare, 0)
                                # i.financialWealth -= careForNeed*self.p['priceSocialCare']
                                # i.financialWealth = max(i.financialWealth, 0)
                                i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
                                i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
                                careSupplied += careForNeed
                                residualCare -= careForNeed
                                if residualCare <= 0:
                                    break
                                
                        receiverOccupants = list(receiver.occupants)
                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                        residualCare = careSupplied
                        for person in careTakers:
                            personalCare = min(person.unmetSocialCareNeed, residualCare)
                            person.unmetSocialCareNeed -= personalCare
                            person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                            person.formalSocialCareReceived += personalCare
                            residualCare -= personalCare
                            if residualCare <= 0:
                                break
                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                        receiver.formalSocialCareReceived += self.p['quantumCare']
                        
                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
                    
                        
                        

#                    for j in range(4):
#                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
#                    supplier.householdFormalSupplyCost += costQuantumSocialCare
#                    
#                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for worker in employed:
#                        maxCare = costQuantumSocialCare/worker.wage
#                        workerCare = min(maxCare, residualCare)
#                        worker.availableWorkingHours -= workerCare
#                        worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                        costQuantumSocialCare -= workerCare*worker.wage
#                        residualCare -= workerCare
#                        if residualCare <= 0:
#                            break
#                    
#                    receiverOccupants = list(receiver.occupants)
#                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for person in careTakers:
#                        personalCare = min(person.unmetSocialCareNeed, residualCare)
#                        person.unmetSocialCareNeed -= personalCare
#                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                        person.formalSocialCareReceived += personalCare
#                        residualCare -= personalCare
#                        if residualCare <= 0:
#                            break
#                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                    receiver.formalSocialCareReceived += self.p['quantumCare']
#                    
#                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 3)
                    
                else: # In this case, it is more convenient to take time off work to provide informal care: out-of-income
#                    print 'Case 4'
#                    print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                    
                    if receiver == supplier:
                        self.inHouseInformalCare += self.p['quantumCare']
                    
                    careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours)
                    if careTransferred == 0:
                        print 'No residual working hours in carer'
                        sys.exit()
                    if carer in receiver.occupants and careTransferred > 0:
                        carer.careForFamily = True
                    incomeForCare = careTransferred*carer.wage
                    carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                    carer.availableWorkingHours = max(0, carer.availableWorkingHours)
                    carer.residualWorkingHours -= careTransferred
                    carer.residualWorkingHours = max(0, carer.residualWorkingHours)
                    carer.outOfWorkSocialCare += careTransferred
                    carer.socialWork += careTransferred
                    
                    
                    if receiver != supplier:
                        self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
                    else:
                        self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred
#                    print 'Care transferred: ' + str(careTransferred)
#                    print 'Carer wage: ' + str(carer.wage)
#                    print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
#                    print 'Pre-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= incomeForCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                        
#                    print 'Post-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                        person.informalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.informalSocialCareReceived += self.p['quantumCare']
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 4)
                    
#        else: # Out-of-wealth care
#            household = list(supplier.occupants)
#            householdCarers = [x for x in household if x.wealthForCare > 0]
#            householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
#            maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']) for x in householdCarers]))
#            residualCare = maxSupply
#            careSupplied = 0
#            for i in householdCarers:
#                careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']), residualCare)
#                if i in receiver.occupants and careForNeed > 0:
#                    i.careForFamily = True
#                i.socialWork += careForNeed
#                if careForNeed > 0:
#                    
#                    i.wealthForCare -= careForNeed*self.p['priceSocialCare']
#                    i.wealthForCare = max(i.wealthForCare, 0)
#                    i.financialWealth -= careForNeed*self.p['priceSocialCare']
#                    i.financialWealth = max(i.financialWealth, 0)
#                    i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
#                    i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
#                    careSupplied += careForNeed
#
#                    residualCare -= careForNeed
#                    if residualCare <= 0:
#                        break
#                    
#            receiverOccupants = list(receiver.occupants)
#            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#            residualCare = careSupplied
#            for person in careTakers:
#                personalCare = min(person.unmetSocialCareNeed, residualCare)
#                person.unmetSocialCareNeed -= personalCare
#                person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                person.formalSocialCareReceived += personalCare
#                residualCare -= personalCare
#                if residualCare <= 0:
#                    break
#            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#            receiver.formalSocialCareReceived += self.p['quantumCare']
#            
#            self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
    def transferSocialCare_Ind(self, receiver, supplier):
        
        if receiver != supplier:
            # In this case, care is provided with resources from people other than the care receiver
            distance = receiver.careNetwork[receiver][supplier]['distance']
            indexSupplier = receiver.suppliers.index(supplier)
            informalSupply = receiver.networkInformalSupplies[indexSupplier]
            formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]

            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(formalSocialCare, self.p['betaFormalCare'])
            probInformalCare = informalFactor/(informalFactor+formalFactor)
            # Select kind of care based on supplier availability
            care = 'formal care'
            if supplier.house.town in receiver.house.town.neighboringTowns:
                # careWeights = [informalSupply, formalSocialCare, careFromWealth]
                # careProbs = [x/sum(careWeights) for x in careWeights]
                careProbs = [probInformalCare, 1-probInformalCare]
                care = np.random.choice(['informal care', 'formal care'], p = careProbs) 
            
            if care == 'informal care':
            
                household = list(supplier.house.occupants)
                householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
                # If informal care is provided, it satisfies the most expensive cumulated child care need.
                for member in householdCarers:
                    member.residualInformalSupply = member.residualInformalSupplies[distance]
                householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
                
                residualCare = min(self.p['quantumCare'], receiver.unmetSocialCareNeed)
                if residualCare < 1.0:
                    residualCare = 1.0
                
                careTransferred = 0
                for i in householdCarers:
                    careForNeed = min(i.residualInformalSupply, residualCare)
                    if careForNeed < 1.0:
                        careForNeed = 1.0
                    if i in receiver.house.occupants and careForNeed > 0:
                        i.careForFamily = True
                    i.socialWork += careForNeed
                    if careForNeed > 0:
                        for j in range(4):
                            i.residualInformalSupplies[j] -= careForNeed
                            i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                        careTransferred += careForNeed
                        residualCare -= careForNeed
                        if residualCare <= 0:
                            break
                        
                if receiver.house.id == supplier.house.id:
                    self.inHouseInformalCare += careTransferred
                    
                if  receiver.house.id != supplier.house.id:
                    receiver.house.networkSupport += careTransferred
                    
                if receiver != supplier:
                    self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
                else:
                    self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred

                receiver.unmetSocialCareNeed -= careTransferred
                receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                receiver.informalSocialCareReceived += careTransferred
                receiver.house.informalSocialCareReceived += careTransferred
                
                self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 1)
                
            else: # Out-of-income care. Could be formal or informal: if different town, only formal; otherwise, depends on lowest wage
                household = list(supplier.house.occupants)
                employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
                
                maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
                
                residualCare = min(self.p['quantumCare'], receiver.unmetSocialCareNeed, maxFormalCare)
                if residualCare < 1.0:
                    residualCare = 1.0
                
                costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
                priceSocialCare = costQuantumSocialCare/residualCare
                
                if supplier.house.town not in receiver.house.town.neighboringTowns or len(employed) == 0: # Only formal care is possible
                    for j in range(4):
                        supplier.house.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0.0)
                    supplier.house.householdFormalSupplyCost += costQuantumSocialCare
                    
                    careTransferred = residualCare
                    if len(employed) > 0:
                        careTransferred = 0
                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
                        for worker in employed:
                            maxCare = costQuantumSocialCare/worker.wage
                            workerCare = min(maxCare, residualCare)
                            if workerCare < 1.0:
                                workerCare = 1.0
                            worker.availableWorkingHours -= workerCare
                            worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                            worker.incomeExpenses += workerCare*worker.wage
                            careTransferred += workerCare
                            costQuantumSocialCare -= workerCare*worker.wage
                            residualCare -= workerCare
                            if residualCare <= 0:
                                break
                    
                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                    receiver.unmetSocialCareNeed -= careTransferred
                    receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                    receiver.formalSocialCareReceived += careTransferred
                    receiver.house.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 2)
                    
                else:
                    # Select the worker with the lowest pay
                    employed.sort(key=operator.attrgetter("wage"))
                    
                    carer = employed[0]
                    if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                        for j in range(4):
                            supplier.house.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                            supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0)
                        supplier.house.householdFormalSupplyCost += costQuantumSocialCare
                        
                        # Workers working hours must be commited to earn salary to buy formal care, so are not available for informal care.
                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
                        careToAllocate = residualCare
                        careTransferred = 0
                        for worker in employed:
                            maxCare = costQuantumSocialCare/worker.wage
                            workerCare = min(maxCare, careToAllocate)
                            if workerCare < 1.0:
                                workerCare = 1.0
                            careTransferred += workerCare
                            worker.availableWorkingHours -= workerCare
                            worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                            worker.incomeExpenses += workerCare*worker.wage
                            costQuantumSocialCare -= workerCare*worker.wage
                            careToAllocate -= workerCare
                            if careToAllocate <= 0:
                                break
                       
                        receiver.unmetSocialCareNeed -= careTransferred
                        receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                        receiver.formalSocialCareReceived += careTransferred
                        receiver.house.formalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 3)
                        
                    else: # In this case, it is more convenient to take time off work to provide informal care.
#                        print 'Case 4'
#                        print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                        
                        
                        
                        careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours, receiver.unmetSocialCareNeed)
                        if careTransferred == 0:
                            print 'No residual working hours in carer'
                            sys.exit()
                        if careTransferred < 1.0:
                            careTransferred = 1.0
                        if carer in receiver.house.occupants and careTransferred > 0:
                            carer.careForFamily = True
                        incomeForCare = careTransferred*carer.wage
                        carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                        carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
                        carer.residualWorkingHours -= careTransferred
                        carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
                        carer.outOfWorkSocialCare += careTransferred
                        carer.socialWork += careTransferred
                        carer.house.outOfWorkSocialCare += careTransferred
                        
                        if receiver.house.id == supplier.house.id:
                            self.inHouseInformalCare += careTransferred
                        
#                        print 'Care transferred: ' + str(careTransferred)
#                        print 'Carer wage: ' + str(carer.wage)
#                        print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
#                        print 'Pre-residual Income for care (4): ' + str(supplier.house.residualIncomeForSocialCare)
                        
                        for j in range(4):
                            supplier.house.residualIncomeForSocialCare[j] -= incomeForCare
                            supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0)
                            
                        # print 'Post-residual Income for care (4): ' + str(supplier.house.residualIncomeForSocialCare)
                        
                        receiver.unmetSocialCareNeed -= careTransferred
                        receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                        receiver.informalSocialCareReceived += careTransferred
                        receiver.house.informalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 4)
                
                
        else: # In this case, formal care is paid with the receiver's wealth
            careSupplied = min(receiver.careSupplyFromWealth, self.p['quantumCare'], receiver.unmetSocialCareNeed)
            receiver.wealthForCare -= careSupplied*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
            receiver.wealthForCare = max(receiver.wealthForCare, 0)
            receiver.wealthSpentOnCare += careSupplied*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])

            receiver.unmetSocialCareNeed -= careSupplied
            receiver.unmetSocialCareNeed = max(receiver.unmetSocialCareNeed, 0)
            receiver.formalSocialCareReceived += careSupplied
            receiver.house.formalSocialCareReceived += careSupplied
            self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 10)
            
        
    def socialCareCost(self, person, care):
        house = person.house
        availableIncomeByTaxBand = self.updateIncomeByTaxBand(house)
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        cost = 0
        residualCare = care
        for i in range(len(availableIncomeByTaxBand)):
            # house.incomeByTaxBand[i] needs to be updated at every transfer of formal care, net of time off work and total formal care cost
            if availableIncomeByTaxBand[i]/prices[i] > residualCare:
                cost += residualCare*prices[i]
                availableIncomeByTaxBand[i] -= residualCare*prices[i]
                break
            else:
                cost += availableIncomeByTaxBand[i]
                residualCare -= availableIncomeByTaxBand[i]/prices[i]
                availableIncomeByTaxBand[i] = 0
        return cost    
        
        
    def computeResidualIncomeForSocialCare(self):
        
        # incomeShares = []
        
        for house in self.map.occupiedHouses:
            
            household = list(house.occupants)
            householdCarers = householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            employed = [x for x in householdCarers if x.status == 'worker']
            
            employed = [x for x in householdCarers if x.status == 'worker']
            for worker in employed:
                worker.potentialIncome = worker.residualWorkingHours*worker.wage
                
            incomes = [x.potentialIncome for x in householdCarers]
            incomes.extend([x.income for x in household if x.status == 'retired'])
            netIncome = sum(incomes) - house.householdFormalSupplyCost
            netIncome = max(netIncome, 0)
            incomePerCapita = netIncome/float(len(household))
            
            house.householdInformalSupply = []
            for i in range(4):
                house.householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
    
            taxBands = len(self.p['taxBrackets'])
            house.incomeByTaxBand = [0]*taxBands
            house.incomeByTaxBand[-1] = sum(incomes)
            for i in range(taxBands-1):
                for income in incomes:
                    if income > self.p['taxBrackets'][i]:
                        bracket = income-self.p['taxBrackets'][i]
                        house.incomeByTaxBand[i] += bracket
                        house.incomeByTaxBand[-1] -= bracket
                        incomes[incomes.index(income)] -= bracket
            
#            ############  Check Variable  ############################
#            if self.year == self.p['getCheckVariablesAtYear']:
#                self.perCapitaHouseholdIncome.append(incomePerCapita)
#            ##########################################################
     
            incomeForCareShare_D0 = 1.0 - 1.0/math.exp(self.p['incomeCareParam']*incomePerCapita)
            
            # incomeShares.append(incomeForCareShare_D0)
            
            incomeForCareShare_D1 = (1.0 - 1.0/math.exp(self.p['incomeCareParam']*incomePerCapita))*self.p['formalCareDiscountFactor']
            
            # print incomeForCareShare_D1
            
            residualIncomeForCare_D0 = netIncome*incomeForCareShare_D0
            residualIncomeForCare_D1 = netIncome*incomeForCareShare_D1
            
            house.residualIncomeForSocialCare = [residualIncomeForCare_D0, residualIncomeForCare_D1, 0, 0]
            
            # Compute total supply of household
            house.totalSupplies = [self.updateFormalSocialCareSupplies(house, x) for x in [0, 1]]
            house.totalSupplies.extend([0,0])
            
            for j in range(4):
                house.totalSupplies[j] += sum([x.residualInformalSupplies[j] for x in house.occupants])
                
            # Add supply from wealth
            peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
            house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
            house.careSupplyFromWealth = 0
            if house.totalLifeExpectancy > 0:
                house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
                # weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed]) # /float(52*house.totalLifeExpectancy)
                house.totalSupplies[0] += float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
                
            house.netCareSupply = house.totalSupplies[0] - house.totalSocialCareNeed
            
            
    
    def computeSocialCareNetworkSupply(self, house):
        
        town = house.town
        house.networkSupply = 0
        house.networkTotalSupplies = []
        house.weightedTotalSupplies = []
        house.networkInformalSupplies = []
        house.networkFormalSocialCareSupplies = []
        
        # Care from wealth
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.financialWealth for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(weeklyWealth/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
        house.networkSupply += house.careSupplyFromWealth
        
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        for supplier in house.suppliers:
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
#            careFromWealth = 0
#            if supplier == house:
#                careFromWealth = house.careSupplyFromWealth
#            weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
            
            # Informal Care Supplies
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies.append(informalSupply)
            house.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            house.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            weightedMaxFormalSocialCare = maxFormalSocialCare
            
            house.networkTotalSupplies.append(informalSupply+maxFormalSocialCare)
            house.weightedTotalSupplies.append(weightedInformalSupply+weightedMaxFormalSocialCare)
            house.networkSupply += maxFormalSocialCare
            
    def computeSocialCareNetworkSupply_W(self, house):
        
        town = house.town
        house.networkSupply = 0
        house.networkTotalSupplies = []
        house.weightedTotalSupplies = []
        house.networkInformalSupplies = []
        house.networkFormalSocialCareSupplies = []
        # Care from wealth
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            # weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
        house.networkSupply += house.careSupplyFromWealth
        
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        for supplier in house.suppliers:
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            careFromWealth = 0
            if supplier == house:
                careFromWealth = house.careSupplyFromWealth
            weightedCareFromWealth = careFromWealth #*self.p['weightCareFromWealth']
            
            # Informal Care Supplies
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies.append(informalSupply)
            house.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            house.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
            
            house.networkTotalSupplies.append(informalSupply+maxFormalSocialCare+careFromWealth)
            house.weightedTotalSupplies.append(weightedInformalSupply+weightedMaxFormalSocialCare+weightedCareFromWealth)
            house.networkSupply += maxFormalSocialCare
            
    def computeSocialCareNetworkSupply_Ind(self, person):
        
        town = person.house.town
        person.networkSupply = 0
        person.networkTotalSupplies = []
        person.weightedTotalSupplies = []
        person.networkInformalSupplies = []
        person.networkFormalSocialCareSupplies = []
        
        person.suppliers = list(person.careNetwork.neighbors(person))
        
#        print person.id
#        print [x.id for x in person.suppliers]
        
        person.careSupplyFromWealth = float(int(person.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
        careFromWealth = person.careSupplyFromWealth
        # weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        person.networkSupply += person.careSupplyFromWealth
        
        for supplier in person.suppliers:
            
            supplierTown = supplier.house.town
            distance = person.careNetwork[person][supplier]['distance']
                
            # Informal Care Supplies
            household = list(supplier.house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplierTown in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            person.networkInformalSupplies.append(informalSupply)
            person.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies_Ind(supplier, distance))
            person.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            
            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(maxFormalSocialCare, self.p['betaFormalCare'])
            
            # weightedMaxFormalSocialCare = maxFormalSocialCare*self.p['weightCareFromIncome']
            
            person.networkTotalSupplies.append(informalSupply+maxFormalSocialCare)
            person.weightedTotalSupplies.append(informalFactor+formalFactor)
            person.networkSupply += maxFormalSocialCare
        
    def updateSocialCareNetworkSupply(self, house, supplier, n):
        
        town = house.town
        
        oldSupply = house.networkSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        oldFormalCareSupplies = list(house.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(house.networkTotalSupplies)
        oldWealthForCare = house.wealthForCare
        oldCareFromWealth = house.careSupplyFromWealth
        
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        
#        if n == 10:
#            print 'Wealth for care; ' + str([x.wealthForCare for x in peopleWithNeed])
        
        # totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.financialWealth for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(weeklyWealth/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
#            if n == 10:
#                print 'House life expectancy: ' + str(house.totalLifeExpectancy)
#                print 'Weekly wealth: ' + str(weeklyWealth)
#                print 'Care supply from wealth: ' + str(house.careSupplyFromWealth)
#                print 'Old wealth for care: ' + str(oldWealthForCare)
#                print 'New wealth for care: ' + str(house.wealthForCare)
                
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
            
#            careFromWealth = 0
#            if supplier == house:
#                careFromWealth = house.careSupplyFromWealth
#            weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare
    
            house.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            house.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare
            house.weightedTotalSupplies[supplierIndex] = weightedInformalSupply+weightedMaxFormalSocialCare
            
            house.networkSupply = sum(house.networkTotalSupplies)
            
            if house.networkSupply >= oldSupply and n != 0 and n != 10:
                print 'Error: social care supply did not decrease!'
                print 'Case: ' + str(n)
                print house.id
                print [x.id for x in house.suppliers]
                print supplierIndex
                print supplier.id
                print ''
                print oldSupply
                print house.networkSupply
                print ''
                print oldInformalSupplies
                print house.networkInformalSupplies
                print ''
                print oldFormalCareSupplies
                print house.networkFormalSocialCareSupplies
                print ''
                print oldCareFromWealth
                print house.careSupplyFromWealth
                print ''
                print oldTotalSupplies
                print house.networkTotalSupplies
                
                sys.exit()
    
    def updateSocialCareNetworkSupply_W(self, house, supplier, n):
        
        town = house.town
        
        oldSupply = house.networkSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        oldFormalCareSupplies = list(house.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(house.networkTotalSupplies)
        oldWealthForCare = house.wealthForCare
        oldCareFromWealth = house.careSupplyFromWealth
        
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        
#        if n == 10:
#            print 'Wealth for care; ' + str([x.wealthForCare for x in peopleWithNeed])
        
        # totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed]) # /float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
#            if n == 10:
#                print 'House life expectancy: ' + str(house.totalLifeExpectancy)
#                print 'Weekly wealth: ' + str(weeklyWealth)
#                print 'Care supply from wealth: ' + str(house.careSupplyFromWealth)
#                print 'Old wealth for care: ' + str(oldWealthForCare)
#                print 'New wealth for care: ' + str(house.wealthForCare)
                
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
            
            careFromWealth = 0
            if supplier == house:
                careFromWealth = house.careSupplyFromWealth
            weightedCareFromWealth = careFromWealth #*self.p['weightCareFromWealth']
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
    
            house.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            house.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare+careFromWealth
            house.weightedTotalSupplies[supplierIndex] = weightedInformalSupply+weightedMaxFormalSocialCare+weightedCareFromWealth
            
            house.networkSupply = sum(house.networkTotalSupplies)
            
            if house.networkSupply >= oldSupply and n != 0 and n != 10:
                print 'Error: social care supply did not decrease!'
                print 'Case: ' + str(n)
                print house.id
                print [x.id for x in house.suppliers]
                print supplierIndex
                print supplier.id
                print ''
                print oldSupply
                print house.networkSupply
                print ''
                print oldInformalSupplies
                print house.networkInformalSupplies
                print ''
                print oldFormalCareSupplies
                print house.networkFormalSocialCareSupplies
                print ''
                print oldCareFromWealth
                print house.careSupplyFromWealth
                print ''
                print oldTotalSupplies
                print house.networkTotalSupplies
                
                sys.exit()    
        
    def updateSocialCareNetworkSupply_Ind(self, receiver, supplier, n):
        
        town = receiver.house.town
        
        oldSupply = receiver.networkSupply
        oldInformalSupplies = list(receiver.networkInformalSupplies)
        oldFormalCareSupplies = list(receiver.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(receiver.networkTotalSupplies)
        oldWealthForCare = receiver.wealthForCare
        oldCareFromWealth = receiver.careSupplyFromWealth
        
        receiver.careSupplyFromWealth = float(int(receiver.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
        careFromWealth = receiver.careSupplyFromWealth
        # weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        receiver.networkSupply = receiver.careSupplyFromWealth
        
        houses = [x.house for x in receiver.suppliers]
        if supplier.house in houses:
            
            supplier = [x for x in receiver.suppliers if x.house.id == supplier.house.id][0]
            supplierIndex = receiver.suppliers.index(supplier)
            
            # suppliers = list(receiver.careNetwork.neighbors(receiver))
            
#            if supplier not in suppliers:
#                print 'Error: supplier not in network!'
#                print receiver.id
#                print [x.id for x in receiver.suppliers]
#                print [x.id for x in suppliers]
#                sys.exit()
            
            distance = receiver.careNetwork[receiver][supplier]['distance']
                
            household = list(supplier.house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.house.town in town.neighboringTowns:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            receiver.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies_Ind(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
    
            receiver.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(maxFormalSocialCare, self.p['betaFormalCare'])
            
            receiver.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare
            receiver.weightedTotalSupplies[supplierIndex] = informalFactor+formalFactor
            
        receiver.networkSupply += sum(receiver.networkTotalSupplies)
        
        # receiver.networkSupply += receiver.careSupplyFromWealth
         
        if receiver.networkSupply >= oldSupply and n != 0 and n != 10:
            print 'Error: social care supply did not decrease!'
            print 'Case: ' + str(n)
            print receiver.id
            print [x.id for x in receiver.suppliers]
            print supplierIndex
            print supplier.id
            print ''
            print oldSupply
            print receiver.networkSupply
            print ''
            print oldInformalSupplies
            print receiver.networkInformalSupplies
            print ''
            print oldFormalCareSupplies
            print receiver.networkFormalSocialCareSupplies
            print ''
            print oldCareFromWealth
            print receiver.careSupplyFromWealth
            print ''
            print oldTotalSupplies
            print receiver.networkTotalSupplies
            
            sys.exit() 
                
    def transferInformalChildCare(self, receiver, supplier):
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        householdCarers = [x for x in supplier.occupants if x.residualInformalSupplies[distance] > 0]
        # Sort the suppliers in order of decreasing informal supply
        totInformalSupply = 0
        for member in householdCarers:
            member.residualInformalSupply = member.residualInformalSupplies[distance]
            totInformalSupply += member.residualInformalSupply
        householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        
        if totInformalSupply == 0:
            print 'Error: totInformalSupply is zero!'
            sys.exit()
        
        # Decrease the suppliers' informal supply by the quantum of care.
        
       
        residualCare = min(self.p['quantumCare'], receiver.totalChildCareNeed)
        if residualCare < 1.0:
            residualCare = 1.0
            
        careTransferred = 0
        for i in householdCarers:
            careForNeed = min(i.residualInformalSupply, residualCare)
            if careForNeed < 1.0:
                careForNeed = 1.0
            i.childWork += careForNeed
            if careForNeed > 0:
                careTransferred += careForNeed
                for j in range(4):
                    i.residualInformalSupplies[j] -= careForNeed
                    i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                residualCare -= careForNeed
                if residualCare <= 0:
                    break
                
        if  receiver != supplier:
            receiver.networkSupport += careTransferred
            
        if careTransferred == 0:
            print 'Informal care'
            print 'Residual care: ' + str(residualCare)
            print 'Error: care transferred is equal to zero!'
            sys.exit()
        
        
        
        # Decrease the child care needs of the receiver
        children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
        # preChildCareNeed = list([x.unmetChildCareNeed for x in children])
        
        # Because of the one-to-many nature of child care, the informal care provided decreases the care need of all the household's children
        for child in children:
            child.informalChildCareReceived += min(careTransferred, child.unmetChildCareNeed)
            child.unmetChildCareNeed -= careTransferred
            child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
        # postChildCareNeed = list([x.unmetChildCareNeed for x in children])
        receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
        receiver.informalChildCareReceived += careTransferred
        
#        preFormalSupply = self.updateFormalChildCareSupplies(receiver)
#        
#        preChildCareNeeds = receiver.childCareNeeds
#        preChildCarePrices = receiver.childCarePrices
#        preCumulatedChildren = receiver.cumulatedChildren
#        workers = [x for x in receiver.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
#        workers.sort(key=operator.attrgetter("wage"))
#        availableHours = [x.availableWorkingHours for x in workers]
#        wages = [x.wage for x in workers]
#        formalChilCareReceived = [x.formalChildCareReceived for x in children]
#        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
        
        
        self.updateChildCareNeeds(receiver)
        
#        postFormalSupply = self.updateFormalChildCareSupplies(receiver)
#        
#        if postFormalSupply > preFormalSupply:
#            print 'Care Transferred: ' + str(careTransferred)
#            print ''
#            print preChildCareNeed
#            print postChildCareNeed
#            print '' 
#            print 'Pre Formal Supply: ' + str(preFormalSupply)
#            print 'Post formal supply: ' + str(postFormalSupply)
#            print ''
#            print preChildCareNeeds
#            print preChildCarePrices
#            print preCumulatedChildren
#            print ''
#            print receiver.childCareNeeds
#            print receiver.childCarePrices
#            print receiver.cumulatedChildren
#            print ''
#            print availableHours
#            print wages
#            print formalChilCareReceived
#            print discountedNeed
#            sys.exit()
        
        # print 'Checking netwrk supply after case 1'
        self.updateChildCareNetworkSupply(receiver, supplier, 1)
        
    def outOfIncomeChildCare(self, receiver):
        
#        print receiver.residualIncomeForChildCare
#        for x in receiver.occupants:
#            print x.status
#            print x.careNeedLevel
#            if x.status == 'worker':
#                print x.potentialIncome
#                print x.residualWorkingHours
#            print x.income
#        print 'Household income: ' + str(self.computeHouseholdIncome(receiver))
        
        employed = [x for x in receiver.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
        children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
        
        maxFormalSupply = receiver.formalChildCareSupply
        careSupply = min(self.p['quantumCare'], receiver.totalChildCareNeed, maxFormalSupply)
        
        if careSupply == 0:
            print 'Error: careSupply OOI is equal to zero!'
            print ''
            sys.exit()
        
        if careSupply < 1.0:
            careSupply = 1.0
        
        potentialCostChildCare = self.computePotentialFormalChildCareCost(receiver, careSupply)
        valueInformalChildCare = potentialCostChildCare/careSupply
        
        if len(employed) > 0:
            employed.sort(key=operator.attrgetter("wage"))
            carer = employed[0]
            
        if len(employed) == 0 or carer.wage >= valueInformalChildCare: # In this case, it is more convenient to pay formal care 
           
            costQuantumChildCare = self.childCareCost(children, careSupply)
            receiver.residualIncomeForChildCare -= costQuantumChildCare
            receiver.residualIncomeForChildCare = max(receiver.residualIncomeForChildCare, 0)
            receiver.householdFormalSupplyCost += costQuantumChildCare
            
            totalCareResources = receiver.residualIncomeForChildCare + receiver.householdFormalSupplyCost
            income = self.computeHouseholdIncome(receiver)
            
#            if int(totalCareResources) != int(income):
#                print receiver.householdFormalSupplyCost
#                print income
#                print receiver.residualIncomeForChildCare
#                print costQuantumChildCare
#                print 'Error: residual income greater than income (2)'
#                sys.exit()
            
#            print ''
#            print 'Pre formal child care: ' + str(self.updateFormalChildCareSupplies(receiver))
#            children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
#            print 'Max formal care: ' + str(sum([max(self.p['maxFormalChildCare'] - x.formalChildCareReceived, 0) for x in children]))
#            print [x.formalChildCareReceived for x in children]
            
            #Reducing the available working hours for informal care
            careTransferred = 0
            if len(employed) > 0:
                employed.sort(key=operator.attrgetter("wage"), reverse=True)
                residualCare = careSupply
                for worker in employed:
                    
                    maxCare = costQuantumChildCare/worker.wage
                    workerCare = min(maxCare, residualCare)
                    if workerCare < 1.0:
                        workerCare = 1.0
                    careTransferred += workerCare
                    
                    worker.incomeExpenses += workerCare*worker.wage
                    
                    worker.availableWorkingHours -= workerCare
                    worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                    costQuantumChildCare -= workerCare*worker.wage
                    residualCare -= workerCare
                    if residualCare <= 0:
                        break
            else:
                careTransferred = careSupply
                #employed.sort(key=operator.attrgetter("wage"), reverse=True)
                #employed[0].availableWorkingHours -= costQuantumChildCare/employed[0].wage
                #employed[0].availableWorkingHours = max(employed[0].availableWorkingHours, 0)
                
            formalChildCares = [x.formalChildCareReceived for x in children if x.formalChildCareReceived < self.p['childcareTaxFreeCap']]
            if len(formalChildCares) > 0:
                children.sort(key=operator.attrgetter("formalChildCareReceived"))
            else:
                children.sort(key=operator.attrgetter("unmetChildCareNeed"), reverse = True)
            
            if careTransferred == 0:
                print 'Out-of-income formal care'
                print 'Error: care transferred is equal to zero!'
                sys.exit()
            
            residualCare = careTransferred
            for child in children:
                careForChild = min(child.unmetChildCareNeed, residualCare)
                if careForChild > 0:
                    child.formalChildCareReceived += careForChild
                    child.unmetChildCareNeed -= careForChild
                    child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
                residualCare -= careForChild
                if residualCare <= 0:
                    break
            receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
            receiver.formalChildCareReceived += careTransferred 
            receiver.formalChildCareCost += costQuantumChildCare
            
            
            self.updateChildCareNeeds(receiver)
            
#            print 'Post formal child care: ' + str(self.updateFormalChildCareSupplies(receiver))
#            children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
#            print 'Max formal care: ' + str(sum([max(self.p['maxFormalChildCare'] - x.formalChildCareReceived, 0) for x in children]))
#            print [x.formalChildCareReceived for x in children]
#            print ''
            # print 'Checking netwrk supply after case 2 (formal)'
            self.updateChildCareNetworkSupply(receiver, receiver, 2)
            
        else: # In this case, it is more convenient to take time off work to provide informal care
            
            
            # print 'Exectuing the time-off-work function'
            
            incomeBefore = self.computeHouseholdIncome(receiver)
            # print 'Household income before: ' + str(incomeBefore)
            
            residualIncomeBefore = receiver.residualIncomeForChildCare
            # print 'Residual Income for child care before: ' + str(residualIncomeBefore)
            
            childcareExpense = receiver.householdFormalSupplyCost
            # print 'Childcare expense: ' + str(childcareExpense)
            total = residualIncomeBefore+childcareExpense
            
#            if int(incomeBefore) != int(total):
#                print 'Error before'
#                sys.exit()
            
            # Care transferred
            careTransferred = min(careSupply, carer.availableWorkingHours)
            if careTransferred < 1.0:
                careTransferred = 1.0
            # print 'Care transferred: ' + str(careTransferred)
            if careTransferred == 0:
                print 'Out-of-income informal care'
                print 'Error: care transferred is equal to zero!'
                sys.exit()
            
            carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
            carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
            carer.residualWorkingHours -= careTransferred
            carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
            carer.outOfWorkChildCare += careTransferred
            carer.childWork += careTransferred #self.p['quantumCare']
            receiver.residualIncomeForChildCare -= carer.wage*careTransferred #self.p['quantumCare']
            # print 'Miised income for care: ' + str(carer.wage*self.p['quantumCare'])
            
            
            receiver.residualIncomeForChildCare = max(receiver.residualIncomeForChildCare, 0)
           
            incomeAfter = self.computeHouseholdIncome(receiver)
            # print 'Household income After: ' + str(incomeAfter)
            
            residualIncomeAfter = receiver.residualIncomeForChildCare
            # print 'Residual Income for child care After: ' + str(residualIncomeAfter)
            
            total = residualIncomeAfter+childcareExpense
            
            totalCareResources = receiver.residualIncomeForChildCare + receiver.householdFormalSupplyCost
            income = self.computeHouseholdIncome(receiver)
            
#            if int(totalCareResources) != int(income):
#                print 'Error: residual income greater than income (3)'
#                print receiver.householdFormalSupplyCost
#                print income
#                print receiver.residualIncomeForChildCare
#                print incomeBefore
#                print incomeAfter
#                print total
#                print carer.wage*self.p['quantumCare']
#                print residualIncomeBefore
#                print residualIncomeAfter
#                for x in receiver.occupants:
#                    print x.status
#                    print x.careNeedLevel
#                    if x.status == 'worker':
#                        print x.potentialIncome
#                        print x.residualWorkingHours
#                    print x.income
                
                
                # sys.exit()
            
            # print incomeBefore - incomeAfter
            # print residualIncomeBefore - residualIncomeAfter
            
#            if int(incomeAfter) != int(total):
#                print incomeBefore
#                print incomeAfter
#                print total
#                print carer.wage*self.p['quantumCare']
#                print residualIncomeBefore
#                print residualIncomeAfter
#                print childcareExpense
#                
#                print 'Error after'
#                sys.exit()
            
            
            children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
            for child in children:
                child.informalChildCareReceived += min(careTransferred, child.unmetChildCareNeed)
                child.unmetChildCareNeed -= careTransferred
                child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
            receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
            receiver.informalChildCareReceived = sum([x.informalChildCareReceived for x in children])
            
            self.updateChildCareNeeds(receiver)
            
            
            # print 'Checking netwrk supply after case 2 (informal)'
            self.updateChildCareNetworkSupply(receiver, receiver, 3)
        
        
    def transferChildCare(self, receiver, supplier, index):
        case = -1
        # Transfer quantim of care: decide who trasfers which kind of care (informal or formal) to whom
        informalSupply = receiver.networkInformalSupplies[index]
        formalChildCare = 0
        if receiver == supplier:
            formalChildCare = receiver.formalChildCareSupply
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'formal care']
        care = 'formal care'
        if supplier.town in receiver.town.neighboringTowns:
            careWeights = [informalSupply, formalChildCare]
            careProbs = [x/sum(careWeights) for x in careWeights]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        # If 'informal care' is selected: informal care provider are sorted in decreasing order.
        # Their supply is used to satisfy the most expensive care need.
        if care == 'informal care':
            case = 3
#            print 'tranfer child care: informal (3)'
#            print informalSupply
            self.transferInformalChildCare(receiver, supplier)
        else:
            case = 4
#            print 'tranfer child care: formal (4)'
#            print formalChildCare
        # Both formal and out-of-income informal care are possible: choice depends on price of child care and lowest wage.
            self.outOfIncomeChildCare(receiver)
            
        return case
    
    def childCareCost(self, children, careSupply):
        children.sort(key=operator.attrgetter("formalChildCareReceived"))
        cost = 0
        residualCare = careSupply
        for child in children:
            careForChild = min(child.unmetChildCareNeed, residualCare)
            if careForChild + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                cost += self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])*careForChild
                self.costTaxFreeChildCare += self.p['priceChildCare']*self.p['childCareTaxFreeRate']*careForChild
            else:
                if child.formalChildCareReceived >= self.p['childcareTaxFreeCap']:
                    cost += self.p['priceChildCare']*careForChild
                else:
                    discountedCare = self.p['childcareTaxFreeCap']-child.formalChildCareReceived
                    cost1 = discountedCare*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
                    self.costTaxFreeChildCare += discountedCare*self.p['priceChildCare']*self.p['childCareTaxFreeRate']
                    fullPriceCare = careForChild - discountedCare
                    cost2 = fullPriceCare*self.p['priceChildCare']
                    cost += (cost1 + cost2)
            residualCare -= careForChild
            if residualCare <= 0:
                break
        return cost
    
    def computeHouseholdIncome(self, house):
        householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
        employed = [x for x in householdCarers if x.status == 'worker']
        householdIncome = 0
        for worker in employed:
            worker.income = worker.residualWorkingHours*worker.wage
            
        householdIncome = sum([x.income for x in householdCarers])

        return householdIncome
        
        
    def updateChildCareNeeds(self, house):
        children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        children.sort(key=operator.attrgetter("unmetChildCareNeed"))
        residualNeeds = [x.unmetChildCareNeed for x in children]
        
        # print 'Unmet child care needs: ' + str(residualNeeds)
        
        marginalNeeds = []
        numbers = []
        toSubtract = 0
        for need in residualNeeds:
            marginalNeed = need-toSubtract
            marginalNeed = max(marginalNeed, 0)
            if marginalNeed > 0:
                marginalNeeds.append(marginalNeed)
                num = len([x for x in residualNeeds if x >= need])
                numbers.append(num)                
                toSubtract = need
        house.childCareNeeds = marginalNeeds
        house.cumulatedChildren = numbers
        
        # print 'House child care needs: ' + str(house.childCareNeeds)
        
        prices = []
        residualCare = 0
        cumulatedCare = 0
        for i in range(len(numbers)):
            cost = 0
            residualCare = house.childCareNeeds[i]
            for child in children[-numbers[i]:]:
                if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                    cost += self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])*residualCare
                else:
                    if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
                        cost += self.p['priceChildCare']*residualCare
                    else:
                        discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
                        cost1 = discountedCare*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
                        fullPriceCare = residualCare - discountedCare
                        cost2 = fullPriceCare*self.p['priceChildCare']
                        cost += (cost1 + cost2)
            cumulatedCare += house.childCareNeeds[i]
            prices.append(cost/house.childCareNeeds[i])
        house.childCarePrices = prices
        
        # print 'House child care prices: ' + str(house.childCarePrices)
        
        house.highPriceChildCare = 0
        house.lowPriceChildCare = 0
        for i in range(len(house.childCarePrices)):
            if house.childCarePrices[i] >= self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']):
                house.highPriceChildCare += house.childCareNeeds[i]
            else:
                house.lowPriceChildCare += house.childCareNeeds[i]
        
        
        if house.totalChildCareNeed > 0 and (house.highPriceChildCare+house.lowPriceChildCare) <= 0:
            print 'Error: mismatch between total child care needs in updateChildCareNeeds'
            print house.totalChildCareNeed
            print house.childCareNeeds
            print house.childCarePrices
            print house.highPriceChildCare
            print house.lowPriceChildCare
            sys.exit()
        # print 'High price care in updateChildCare: ' + str(house.highPriceChildCare)
            
        # print 'Low price care in updateChildCare: ' + str(house.lowPriceChildCare)
                    
    def computePotentialFormalChildCareCost(self, house, careSupply):
        # How much would the household have to pay to provide the same amount of care through formal childcare as a quantum of informal care?
        cost = 0
        residualNeed = careSupply
        for i in range(len(house.childCareNeeds)):
            careForChild = min(house.childCareNeeds[i], residualNeed)
            cost += careForChild*house.childCarePrices[i]
            residualNeed -= careForChild
            if residualNeed <= 0:
                break
        return cost
        
    def computeChildCareNetworkSupply(self, house):
        
        town = house.town
        
       
        
        house.networkSupply = 0
        house.formalChildCareSupply = 0
        house.networkTotalSupplies = []
        house.networkInformalSupplies = []
        house.childCareWeights = []
        house.formalCaresRatios = []
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        # Household supply
        
#        household = list(house.occupants)
#        householdCarers = [x for x in household if x.residualInformalSupplies[0] > 0]
#        informalSupply = sum([x.residualInformalSupplies[0] for x in householdCarers])
#        house.networkInformalSupplies.append(informalSupply)
#        house.formalChildCareSupply = self.updateFormalChildCareSupplies(house)
#        householdTotalSupply = informalSupply + house.formalChildCareSupply
#        house.networkTotalSupplies.append(householdTotalSupply)
#        house.networkSupply = householdTotalSupply
#        
        for supplier in house.suppliers:
            
            if supplier == house:
                household = list(house.occupants)
                householdCarers = [x for x in household if x.residualInformalSupplies[0] > 0]
                informalSupply = sum([x.residualInformalSupplies[0] for x in householdCarers])
                house.networkInformalSupplies.append(informalSupply)
                house.formalChildCareSupply = self.updateFormalChildCareSupplies(house)
                householdTotalSupply = informalSupply + house.formalChildCareSupply
                house.networkTotalSupplies.append(householdTotalSupply)
                house.networkSupply += householdTotalSupply
            else:
                distance = house.careNetwork[house][supplier]['distance']
                household = list(supplier.occupants)
                householdCarers = [x for x in household if x.residualInformalSupplies[distance] > 0]
                informalSupply = 0
                if supplier.town in town.neighboringTowns:
                    informalSupply = sum([x.residualInformalSupplies[distance] for x in householdCarers])
                house.networkInformalSupplies.append(informalSupply)
                house.networkTotalSupplies.append(informalSupply)
                house.networkSupply += informalSupply
            
    def updateChildCareNetworkSupply(self, house, supplier, n):
        
        children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        
        
        oldSupply = house.networkSupply
        oldFormalSupply = house.formalChildCareSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        
        town = house.town
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.residualInformalSupplies[distance] > 0]
            informalSupply = 0
            if supplier.town in town.neighboringTowns:
                informalSupply = sum([x.residualInformalSupplies[distance] for x in householdCarers])
            house.networkInformalSupplies[supplierIndex] = informalSupply
            house.networkTotalSupplies[supplierIndex] = informalSupply
            
            if house == supplier:
                
               #  print 'Updating formal child care supply.....'
                residualFormalChilCare = sum([max(self.p['maxFormalChildCare'] - x.formalChildCareReceived, 0) for x in children])
                house.formalChildCareSupply = min(self.updateFormalChildCareSupplies(house), residualFormalChilCare)
                house.networkTotalSupplies[supplierIndex] += house.formalChildCareSupply

            house.networkSupply = sum(house.networkTotalSupplies)
            
#            if n != 4 and n != 3:
#                if house.networkSupply >= oldSupply and house:
#                    print ''
#                    print 'Case; ' + str(n)
#                    print oldSupply
#                    print house.networkSupply
#                    print ''
#                    print oldInformalSupplies
#                    print house.networkInformalSupplies
#                    print ''
#                    print oldFormalSupply
#                    print house.formalChildCareSupply
#                    print 'Error: child supply did not change'
#                    sys.exit()
            
    
    def updateIncomeByTaxBand(self, house):
        householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
        employed = [x for x in householdCarers if x.status == 'worker']
        householdIncome = 0
        for worker in employed:
            worker.income = worker.residualWorkingHours*worker.wage
        incomes = [x.income for x in householdCarers]
        
        taxBands = len(self.p['taxBrackets'])
        house.incomeByTaxBand = [0]*taxBands
        house.incomeByTaxBand[-1] = sum(incomes)
        for i in range(taxBands-1):
            for income in incomes:
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    house.incomeByTaxBand[i] += bracket
                    house.incomeByTaxBand[-1] -= bracket
                    incomes[incomes.index(income)] -= bracket
        # Available income by tax band
        house.availableIncomeByTaxBand = house.incomeByTaxBand
        careExpense = house.householdFormalSupplyCost
        for i in range(len(house.availableIncomeByTaxBand)):
            if house.availableIncomeByTaxBand[i] > careExpense:
                house.availableIncomeByTaxBand[i] -= careExpense
                careExpense = 0
                break
            else:
                careExpense -= house.availableIncomeByTaxBand[i]
                house.availableIncomeByTaxBand[i] = 0
        return house.availableIncomeByTaxBand        
    
#    def updateFormalSocialCareSupplies(self, house, distance):
#        availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
#        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
#        
#        # print 'residual Income for care: ' + str(residualIncomeForCare)
#        
#        # How much social care can the household buy with the residual income for care?
#        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
#        incomeByTaxBand = list(availableIncomeByTaxBand)
#        totalHours = 0
#        for i in range(len(incomeByTaxBand)):
#            if residualIncomeForCare > incomeByTaxBand[i]:
#                totalHours += incomeByTaxBand[i]/prices[i]
#                residualIncomeForCare -= incomeByTaxBand[i]
#            else:
#                totalHours += residualIncomeForCare/prices[i]
#                break
#        
#        # print 'Tot hours: ' + str(totalHours)
#        
#        socialCareSupplies = round(totalHours)
#        
#        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#        return socialCareSupplies
        
    def updateFormalSocialCareSupplies(self, house, distance):
        
        # The out-of-income social care is given by the sum of the informal social care provided by taking hours off work and the formal care paid through the
        # residual income.
        
        # availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
        workers = [x for x in house.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        
        totHours = 0
        for worker in workers:
            if residualIncomeForCare == 0:
                break
            workerIncome = worker.availableWorkingHours*worker.wage
            for i in range(len(self.p['taxBrackets'])):
                bracket = max(workerIncome-self.p['taxBrackets'][i], 0)
                incomeForFormalCare = min(bracket, residualIncomeForCare)
                workerIncome -= incomeForFormalCare
                if prices[i] > worker.wage:
                    totHours += incomeForFormalCare/worker.wage
                else:
                    totHours += incomeForFormalCare/prices[i]
                residualIncomeForCare -= incomeForFormalCare
                residualIncomeForCare = max(residualIncomeForCare, 0)
                if residualIncomeForCare == 0:
                    break
        # print 'Tot hours: ' + str(totalHours)
        
        socialCareSupplies = int(totHours)
        
        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        return socialCareSupplies    
    
    def updateFormalSocialCareSupplies_Ind(self, supplier, distance):
        
        # The out-of-income social care is given by the sum of the informal social care provided by taking hours off work and the formal care paid through the
        # residual income.
        house = supplier.house
        # availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
        workers = [x for x in house.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        
        totHours = 0
        for worker in workers:
            if residualIncomeForCare == 0:
                break
            workerIncome = worker.availableWorkingHours*worker.wage
            for i in range(len(self.p['taxBrackets'])):
                bracket = max(workerIncome-self.p['taxBrackets'][i], 0)
                incomeForFormalCare = min(bracket, residualIncomeForCare)
                workerIncome -= incomeForFormalCare
                if prices[i] > worker.wage:
                    totHours += incomeForFormalCare/worker.wage
                else:
                    totHours += incomeForFormalCare/prices[i]
                residualIncomeForCare -= incomeForFormalCare
                residualIncomeForCare = max(residualIncomeForCare, 0)
                if residualIncomeForCare == 0:
                    break
        # print 'Tot hours: ' + str(totalHours)
        
        socialCareSupplies = int(totHours)
        
        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        return socialCareSupplies

    def updateFormalChildCareSupplies(self, receiver):
        
        # residualIncomeForCare = receiver.residualIncomeForChildCare
        receiverOccupants = receiver.occupants
        children = [x for x in receiverOccupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        workers = [x for x in receiverOccupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        availableHours = [x.availableWorkingHours for x in workers]
        wages = [x.wage for x in workers]
        
#        print ''
#        print 'In-function children needs: ' + str(receiver.childCareNeeds)
#        print 'In-function child care prices: ' + str(receiver.childCarePrices)
#        print 'In-function num children: ' + str(receiver.cumulatedChildren)
#        print 'In-function available hours: ' + str(availableHours)
#        print 'In-function wages: ' + str(wages)
        
        
        residualNeeds = list(receiver.childCareNeeds)
        
        # print 'Wages: ' + str(wages)
        # print 'Available hours pre: ' + str(availableHours)
        
        totHours = 0
        for i in range(len(receiver.childCareNeeds)):
            for j in range(len(workers)):
                if receiver.childCarePrices[i] > wages[j]:
                    if availableHours[j] > residualNeeds[i]:
                        totHours += residualNeeds[i]*receiver.cumulatedChildren[i]
                        availableHours[j] -= residualNeeds[i]
                        residualNeeds[i] = 0
                        break
                    else:
                        totHours += availableHours[j]*receiver.cumulatedChildren[i]
                        residualNeeds[i] -= availableHours[j]
                        availableHours[j] = 0
                        
        # The remaining income is used to provide formal child care
        residualIncomeForCare = sum(np.multiply(availableHours,wages))
        
        # print 'Residual Incoem for Care: ' + str(residualIncomeForCare)
        # print 'Available hours post: ' + str(availableHours)
        # print 'Formal child care received:' + str(formalChilCareReceived)
        
        # List of residual formal child care below the tax free cap (i.e. for which the household get the discounted price)
        formalChilCareReceived = [x.formalChildCareReceived for x in children]
        
        # print 'Formal Child Care Received: ' + str(formalChilCareReceived)
        
        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
        
#        print 'In-function available hours: ' + str(formalChilCareReceived)
#        print 'In-function discounted need: ' + str(discountedNeed)
#        print ''
        
        # print 'Discounted Need: ' + str(discountedNeed)
        # print ''
        # print 'Discounted need: ' + str(discountedNeed)
        
        # Total cost of discounted child care 
        discountedCost = sum(discountedNeed)*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
        
        
        
        # print 'Discounted Cost: ' + str(discountedCost)

        if residualIncomeForCare > discountedCost:
            totHours += sum(discountedNeed)
            residualIncomeForCare -= discountedCost
            totHours += residualIncomeForCare/self.p['priceChildCare']
        else:
            totHours += residualIncomeForCare/(self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate']))
            
        # print 'Total formal supply hours: ' + str(totHours)
        
        # totHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']   
        totHours = int(totHours)
        
        return totHours

#    def updateFormalChildCareSupplies(self, receiver):
#        
#        residualIncomeForCare = receiver.residualIncomeForChildCare
#        receiverOccupants = receiver.occupants
#        children = [x for x in receiverOccupants if x.age > 0 and x.age < self.p['ageTeenagers']]
#        formalChilCareReceived = [x.formalChildCareReceived for x in children]
#        
#        # print 'Formal child care received:' + str(formalChilCareReceived)
#        
#        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
#        
#        # print 'Discounted need: ' + str(discountedNeed)
#        
#        discountedCost = sum(discountedNeed)*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
#        
#        # print 'Discounted Cost: ' + str(discountedCost)
#        
#        totHours = 0
#        if residualIncomeForCare > discountedCost:
#            totHours = sum(discountedNeed)
#            residualIncomeForCare -= discountedCost
#            totHours += residualIncomeForCare/self.p['priceChildCare']
#        else:
#            totHours = residualIncomeForCare/(self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate']))
#            
#        # print 'Total formal supply hours: ' + str(totHours)
#        
#        # totHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']   
#        totHours = round(totHours)
#        
#        return totHours
            
    def resetCareVariables_KN(self):
        
        for house in self.map.occupiedHouses:
            
            house.careNetwork.clear()
            house.demandNetwork.clear()
            house.totalSocialCareNeed = 0
            house.totalUnmetSocialCareNeed = 0
            house.totalChildCareNeed = 0
            house.childCareNeeds = []
            house.childCarePrices = []
            house.highPriceChildCare = 0
            house.lowPriceChildCare = 0
            house.residualIncomeForChildCare = 0
            house.initialResidualIncomeForChildCare = 0
            house.residualIncomeForSocialCare = []
            house.householdInformalSupplies = []
            house.householdFormalSupply = []
            house.networkSupply = 0
            house.networkTotalSupplies = []
            house.networkInformalSupplies = []
            house.formalChildCareSupply = 0
            house.networkFormalSocialCareSupplies = []
            house.totalSupplies = []
            house.netCareSupply = 0
            house.childCareWeights = []
            house.formalCaresRatios = []
            house.informalChildCareReceived = 0
            house.informalSocialCareReceived = 0
            house.formalChildCareReceived = 0
            house.formalChildCareCost = 0
            house.formalSocialCareReceived = 0
            house.householdFormalSupplyCost = 0
            house.wealthForCare = 0
            house.incomeByTaxBand = []
            house.averageChildCarePrice = 0
            house.networkSupport = 0
            house.outOfWorkSocialCare = 0
            house.townAttractiveness = []
            house.netCareDemand = 0
            house.careAttractionFactor = 0
            house.newOccupancy = False
            
            for person in house.occupants:
                person.careNetwork.clear()
                person.hoursChildCareDemand = 0
                person.netChildCareDemand = 0
                person.unmetChildCareNeed = 0
                person.hoursSocialCareDemand = 0
                person.unmetSocialCareNeed = 0
                person.informalChildCareReceived = 0
                person.formalChildCareReceived = 0
                person.publicChildCareContribution = 0
                person.informalSocialCareReceived = 0
                person.formalSocialCareReceived = 0
                person.childWork = 0
                person.socialWork = 0
                person.potentialIncome = 0
                person.wealthPV = 0
                person.wealthForCare = 0
                person.incomeExpenses = 0
                person.outOfWorkChildCare = 0
                person.outOfWorkSocialCare = 0
                person.residualWorkingHours = 0
                person.availableWorkingHours = 0
                person.residualInformalSupplies = [0.0, 0.0, 0.0, 0.0]
                person.residualInformalSupply = 0
                person.hoursInformalSupplies = [0.0, 0.0, 0.0, 0.0]
                person.maxFormalCareSupply = 0
                person.totalSupply = 0
                person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
                person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
                person.careForFamily = False
                person.wealthSpentOnCare = 0
                # Social care provision variables
                person.networkSupply = 0
                person.networkTotalSupplies = []
                person.weightedTotalSupplies = []
                person.networkInformalSupplies = []
                person.networkFormalSocialCareSupplies = []
                person.suppliers = []
            
    def householdCareNetwork(self):
        
        # Create two care netwroks:
        # - an household care network for child care (a child care need is a household need)
        # - a person care network for social care (as socila care is personal)
        
        for house in self.map.occupiedHouses:
        
            house.careNetwork.add_node(house)
            house.demandNetwork.add_node(house)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = sum([x.unmetSocialCareNeed for x in household])
            # Distance 1
            for member in household:
                
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                        
            # Distance 2
            for member in household:
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                            
            # Distance 3
            for member in household:
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 3)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited:
                                house.careNetwork.add_edge(house, nok.house, distance = 3)
                                visited.append(nok.house)
                                
        peopleInNeed = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
        for person in peopleInNeed:
            visited = []
            person.careNetwork.add_node(person)
            household = list(person.house.occupants)
            if len(household) > 1:
                otherMembers = [x for x in household if x.id != person.id]
                person.careNetwork.add_edge(person, otherMembers[0], distance = 0)
                visited.append(person.house)
            # First level
            if person.father != None:
                nok = person.father
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
                nok = person.mother
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
            for child in person.children:
                nok = child
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
            # Second level
            if person.father != None:
                if person.father.father != None:
                    nok = person.father.father
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                    nok = person.father.mother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                if person.mother.father != None:
                    nok = person.mother.father
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                    nok = person.mother.mother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                brothers = list(set(person.father.children + person.mother.children))
                brothers.remove(person)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
            for child in person.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
            # Third level
            uncles = []
            if person.father != None:
                if person.father.father != None:
                    uncles = list(set(person.father.father.children + person.father.mother.children))
                    uncles.remove(person.father)
                if person.mother.father != None:
                    uncles.extend(list(set(person.mother.father.children + person.mother.mother.children)))
                    uncles.remove(person.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 3)
                        visited.append(nok.house)
                brothers = list(set(person.father.children + person.mother.children))
                brothers.remove(person)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok.house not in visited:
                            person.careNetwork.add_edge(person, nok, distance = 3)
                            visited.append(nok.house)
        
        for house in self.map.occupiedHouses:
            suppliers = house.careNetwork.successors(house)
            distances = [house.careNetwork[house][x]['distance'] for x in suppliers]
            for supplier in suppliers:
                if supplier.demandNetwork.has_edge(supplier, house) == True:
                    continue
                supplier.demandNetwork.add_edge(supplier, house, distance = distances[suppliers.index(supplier)])
    
    def householdSocialCareNetwork(self):
        
        
        for house in self.map.occupiedHouses:
            
            house.careNetwork.clear()
            house.careNetwork.add_node(house, netDemand = 0)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = max(sum([x.unmetSocialCareNeed for x in household])-house.totalSupplies[0], 0)
            # Distance 1
            for member in household:
                distanceOne = []
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
            
            np.random.shuffle(distanceOne)
            
            for supplier in distanceOne:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp'])
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                
                print 'Prob kinship network: ' + str(prob)
                
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_node(supplier, netDemand = 0)
                    house.careNetwork.add_edge(house, supplier, distance = 1, careTransferred = 0)
                    residualCareNeed -= supplier.totalSupplies[1]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                
                
            # Distance 2
            for member in household:
                distanceTwo = []
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                            
            np.random.shuffle(distanceTwo)
            
            for supplier in distanceTwo:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp']*2.0)
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_edge(house, supplier, distance = 2)
                    residualCareNeed -= supplier.totalSupplies[2]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                            
            # Distance 3
            for member in household:
                distanceThree = []
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceThree.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited:
                                distanceThree.append(nok.house)
                                
            np.random.shuffle(distanceThree)
            
            for supplier in distanceThree:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp']*3.0)
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_edge(house, supplier, distance = 3)
                    residualCareNeed -= supplier.totalSupplies[3]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                    
                    
    def householdCareNetwork_netSupply(self):
        
        for house in self.map.occupiedHouses:
            house.careNetwork.clear()
            house.careNetwork.add_node(house)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = sum([x.unmetSocialCareNeed for x in household])
            # Distance 1
            for member in household:
                
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                        
            # Distance 2
            for member in household:
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                            
            # Distance 3
            for member in household:
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 3)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                                house.careNetwork.add_edge(house, nok.house, distance = 3)
                                visited.append(nok.house)
                                      
    def computeSocialCareNeeds(self):
        
        self.publicSocialCare = 0
        for house in self.map.occupiedHouses:
            household = list(house.occupants)
            for person in household:
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                person.hoursSocialCareDemand = careNeed
                person.unmetSocialCareNeed = person.hoursSocialCareDemand
                
                if person.unmetSocialCareNeed > 0:
                    person.wealthPV = person.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], person.lifeExpectancy)
                    person.wealthForCare = person.financialWealth
                
                preCareNeed = person.unmetSocialCareNeed
                
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit'] and person.independentStatus == True:
                    socialCareCost = person.unmetSocialCareNeed*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
                    # The state pays for all the social care need that cannot be satisfied by the person with his income (leaving him a minimum income)
                    if socialCareCost > person.income - self.p['minimumIncomeGuarantee']:
                        if person.income > self.p['minimumIncomeGuarantee']:
                            stateContribution = 0
                            if person.wealth <= self.p['minWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                            elif  person.wealth > self.p['minWealthMeansTest'] and person.wealth < self.p['maxWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                                stateContribution -= int(person.wealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare   
                        else:
                            stateContribution = 0
                            if person.wealth <= self.p['minWealthMeansTest']:
                                stateContribution = socialCareCost
                            elif  person.wealth > self.p['minWealthMeansTest'] and person.wealth < self.p['maxWealthMeansTest']:
                                stateContribution = socialCareCost
                                stateContribution -= int(person.wealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare
                        
                        postCareNeed = person.unmetSocialCareNeed
                        
                        if postCareNeed > preCareNeed or postCareNeed < 0:
                            print postCareNeed
                            print preCareNeed
                            print person.income
                            print stateContribution
                            print stateCare
                            # sys.exit()
                            
                        
            house.totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in household])
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in household])
        
        self.costPublicSocialCare = self.publicSocialCare*self.p['priceSocialCare']
        self.publicCareProvision.append(self.publicSocialCare)
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicSocialCare = 0
        if totalSocialCareNeed > 0:
            self.sharePublicSocialCare = 1.0 - float(totalResidualSocialCareNeed)/float(totalSocialCareNeed)
            
            
    def computeSocialCareNeeds_W(self):
        
        self.publicSocialCare = 0
        for house in self.map.occupiedHouses:
            household = list(house.occupants)
            for person in household:
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                person.hoursSocialCareDemand = careNeed
                person.unmetSocialCareNeed = person.hoursSocialCareDemand
                
                if person.unmetSocialCareNeed > 0:
                    person.wealthPV = person.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], person.lifeExpectancy)
                    
                    shareWealthForCare = 1.0 - 1.0/math.exp(self.p['wealthCareParam']*person.financialWealth)
                    
                    # print 'Share of financial wealth for care: ' + str(shareWealthForCare)
                    
                    if shareWealthForCare < 0:
                        print 'Error: negative share: ' + str(person.financialWealth)
                        sys.exit()
                    
                    person.wealthForCare = ((person.financialWealth/person.lifeExpectancy)*shareWealthForCare)/52.0
                
                preCareNeed = person.unmetSocialCareNeed
                
                # Compute probability of taking advantage of public social care
                # Depends on income (-) of household and level of unmet care need (+)
                
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit'] and person.independentStatus == True:
                    socialCareCost = person.unmetSocialCareNeed*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
                    # The state pays for all the social care need that cannot be satisfied by the person with his income (leaving him a minimum income)
                    if socialCareCost > person.income - self.p['minimumIncomeGuarantee']:
                        if person.income > self.p['minimumIncomeGuarantee']:
                            stateContribution = 0
                            if person.financialWealth <= self.p['minWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                            elif  person.financialWealth > self.p['minWealthMeansTest'] and person.financialWealth < self.p['maxWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                                stateContribution -= int(person.financialWealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare   
                        else:
                            stateContribution = 0
                            if person.financialWealth <= self.p['minWealthMeansTest']:
                                stateContribution = socialCareCost
                            elif  person.financialWealth > self.p['minWealthMeansTest'] and person.financialWealth < self.p['maxWealthMeansTest']:
                                stateContribution = socialCareCost
                                stateContribution -= int(person.financialWealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare
                        
                        postCareNeed = person.unmetSocialCareNeed
                        
                        if postCareNeed > preCareNeed or postCareNeed < 0:
                            print postCareNeed
                            print preCareNeed
                            print person.income
                            print stateContribution
                            print stateCare
                            # sys.exit()
                            
                        
            house.totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in household])
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in household])
        
        self.costPublicSocialCare = self.publicSocialCare*self.p['priceSocialCare']
        self.publicCareProvision.append(self.publicSocialCare)
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicSocialCare = 0
        if totalSocialCareNeed > 0:
            self.sharePublicSocialCare = 1.0 - float(totalResidualSocialCareNeed)/float(totalSocialCareNeed)
            
            
    def computeSocialCareNeeds_Scot(self):
        
        self.publicSocialCare = 0
        self.publicCareExpenses = 0
        for house in self.map.occupiedHouses:
            household = list(house.occupants)
            for person in household:
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                person.hoursSocialCareDemand = careNeed
                person.unmetSocialCareNeed = person.hoursSocialCareDemand
                
                if person.unmetSocialCareNeed > 0:
                    person.wealthPV = person.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], person.lifeExpectancy)
                    
                    shareWealthForCare = 1.0 - 1.0/math.exp(self.p['wealthCareParam']*person.financialWealth)
                    
                    # print 'Share of financial wealth for care: ' + str(shareWealthForCare)
                    
                    if shareWealthForCare < 0:
                        print 'Error: negative share: ' + str(person.financialWealth)
                        sys.exit()
                    
                    person.wealthForCare = ((person.financialWealth/person.lifeExpectancy)*shareWealthForCare)/52.0
                
                preCareNeed = person.unmetSocialCareNeed
                
                # Compute probability of taking advantage of public social care
                # Depends on income (-) of household and level of unmet care need (+)
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit']:
                    socialCareCost = person.unmetSocialCareNeed*self.p['priceSocialCare']
                    stateContribution = socialCareCost
                    stateCare = person.unmetSocialCareNeed
                    self.publicSocialCare += stateCare
                    self.publicCareExpenses += socialCareCost
                    person.unmetSocialCareNeed -= stateCare
                    
                    
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit'] and person.independentStatus == True:
                    accomodationCost = self.p['residentialCost']
                    stateContribution = 0
                    if person.financialWealth <= self.p['minWealthMeansTest']:
                        stateContribution = accomodationCost
                    elif  person.financialWealth > self.p['minWealthMeansTest'] and person.financialWealth < self.p['maxWealthMeansTest']:
                        stateContribution -= int(person.financialWealth/self.p['wealthToPoundReduction'])
                        stateContribution = max(stateContribution, 0)
                    self.publicCareExpenses += stateContribution
    
                        
            house.totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in household])
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in household])
        
        self.costPublicSocialCare = self.publicSocialCare*self.p['priceSocialCare'] + self.publicCareExpenses
        self.publicCareProvision.append(self.publicSocialCare)
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicSocialCare = 0
        if totalSocialCareNeed > 0:
            self.sharePublicSocialCare = 1.0 - float(totalResidualSocialCareNeed)/float(totalSocialCareNeed)
       
    def computeChildCareNeeds(self):
        
        self.publicChildCare = 0
        for house in self.map.occupiedHouses:
        
            household = list(house.occupants)
            
            children = [x for x in household if x.age > 0 and x.age < self.p['ageTeenagers']]
            
            newBorns = [x for x in household if x.age == 0]
            for child in newBorns:
                child.hoursChildCareDemand = self.p['zeroYearCare']
                child.netChildCareDemand = child.hoursChildCareDemand
                child.informalChildCareReceived = self.p['zeroYearCare']
                child.unmetChildCareNeed = 0
                child.mother.childWork = self.p['zeroYearCare']
            
            for child in children:
                child.hoursChildCareDemand = max(0, self.p['childCareDemand'] - child.unmetSocialCareNeed)
            
#            householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
#            employed = [x for x in householdCarers if x.status == 'worker']
#            householdIncome = 0
#            for worker in employed:
#                worker.income = worker.residualWorkingHours*worker.wage
            house.totalChildCareNeed = 0
            income = sum([x.income for x in household])
            if income  < self.p['maxHouseholdIncomeChildCareSupport']:
                firstGroup = [x for x in children if x.age < 2]
                for child in firstGroup:
                    child.unmetChildCareNeed = child.hoursChildCareDemand
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                secondGroup = [x for x in children if x.age  == 2]
                for child in secondGroup:
                    child.unmetChildCareNeed = max(0, child.hoursChildCareDemand - self.p['freeChildCareHoursToddlers'])
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                    self.publicChildCare += min(child.hoursChildCareDemand, self.p['freeChildCareHoursToddlers'])
                thirdGroup = [x for x in children if x.age > 2 and x.age < 5]
                for child in thirdGroup:
                    child.unmetChildCareNeed = max(0, child.hoursChildCareDemand - self.p['freeChildCareHoursPreSchool'])
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                    self.publicChildCare += min(child.hoursChildCareDemand, self.p['freeChildCareHoursPreSchool'])
                fourthGroup = [x for x in children if x.age > 4]
                for child in fourthGroup:
                    child.unmetChildCareNeed = max(0, child.hoursChildCareDemand - self.p['freeChildCareHoursSchool'])
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                    self.publicChildCare += min(child.hoursChildCareDemand, self.p['freeChildCareHoursSchool'])
            else:
                firstGroup = [x for x in children if x.age < 3]
                for child in firstGroup:
                    child.unmetChildCareNeed = child.hoursChildCareDemand
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                secondGroup = [x for x in children if x.age > 2 and x.age < 5]
                for child in secondGroup:
                    child.unmetChildCareNeed = max(0, child.hoursChildCareDemand - self.p['freeChildCareHoursPreSchool'])
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                    self.publicChildCare += min(child.hoursChildCareDemand, self.p['freeChildCareHoursPreSchool'])
                thirdGroup = [x for x in children if x.age > 4]
                for child in thirdGroup:
                    child.unmetChildCareNeed = max(0, child.hoursChildCareDemand - self.p['freeChildCareHoursSchool'])
                    child.netChildCareDemand = child.unmetChildCareNeed
                    house.totalChildCareNeed += child.unmetChildCareNeed
                    self.publicChildCare += min(child.hoursChildCareDemand, self.p['freeChildCareHoursSchool'])
                    
            children.sort(key=operator.attrgetter("unmetChildCareNeed"))
            
            totalNeed = sum([x.unmetChildCareNeed for x in children])
            discountedNeed = sum([min(self.p['childcareTaxFreeCap'], x.unmetChildCareNeed) for x in children])
            if totalNeed > 0:
                ratio = discountedNeed/totalNeed
            else:
                ratio = 0.0
            house.averageChildCarePrice = self.p['priceChildCare']*(1.0-ratio) + self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])*ratio
                
            residualNeeds = [x.unmetChildCareNeed for x in children]
            marginalNeeds = []
            numbers = []
            toSubtract = 0
            for need in residualNeeds:
                marginalNeed = need-toSubtract
                if marginalNeed > 0:
                    marginalNeeds.append(marginalNeed)
                    num = len([x for x in residualNeeds if x >= need])
                    numbers.append(num)                
                    toSubtract = need
            house.childCareNeeds = marginalNeeds
            house.cumulatedChildren = numbers
            
            prices = []
            residualCare = 0
            cumulatedCare = 0
            for i in range(len(numbers)):
                cost = 0
                residualCare = house.childCareNeeds[i]
                for child in children[-numbers[i]:]:
                    if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                        cost += self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])*residualCare
                    else:
                        if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
                            cost += self.p['priceChildCare']*residualCare
                        else:
                            discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
                            cost1 = discountedCare*self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])
                            fullPriceCare = residualCare - discountedCare
                            cost2 = fullPriceCare*self.p['priceChildCare']
                            cost += (cost1 + cost2)
                cumulatedCare += house.childCareNeeds[i]
                prices.append(cost/house.childCareNeeds[i])
            house.childCarePrices = prices
            
            # Compite high and low price chil care need
            house.highPriceChildCare = 0
            house.lowPriceChildCare = 0
            for i in range(len(house.childCarePrices)):
                if house.childCarePrices[i] >= self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']):
                    house.highPriceChildCare += house.childCareNeeds[i]
                else:
                    house.lowPriceChildCare += house.childCareNeeds[i]
                    
            if house.totalChildCareNeed > 0 and (house.highPriceChildCare+house.lowPriceChildCare) <= 0:
                print 'Error: mismatch between total child care needs in computeChildCareNeeds'
                print residualNeeds
                print house.totalChildCareNeed
                print house.childCareNeeds
                print house.childCarePrices
                print house.highPriceChildCare
                print house.lowPriceChildCare
                sys.exit()
        
        children = [x for x in self.pop.livingPeople if x.age > 0 and x.age < self.p['ageTeenagers']]
        totalChildCareNeed = sum([x.hoursChildCareDemand for x in children])
        totalUnmetChildCareNeed = sum([x.unmetChildCareNeed for x in children])
      
        self.costPublicChildCare = self.publicChildCare*self.p['priceChildCare']
        self.sharePublicChildCare = 0
        if totalChildCareNeed > 0:
            self.sharePublicChildCare = 1.0 - float(totalUnmetChildCareNeed)/float(totalChildCareNeed)
            
    def householdCareSupply(self):
        
        for house in self.map.occupiedHouses:
        
            household = list(house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.hoursSocialCareDemand == 0 and x.maternityStatus == False]
            for member in householdCarers:
                if member.status == 'teenager':
                    member.residualInformalSupplies = list(self.p['teenagerSupply'])
                elif member.status == 'student' and member.outOfTownStudent == False:
                    member.residualInformalSupplies = list(self.p['studentSupply'])
                elif member.status == 'retired':
                    member.residualInformalSupplies = list(self.p['retiredSupply'])
                elif member.status == 'worker' and member.careNeedLevel == 0:
                    member.residualInformalSupplies = list(self.p['employedSupply'])
                # member.residualInformalSupplies = [max(x-member.hoursSocialCareDemand, 0) for x in member.residualInformalSupplies]
                member.hoursInformalSupplies = member.residualInformalSupplies
                
            house.householdInformalSupplies = []
            for i in range(4):
                house.householdInformalSupplies.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            
            employed = [x for x in householdCarers if x.status == 'worker']
            for worker in employed:
                if worker.careNeedLevel < 2:
                    worker.residualWorkingHours = self.p['weeklyHours'][worker.careNeedLevel]
                    worker.availableWorkingHours = worker.residualWorkingHours
                worker.potentialIncome = self.p['weeklyHours'][worker.careNeedLevel]*worker.wage
                
            potentialIncomes = [x.potentialIncome for x in household if x.maternityStatus == False]
            potentialIncomes.extend([x.income for x in household if x.status == 'retired'])
            potentialIncome = sum(potentialIncomes)
            
            house.residualIncomeForChildCare = potentialIncome
            house.initialResidualIncomeForChildCare = house.residualIncomeForChildCare
            
            # The household's tax brackets are the sum of the individual income brackets.
            taxBands = len(self.p['taxBrackets'])
            house.incomeByTaxBand = [0]*taxBands
            house.incomeByTaxBand[-1] = potentialIncome
            for i in range(taxBands-1):
                for income in potentialIncomes:
                    if income > self.p['taxBrackets'][i]:
                        bracket = income-self.p['taxBrackets'][i]
                        house.incomeByTaxBand[i] += bracket
                        house.incomeByTaxBand[-1] -= bracket
                        potentialIncomes[potentialIncomes.index(income)] -= bracket
                        

    def computeNetCareDemand(self):
        for house in self.map.occupiedHouses:
            house.suppliers = [house]
            house.suppliers.extend(list(house.careNetwork.neighbors(house)))
            house.receivers = list(house.demandNetwork.neighbors(house))
            totalDemand = house.totalUnmetSocialCareNeed + sum(house.childCareNeeds) # Total informal care need
            totalSupply = house.householdInformalSupplies[0]# Total internal care supply
            house.netCareDemand = totalDemand - totalSupply
            
                        
    def householdRelocation(self, policyFolder):
        shareRelocated = 0
        relocated = 0
        numHouseholds = len(self.map.occupiedHouses)
        for house in self.map.occupiedHouses:
            householdIncome = sum([x.income for x in house.occupants])
            perCapitaIncome = householdIncome/float(len(house.occupants))
            if house.netCareDemand > 0:
                house.careAttractionFactor = house.netCareDemand/math.exp(self.p['careAttractionExp']*perCapitaIncome)
            else:
                house.careAttractionFactor = house.netCareDemand
        
        for house in self.map.occupiedHouses:
            house.townAttractiveness = []
            if house.newOccupancy == True:
                continue
            
            houseRank = max([x.classRank for x in house.occupants])
            householdIncome = sum([x.income for x in house.occupants])
            perCapitaIncome = householdIncome/float(len(house.occupants))
            house.sizeIndex = self.computeHouseholdDimension(house) - 1
            
            for town in self.map.towns:
                # First element: care-related factor (KNA)
                
                # If the household has positive net demand, the care attraction associated with a town depends on quantity of net supply within the 
                # household's care supply network.
                # Vice versa, if the household has positive net supply, the care attraction associated with a town depends on quantity of net supply within the
                # household's care demand network.
                
                if house.netCareDemand > 0:
                    neighbors = [x for x in house.suppliers if x != house and x.town in town.neighboringTowns and x.careAttractionFactor < 0]
                    distances = [house.careNetwork[house][x]['distance'] for x in neighbors]
                else:
                    neighbors = [x for x in house.receivers if x != house and x.town in town.neighboringTowns and x.careAttractionFactor > 0]
                    distances = [house.demandNetwork[house][x]['distance'] for x in neighbors]
                    
                cares = [x.careAttractionFactor for x in neighbors]
                # The total care demand/supply is weighted by the kinship distance
                totalCare = sum([abs(x)/math.pow(self.p['networkDistanceParam'], distances[cares.index(x)]) for x in cares])
#                for care in cares:
#                    distance = distances[cares.index(care)]
#                    totalCareWeight += abs(care)/math.pow(self.p['networkDistanceParam'], distance)
                
                # The total attraction depends on the product of the house care the network care: if the household has not net demand, ther is no use for
                # the network net supply, and vice versa,
                kinshipNetworkAttraction = abs(house.careAttractionFactor)*totalCare
                careFactor = math.exp(self.p['knaExp']*kinshipNetworkAttraction)
                
                
                # Second element: economic and social factors (sea)
                sameSES = len([x for x in town.houses if len(x.occupants) > 0 and max([y.classRank for y in x.occupants]) >= houseRank])
                allHouses = len([x for x in town.houses if len(x.occupants) > 0])
                townSESShare = 0.0
                if allHouses > 0:
                    townSESShare = float(sameSES)/float(allHouses)
                sameSES = len([x for x in self.map.allHouses if len(x.occupants) > 0 and max([y.classRank for y in x.occupants]) == houseRank])
                allHouses = len([x for x in self.map.allHouses if len(x.occupants) > 0])
                mapSESShare = float(sameSES)/float(allHouses)
                deltaSES = townSESShare - mapSESShare
                sesFactor = math.exp(self.p['sesShareExp']*deltaSES)
                relRent = house.town.LHA[house.sizeIndex]/(house.town.LHA[house.sizeIndex]+math.exp(self.p['relativeRentExp']*perCapitaIncome))
                rentFactor = 1/math.exp(self.p['rentExp']*relRent)
                
#                townHouses = len([x for x in town.houses if len(x.occupants) == 0])
#                mapHouses = len([x for x in self.map.allHouses if len(x.occupants) == 0])
#                shareAvailableHouses = float(townHouses)/float(mapHouses)
                sea = sesFactor*rentFactor
                
                # Town's total attractiveness (TTA)
                townTotalAttractiveness = careFactor*sea
                
                house.townAttractiveness.append(townTotalAttractiveness)
            
            # 1 - Sample a town other than the one where the family is living
            probTowns = []
            potentialTowns = []
            for town in self.map.towns:
                if town == house.town:
                    continue
                potentialTowns.append(town)
                indexTown = self.map.towns.index(town)
                townAttractiveness = house.townAttractiveness[indexTown]
                townHouses = len([x for x in town.houses if len(x.occupants) == 0])
                mapHouses = len([x for x in self.map.allHouses if len(x.occupants) == 0])
                shareAvailableHouses = float(townHouses)/float(mapHouses)
                probTowns.append(shareAvailableHouses*townAttractiveness)
            prob = [x/sum(probTowns) for x in probTowns]
            newTown = np.random.choice(potentialTowns, p = prob)
            
            # 2 - Decide whether to relocate to the new town or remain in the current one
            indexNewTown = self.map.towns.index(newTown)
            indexCurrentTown = self.map.towns.index(house.town)
            newTownAttractiveness = house.townAttractiveness[indexNewTown]
            currentTownAttractiveness = house.townAttractiveness[indexCurrentTown]
            attractivenessRatio = newTownAttractiveness/(newTownAttractiveness+currentTownAttractiveness)
            relocationCost = sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in house.occupants])
            probRelocation = attractivenessRatio/math.exp(self.p['relocationCostBeta']*relocationCost)
            probRelocation *= self.p['scalingFactor']
            
            # print 'Prob Relocation: ' + str(probRelocation)
            
#                # Compute relocation probability
#                relocationCost = self.p['relocationCostParam']*sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in household])
#                supportNetworkFactor = math.exp(self.p['supportNetworkBeta']*house.networkSupport)
#                relocationCostFactor = math.exp(self.p['relocationCostBeta']*relocationCost)
#                perCapitaIncome = self.computeHouseholdIncome(house)/float(len(household))
#                incomeFactor = math.exp(self.p['incomeRelocationBeta']*perCapitaIncome)
#                relativeRelocationFactor = (supportNetworkFactor*relocationCostFactor)/incomeFactor
#                probRelocation = self.p['baseRelocationRate']/relativeRelocationFactor
           
            if random.random() < probRelocation: #self.p['basicProbFamilyMove']*self.p['probFamilyMoveModifierByDecade'][int(ageClass)]:
                
                relocated += 1
                
                peopleToMove = [x for x in house.occupants]
#                    personChildren = self.bringTheKids(person)
#                    peopleToMove += personChildren
#                    partnerChildren = self.bringTheKids(person.partner)
#                    peopleToMove += [x for x in partnerChildren if x not in personChildren]
#                    stepChildrenPartner = [x for x in personChildren if x not in partnerChildren]
#                    stepChildrenPerson = [x for x in partnerChildren if x not in personChildren]
#                    person.children.extend(stepChildrenPerson)
#                    person.partner.children.extend(stepChildrenPartner)
                
                # Add a choice of town which depends on kinship network and available houses.
                
#                if person.house == self.displayHouse:
#                    messageString = str(self.year) + ": #" + str(person.id) + " and #" + str(person.partner.id) + " move house"
#                    if len(peopleToMove) > 2:
#                        messageString += " with kids"
#                    messageString += "."
#                    self.textUpdateList.append(messageString)
                # self.findNewHouse(peopleToMove,distance)
                self.findNewHouseInNewTown(peopleToMove, newTown, policyFolder)
        
        shareRelocated = float(relocated)/float(numHouseholds)
        print shareRelocated
        
        # Update display house
        if len(self.displayHouse.occupants) < 1:
            self.displayHouse.display = False
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.displayHouse.display = True
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.displayHouse.display = True
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
                
                
    def computeHouseholdDimension(self, house):
        # Compute number of rooms for housing benefit purposes
        adults = [x for x in house.occupants if x.age > 15]
        houseBenefitRoom = 0
        visited = []
        for person in adults:
            if person in visited:
                continue
            visited.append(person)
            if person.partner != None:
                visited.append(person.partner)
            houseBenefitRoom +=1
        rooms = []
        children = [x for x in house.occupants if x.age < 16]
        children.sort(key=operator.attrgetter("age"), reverse = True)
        allocated = []
        for child in children:
            roomMates = []
            if child in allocated:
                continue
            allocated.append(child)
            roomMates.append(child)
            if child.age > 9:
                # Only another child of same sex can go with him
                sameSexChildren = [x for x in children if x.sex == child.sex and x.id != child.id]
                if len(sameSexChildren) > 0:
                    allocated.append(sameSexChildren[0])
                    roomMates.append(sameSexChildren[0])
            else:
                # Any child can share the room
                otherChildren = [x for x in children if x.id != child.id]
                if len(otherChildren) > 0:
                    allocated.append(otherChildren[0])
                    roomMates.append(otherChildren[0])
            rooms.append(roomMates)
        houseBenefitRoom += len(rooms)
        houseBenefitRoom = min(houseBenefitRoom, 4)
        houseBenefitRoom -= 1
        return houseBenefitRoom
        
    def doAgeTransitions(self, policyFolder):
        
        for person in self.pop.livingPeople:
            person.age += 1
            person.yearInTown += 1
            person.maternityStatus = False
        """Check whether people have moved on to a new status in life."""
        peopleNotYetRetired = [x for x in self.pop.livingPeople if x.status != 'retired']
        for person in peopleNotYetRetired:
            age = self.year - person.birthdate
            ## Do transitions to adulthood and retirement
            if person.age == self.p['ageTeenagers']:
                person.status == 'teenager'
            if person.age == self.p['ageOfAdulthood']:
                person.status = 'student'
                if np.random.random() < self.p['probOutOfTownStudent']:
                    person.outOfTownStudent = True
                person.classRank = 0 # max(person.father.classRank, person.mother.classRank)
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " is now an adult."
                    self.textUpdateList.append(messageString)
                        
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                        
                        
            elif person.age == self.p['ageOfRetirement']:
                person.status = 'retired'
#                person.wage = 0
#                dK = np.random.normal(0, self.p['wageVar'])
#                person.income *= 0.7*math.exp(dK) #self.p['pensionWage'][person.classRank]*self.p['weeklyHours'][0]
#                person.potentialIncome = person.income
                
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " has now retired."
                    self.textUpdateList.append(messageString)
                        
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])

            ## If somebody is still at home but their parents have died, promote them to independent adult
            if person.mother != None:
                if person.status == 'worker' and person.mother not in person.house.occupants and person.father not in person.house.occupants:
                    person.independentStatus = True
            if person.status == 'student' and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                if person.mother.dead:
                    if person.father.dead:
                        person.independentStatus = True
                        self.startWorking(person)
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + "'s parents are both dead."
                            self.textUpdateList.append(messageString)
                                
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                    else:
                        self.movePeopleIntoChosenHouse(person.father.house, person.house,[person], 0, policyFolder)
                else:
                    self.movePeopleIntoChosenHouse(person.mother.house, person.house,[person], 0, policyFolder)
                    
            ## If somebody is a *child* at home and their parents have died, they need to be adopted
            if person.status == 'retired' and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                person.independentStatus = True
            
            if person.status == 'child' and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                if person.mother.dead:
                    if person.father.dead:
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + "will now be adopted."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
        
                        while True:
                            adoptiveMother = random.choice(self.pop.livingPeople)
                            if ( adoptiveMother.status != 'child'
                                 and adoptiveMother.sex == 'female'
                                 and adoptiveMother.partner != None ):
                                break
        
                        person.mother = adoptiveMother
                        adoptiveMother.children.append(person)
                        person.father = adoptiveMother.partner
                        adoptiveMother.partner.children.append(person)                
        
                        if adoptiveMother.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " has been newly adopted by " + str(adoptiveMother.id) + "." 
                            self.textUpdateList.append(messageString)
                                
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                            
                            
                        self.movePeopleIntoChosenHouse(adoptiveMother.house,person.house,[person], 0, policyFolder)   
                    else:
                        self.movePeopleIntoChosenHouse(person.father.house, person.house,[person], 0, policyFolder)
                else:
                    self.movePeopleIntoChosenHouse(person.mother.house, person.house,[person], 0, policyFolder)
                    
    def startWorking(self, person):
        
        person.status = 'worker'
        person.outOfTownStudent = False
        
        dKi = np.random.normal(0, self.p['wageVar'])
        person.initialIncome = self.p['incomeInitialLevels'][person.classRank]*math.exp(dKi)
        dKf = np.random.normal(dKi, self.p['wageVar'])
        person.finalIncome = self.p['incomeFinalLevels'][person.classRank]*math.exp(dKf)
        
        person.wage = person.initialIncome
        person.income = person.wage*self.p['weeklyHours'][int(person.careNeedLevel)]
        person.potentialIncome = person.income
    
    def doSocialTransition(self, policyFolder):
        
        for person in self.pop.livingPeople:
            if person.age == self.p['workingAge'][person.classRank] and person.status == 'student':
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                if person.classRank == 4:
                    probStudy = 0.0
                else:
                    probStudy = self.transitionProb(person) # Probability of keeping studying
                
                if random.random() > probStudy:
                    self.startWorking(person)
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " is now looking for a job."
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                        
                else:
                    person.classRank += 1
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " is now a student."
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                        
            
    def transitionProb (self, person):
        household = [x for x in person.house.occupants]
        if person.father.dead + person.mother.dead != 2:
            disposableIncome = sum([x.income for x in household])
            perCapitaDisposableIncome = disposableIncome/len(household)
            # print('Per Capita Disposable Income: ' + str(perCapitaDisposableIncome))
            
            if perCapitaDisposableIncome > 0.0:
                
                forgoneSalary = self.p['incomeInitialLevels'][person.classRank]*self.p['weeklyHours'][person.careNeedLevel]
                educationCosts = self.p['educationCosts'][person.classRank]
                
                # relCost = (forgoneSalary+educationCosts)/perCapitaDisposableIncome
                
                relCost = forgoneSalary/perCapitaDisposableIncome
                
                # Check variable
#                if self.year == self.p['getCheckVariablesAtYear']:
#                    self.relativeEducationCost.append(relCost) # 0.2 - 5
                
                incomeEffect = (self.p['costantIncomeParam']+1)/(math.exp(self.p['eduWageSensitivity']*relCost) + self.p['costantIncomeParam']) # Min-Max: 0 - 10
                
                targetEL = max(person.father.classRank, person.mother.classRank)
                
                dE = float(targetEL - person.classRank)
                expEdu = math.exp(self.p['eduRankSensitivity']*dE)
                educationEffect = expEdu/(expEdu+self.p['costantEduParam'])
                
                careEffect = 1/math.exp(self.p['careEducationParam']*person.socialWork)
                
                
                ### Fixing probability to keep studying   ######################
                
                pStudy = incomeEffect*educationEffect*careEffect
                
#                shareAdjustmentFactor = self.socialClassShares[person.classRank] - self.p['shareClasses'][person.classRank]
#                
#                pStudy *= math.exp(self.p['classAdjustmentBeta']*shareAdjustmentFactor)
                
                if person.classRank == 0 and self.socialClassShares[0] > 0.2:
                    pStudy *= 1.0/0.9
                
                if person.classRank == 0 and self.socialClassShares[0] < 0.2:
                    pStudy *= 0.85
                
                if person.classRank == 1 and self.socialClassShares[1] > 0.35:
                    pStudy *= 1.0/0.8
                    
                if person.classRank == 2 and self.socialClassShares[2] > 0.25:
                    pStudy *= 1.0/0.85
                    
                
                #####################################################################
                
                # pStudy = math.pow(incomeEffect, self.p['incEduExp'])*math.pow(educationEffect, 1-self.p['incEduExp'])
                if pStudy < 0:
                    pStudy = 0
                # Check
#                if self.year == self.p['getCheckVariablesAtYear']:
#                    self.probKeepStudying.append(pStudy)
#                    self.person.classRankStudent.append(person.classRank)
                
            else:
                # print('perCapitaDisposableIncome: ' + str(perCapitaDisposableIncome))
                pStudy = 0
        else:
            pStudy = 0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        #pStudy = 0.8
        return pStudy
    
    
    def updateIncome(self):
        
        for person in self.pop.livingPeople:
            if person.status == 'worker' and person.careNeedLevel < 2:
                person.workExperience *= self.p['workDiscountingTime']
                if person.maternityStatus == False:
                    if self.p['weeklyHours'][person.careNeedLevel] > 0:
                        person.workingPeriods += float(self.p['weeklyHours'][person.careNeedLevel])/40.0
                        person.workExperience += person.residualWorkingHours/40.0
                    person.wage = self.computeWage(person)
                    person.income = person.wage*person.residualWorkingHours   # self.p['weeklyHours'][int(person.careNeedLevel)]
                    person.lastIncome = person.income
                elif person.maternityStatus == True:
                    person.wage = 0
                    person.income = 0
                   
            elif person.age == self.p['ageOfRetirement'] or person.careNeedLevel > 1:
                person.wage = 0
                shareWorkingTime = person.workingPeriods/float(self.p['minContributionYears'])
                dK = np.random.normal(0, self.p['wageVar'])
#                averageIncome = 0
#                if person.workingPeriods > 0:
#                    averageIncome = person.cumulativeIncome/person.workingPeriods
                person.income = person.lastIncome*shareWorkingTime*math.exp(dK) #self.p['pensionWage'][person.classRank]*self.p['weeklyHours'][0]
#                if person.income < self.p['statePension']:
#                    person.income = self.p['statePension']
            person.cumulativeIncome += (person.income - person.incomeExpenses)
            person.cumulativeIncome = max(person.cumulativeIncome, 0)
        
        self.grossDomesticProduct = sum([x.income for x in self.pop.livingPeople if x.wage > 0])
        
        for house in self.map.occupiedHouses:
            house.outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in house.occupants])
            house.householdIncome = sum([x.income for x in house.occupants])
            house.incomePerCapita = house.householdIncome/float(len(house.occupants))
           
        households = [x for x in self.map.occupiedHouses]
        households.sort(key=operator.attrgetter("incomePerCapita"))
        for i in range(5):
            number = int(round(len(households)/(5.0-float(i))))
            quintile = households[:number]
            for j in quintile:
                j.incomeQuintile = i
            households = [x for x in households if x not in quintile]
 
        # Compute tax revenue and income after tax
        earningPeople = [x for x in self.pop.livingPeople if x.status == 'worker' and x.maternityStatus == False]
        self.totalTaxRevenue = 0
        self.totalPensionRevenue = 0
        for person in earningPeople:
            employeePensionContribution = 0
            # Pension Contributions
            if person.income > 162.0:
                if person.income < 893.0:
                    employeePensionContribution = (person.income - 162.0)*0.12
                else:
                    employeePensionContribution = (893.0 - 162.0)*0.12
                    employeePensionContribution += (person.income - 893.0)*0.02
            person.income -= employeePensionContribution
            self.totalPensionRevenue += employeePensionContribution
            
            # Tax Revenues
            tax = 0
            residualIncome = person.income
            for i in range(len(self.p['taxBrackets'])):
                if residualIncome > self.p['taxBrackets'][i]:
                    taxable = residualIncome - self.p['taxBrackets'][i]
                    tax += taxable*self.p['taxationRates'][i]
                    residualIncome -= taxable
            person.income -= tax
            self.totalTaxRevenue += tax
        self.statePensionRevenue.append(self.totalPensionRevenue)
        self.stateTaxRevenue.append(self.totalTaxRevenue)
        
        # Pensions Expenditure
        pensioners = [x for x in self.pop.livingPeople if x.status == 'retired']
        totalIncome = sum([x.income for x in earningPeople if x.status == 'worker'])
        self.pensionExpenditure = self.p['statePension']*len(pensioners) + totalIncome*self.p['statePensionContribution']
        self.statePensionExpenditure.append(self.pensionExpenditure)
        
        # Assign incomes according to empirical income distribution
        #####   Temporarily disactivating the top-down income attribution   ############################
        
#        earningPeople = [x for x in self.pop.livingPeople if x.income > 0] #x.status == 'worker']
#        earningPeople.sort(key=operator.attrgetter("income"))
#        
#        workersToAssign = list(earningPeople)
#        incomePercentiles = []
#        for i in range(99, 0, -1):
#            groupNum = int(float(len(workersToAssign))/float(i))
#            workersGroup = workersToAssign[0:groupNum]
#            incomePercentiles.append(workersGroup)
#            workersToAssign = workersToAssign[groupNum:]
#        
#        for i in range(99):
#            wage = float(self.incomesPercentiles[i])/(52*40)
#            for person in incomePercentiles[i]:
#                dK = np.random.normal(0, self.p['wageVar'])
#                person.wage = wage*math.exp(dK)
#                person.income = person.wage*self.p['weeklyHours'][int(person.careNeedLevel)]
        
    def updateWealth_Ind(self):
        # Only workers: retired are assigned a wealth at the end of their working life (which they consume thereafter)
        earningPop = [x for x in self.pop.livingPeople if x.cumulativeIncome > 0]
        
        earningPop.sort(key=operator.attrgetter("cumulativeIncome"))
        
        peopleToAssign = list(earningPop)
        wealthPercentiles = []
        for i in range(100, 0, -1):
            groupNum = int(float(len(peopleToAssign))/float(i))
            peopleGroup = peopleToAssign[0:groupNum]
            wealthPercentiles.append(peopleGroup)
            peopleToAssign = peopleToAssign[groupNum:]
            
        for i in range(100):
            wealth = float(self.wealthPercentiles[i])
            for person in wealthPercentiles[i]:
                dK = np.random.normal(0, self.p['wageVar'])
                person.wealth = wealth*math.exp(dK)
                
        for person in self.pop.livingPeople:
            # Update financial wealth
            if person.wage > 0:
                person.financialWealth = person.wealth*self.p['shareFinancialWealth']
            else:
                person.financialWealth -= person.wealthSpentOnCare
            person.financialWealth = max(person.financialWealth, 0)
        
        notEarningPop = [x for x in self.pop.livingPeople if x.cumulativeIncome > 0 and x.wage == 0]
        for person in notEarningPop:
            person.financialWealth *= (1.0 + self.p['pensionReturnRate'])
            
    def updateWealth(self):
        households = [x for x in self.map.occupiedHouses]
        for h in households:
            h.householdCumulativeIncome = sum([x.cumulativeIncome for x in h.occupants])
        households.sort(key=operator.attrgetter("householdCumulativeIncome"))
        
        householdsToAssign = list(households)
        wealthPercentiles = []
        for i in range(100, 0, -1):
            groupNum = int(float(len(householdsToAssign))/float(i))
            householdGroup = householdsToAssign[0:groupNum]
            wealthPercentiles.append(householdGroup)
            householdsToAssign = householdsToAssign[groupNum:]
            
        for i in range(100):
            wealth = float(self.wealthPercentiles[i])
            for household in wealthPercentiles[i]:
                dK = np.random.normal(0, self.p['wageVar'])
                household.wealth = wealth*math.exp(dK)
        
        # Assign household wealth to single members
        for h in households:
            if h.householdCumulativeIncome > 0:
                earningMembers = [x for x in h.occupants if x.cumulativeIncome > 0]
                for m in earningMembers:
                    m.wealth = (m.cumulativeIncome/h.householdCumulativeIncome)*h.wealth
            else:
                independentMembers = [x for x in h.occupants if x.independentStatus == True]
                if len(independentMembers) > 0:
                    for m in independentMembers:
                        m.wealth = h.wealth/float(len(independentMembers))
            
        
        
    def computeWage(self, person):
        
        # newK = self.p['incomeFinalLevels'][classRank]*math.exp(dK)    
        # c = np.math.log(self.p['incomeInitialLevels'][classRank]/newK)
        # wage = newK*np.math.exp(c*np.math.exp(-1*self.p['incomeGrowthRate'][classRank]*workExperience))
        c = np.math.log(person.initialIncome/person.finalIncome)
        wage = person.finalIncome*np.math.exp(c*np.math.exp(-1*self.p['incomeGrowthRate'][person.classRank]*person.workExperience))
        dK = np.random.normal(0, self.p['wageVar'])
        wage *= math.exp(dK)
        return wage
    
    def computeBirthProb(self, fertilityBias, rawRate, womanRank):
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female' and x.age >= self.p['minPregnancyAge']]
        womanClassShares = []
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 0])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 1])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 2])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 3])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 4])/float(len(womenOfReproductiveAge)))
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += womanClassShares[i]*math.pow(self.p['fertilityBias'], i)
        baseRate = rawRate/a
        birthProb = baseRate*math.pow(self.p['fertilityBias'], womanRank)
        return birthProb
    
    def doBirths(self, policyFolder):
        
        preBirth = len(self.pop.livingPeople)
        
        marriedLadies = 0
        adultLadies = 0
        births = [0, 0, 0, 0, 0]
        marriedPercentage = []
        
        adultWomen = [x for x in self.pop.livingPeople
                                       if x.sex == 'female' and x.age >= self.p['minPregnancyAge']]
        
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age >= self.p['minPregnancyAge']
                                  and x.age <= self.p['maxPregnancyAge']
                                  and x.partner != None]
        
        adultLadies_1 = [x for x in adultWomen if x.classRank == 0]   
        marriedLadies_1 = len([x for x in adultLadies_1 if x.partner != None])
        if len(adultLadies_1) > 0:
            marriedPercentage.append(marriedLadies_1/float(len(adultLadies_1)))
        else:
            marriedPercentage.append(0)
        adultLadies_2 = [x for x in adultWomen if x.classRank == 1]    
        marriedLadies_2 = len([x for x in adultLadies_2 if x.partner != None])
        if len(adultLadies_2) > 0:
            marriedPercentage.append(marriedLadies_2/float(len(adultLadies_2)))
        else:
            marriedPercentage.append(0)
        adultLadies_3 = [x for x in adultWomen if x.classRank == 2]   
        marriedLadies_3 = len([x for x in adultLadies_3 if x.partner != None]) 
        if len(adultLadies_3) > 0:
            marriedPercentage.append(marriedLadies_3/float(len(adultLadies_3)))
        else:
            marriedPercentage.append(0)
        adultLadies_4 = [x for x in adultWomen if x.classRank == 3]  
        marriedLadies_4 = len([x for x in adultLadies_4 if x.partner != None])   
        if len(adultLadies_4) > 0:
            marriedPercentage.append(marriedLadies_4/float(len(adultLadies_4)))
        else:
            marriedPercentage.append(0)
        adultLadies_5 = [x for x in adultWomen if x.classRank == 4]   
        marriedLadies_5 = len([x for x in adultLadies_5 if x.partner != None]) 
        if len(adultLadies_5) > 0:
            marriedPercentage.append(marriedLadies_5/float(len(adultLadies_5)))
        else:
            marriedPercentage.append(0)
        
        # print(marriedPercentage)
        
#        for person in self.pop.livingPeople:
#           
#            if person.sex == 'female' and person.age >= self.p['minPregnancyAge']:
#                adultLadies += 1
#                if person.partner != None:
#                    marriedLadies += 1
#        marriedPercentage = float(marriedLadies)/float(adultLadies)
        
        for woman in womenOfReproductiveAge:
            
            womanClassRank = woman.classRank
            if woman.status == 'student':
                womanClassRank = woman.parentsClassRank

            if self.year < self.p['fertilityDataFrom']:
                rawRate = self.p['growingPopBirthProb']
                birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, womanClassRank)
            else:
                rawRate = self.fert_data[(self.year - woman.birthdate)-16, self.year-int(self.p['fertilityDataFrom'])]
                birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, womanClassRank)/marriedPercentage[womanClassRank]
                
            # birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, woman.classRank)
            
            #baseRate = self.baseRate(self.socialClassShares, self.p['fertilityBias'], rawRate)
            #fertilityCorrector = (self.socialClassShares[woman.classRank] - self.p['initialClassShares'][woman.classRank])/self.p['initialClassShares'][woman.classRank]
            #baseRate *= 1/math.exp(self.p['fertilityCorrector']*fertilityCorrector)
            #birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
            
            if random.random() < birthProb:
                # (self, mother, father, age, birthYear, sex, status, house,
                # classRank, sec, edu, wage, income, finalIncome):
                parentsClassRank = max([woman.classRank, woman.partner.classRank])
                baby = Person(woman, woman.partner, self.year, 0, 'random', woman.house, woman.sec, -1, parentsClassRank, 0, 0, 0, 0, 0, 0, 'child', False)
                self.pop.allPeople.append(baby)
                self.pop.livingPeople.append(baby)
                woman.house.occupants.append(baby)
                woman.children.append(baby)
                woman.partner.children.append(baby)
                woman.maternityStatus = True
                woman.residualWorkingHours = 0
                woman.availableWorkingHours = 0
                woman.potentialIncome = 0
                woman.income = 0
                if woman.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(woman.id) + " had a baby, #" + str(baby.id) + "." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                    
        postBirth = len(self.pop.livingPeople)

        self.births = postBirth - preBirth
        self.shareBirths = float(self.births)/float(postBirth-self.births)
        
        print('the number of births is: ' + str(postBirth - preBirth))
    
    def computeSplitProb(self, rawRate, classRank):
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(self.p['divorceBias'], i)
        baseRate = rawRate/a
        splitProb = baseRate*math.pow(self.p['divorceBias'], classRank)
        return splitProb
            
    def doDivorces(self, policyFolder):
        menInRelationships = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner != None ]
        for man in menInRelationships:
            
            age = self.year - man.birthdate 

            ## This is here to manage the sweeping through of this parameter
            ## but only for the years after 2012
            if self.year < self.p['thePresent']:
                rawRate = self.p['basicDivorceRate'] * self.p['divorceModifierByDecade'][int(age)/10]
            else:
                rawRate = self.p['variableDivorce'] * self.p['divorceModifierByDecade'][int(age)/10]
                
            splitProb = self.computeSplitProb(rawRate, man.classRank)
                
            if random.random() < splitProb:
                # man.children = []
                wife = man.partner
                man.partner = None
                wife.partner = None
                man.yearDivorced.append(self.year)
                wife.yearDivorced.append(self.year)
                if wife.status == 'student':
                    wife.independentStatus = True
                    self.startWorking(wife)
                self.divorceTally += 1
                distance = random.choice(['near','far'])
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " splits with #" + str(wife.id) + "."
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                    
                # manChildren = [x for x in man.children if x.dead == False and x.house == man.house and x.father == man and x.mother != wife]
                
                manChildren = []
                children = [x for x in man.children if x.dead == False and x.house == man.house]
                for child in children:
                    if child.father == man and child.mother != wife:
                        manChildren.append(child)
                    else:
                        if np.random.random() < self.p['probChildrenWithFather']:
                            manChildren.append(child)
                
#                for x in manChildren:
#                    if x not in man.house.occupants:
#                        print 'Error in doDivorce: man children not in house'
#                        sys.exit()
                        
                peopleToMove = [man]
                peopleToMove += manChildren
                self.findNewHouse(peopleToMove,distance, policyFolder)
                
    def doMarriages(self, policyFolder):
        
        eligibleMen = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner == None and x.status != 'child' and x.status != 'student']
        eligibleWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.partner == None and x.status != 'child']
        
        
        if len(eligibleMen) > 0 and len (eligibleWomen) > 0:
            random.shuffle(eligibleMen)
            random.shuffle(eligibleWomen)
            
            interestedWomen = []
            for w in eligibleWomen:
                womanMarriageProb = self.p['basicFemaleMarriageProb']*self.p['femaleMarriageModifierByDecade'][w.age/10]
                if random.random() < womanMarriageProb:
                    interestedWomen.append(w)
        
            for man in eligibleMen:
                
                ageClass = int(man.age/10)
                manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][ageClass]
                
                ageClassPop = [x for x in eligibleMen if int(x.age/10) == ageClass]
                noChildrenMen = [x for x in ageClassPop if len([y for y in x.children if y.dead == False and y.house == x.house]) == 0]
                shareNoChildren = float(len(noChildrenMen))/float(len(ageClassPop))
                den = shareNoChildren + (1-shareNoChildren)*self.p['manWithChildrenBias']
                baseRate = manMarriageProb/den
                if man in noChildrenMen:
                    manMarriageProb = baseRate
                else:
                    manMarriageProb = baseRate*self.p['manWithChildrenBias']
                
                
                # Adjusting for number of children
#                numChildrenWithMan = len([x for x in man.children if x.house == man.house])
#                childrenFactor = 1/math.exp(self.p['numChildrenExp']*numChildrenWithMan)
#                manMarriageProb *= childrenFactor
                
                # Adjusting to increase rate
                manMarriageProb *= self.p['maleMarriageMultiplier']
                
                
                if random.random() < manMarriageProb:
                    potentialBrides = []
                    for woman in interestedWomen:
                        deltaAge = man.age - woman.age
                        if deltaAge < 20 and deltaAge > -10:
                            if woman.house != man.house:
                                if man.mother != None and woman.mother != None:
                                    if man.mother != woman.mother and man not in woman.children and woman not in man.children:
                                        potentialBrides.append(woman)
                                else:
                                    if man not in woman.children and woman not in man.children:
                                        potentialBrides.append(woman)
                    
                    if len(potentialBrides) > 0:
                        manTown = man.house.town
                        bridesWeights = []
                        for woman in potentialBrides:
                            
                            womanTown = woman.house.town
                            geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                            geoFactor = 1/math.exp(self.p['betaGeoExp']*geoDistance)
                            
                            womanRank = woman.classRank
                            studentFactor = 1.0
                            if woman.status == 'student':
                                studentFactor = self.p['studentFactorParam']
                                womanRank = max(woman.father.classRank, woman.mother.classRank)
                            statusDistance = float(abs(man.classRank-womanRank))/float((self.p['numberClasses']-1))
                            if man.classRank < womanRank:
                                betaExponent = self.p['betaSocExp']
                            else:
                                betaExponent = self.p['betaSocExp']*self.p['rankGenderBias']
                            socFactor = 1/math.exp(betaExponent*statusDistance)
                            
                            ageFactor = self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                            
                            numChildrenWithWoman = len([x for x in woman.children if x.house == woman.house])
                            
                            childrenFactor = 1/math.exp(self.p['bridesChildrenExp']*numChildrenWithWoman)
                            
                            marriageProb = geoFactor*socFactor*ageFactor*childrenFactor*studentFactor
                            
                            bridesWeights.append(marriageProb)
                            
                        if sum(bridesWeights) > 0:
                            bridesProb = [i/sum(bridesWeights) for i in bridesWeights]
                            woman = np.random.choice(potentialBrides, p = bridesProb)
                        else:
                            woman = np.random.choice(potentialBrides)
                        man.partner = woman
                        woman.partner = man
                        man.yearMarried.append(self.year)
                        woman.yearMarried.append(self.year)
                        interestedWomen.remove(woman)
                        
                        self.marriageTally += 1
    
                        if man.house == self.displayHouse or woman.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                            messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                            messageString += ") marry."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
        
    def deltaAge(self, dA):
        if dA <= -10 :
            cat = 0
        elif dA >= -9 and dA <= -3:
            cat = 1
        elif dA >= -2 and dA <= 0:
            cat = 2
        elif dA >= 1 and dA <= 4:
            cat = 3
        elif dA >= 5 and dA <= 9:
            cat = 4
        else:
            cat = 5
        return cat

    
    def doMovingAround(self, policyFolder):
        """
        Various reasons why a person or family group might want to
        move around. People who are in partnerships but not living
        together are highly likely to find a place together. Adults
        still living at home might be ready to move out this year.
        Single people might want to move in order to find partners. A
        family might move at random for work reasons. Older people
        might move back in with their kids.
        """
        for i in self.pop.livingPeople:
            i.movedThisYear = False
            
        ## Need to keep track of this to avoid multiple moves
        separetedSpouses = [x for x in self.pop.livingPeople if x.partner != None and x.house != x.partner.house]
        couples = []
        for i in separetedSpouses:
            couples.append([i, i.partner])
            
        
            
        for person in separetedSpouses:
            
            
            if person.house != person.partner.house:
            
#                if len(person.yearMarried) > 0 and  person.yearMarried[-1] == self.year and person.house == person.partner.house:
#                    print 'Error: couple already in same house!'
#                    sys.exit()
                
                # if person.partner != None and person.house != person.partner.house:
                    ## so we have someone who lives apart from their partner...
                    ## very likely they will change that
                if random.random() < self.p['probApartWillMoveTogether']:
                    peopleToMove = [person,person.partner]
                    personChildren = self.bringTheKids(person)
                    personChildrenToMove = [x for x in personChildren if x not in separetedSpouses]
                    peopleToMove += personChildrenToMove
                    partnerChildren = self.bringTheKids(person.partner)
                    partnerChildrenToMove = [x for x in partnerChildren if x not in separetedSpouses]
                    peopleToMove += [x for x in partnerChildrenToMove if x not in personChildrenToMove]
                    
                    if random.random() < self.p['coupleMovesToExistingHousehold']:
                        myHousePop = len(person.house.occupants)
                        yourHousePop = len(person.partner.house.occupants)
                        if yourHousePop < myHousePop:
                            targetHouse = person.partner.house
                        else:
                            targetHouse = person.house
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " and #" + str(person.partner.id)
                            messageString += " move to existing household."
                            self.textUpdateList.append(messageString)
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                                
                        self.movePeopleIntoChosenHouse(targetHouse,person.house,peopleToMove, 0, policyFolder)                        
                    else:
                        distance = random.choice(['here','near'])
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " moves out to live with #" + str(person.partner.id)
                            if len(peopleToMove) > 2:
                                messageString += ", bringing the kids"
                            messageString += "."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                                
                        self.findNewHouse(peopleToMove,distance, policyFolder)                        
    
                    if person.independentStatus == False:
                        person.independentStatus = True
                    if person.partner.independentStatus == False:
                        person.partner.independentStatus = True

        for person in self.pop.livingPeople:
            age = self.year - person.birthdate
            ageClass = age / 10
            
            if person.movedThisYear:
                continue
            
            elif person.status == 'worker' and person.independentStatus == False and person.partner == None:
                ## a single person who hasn't left home yet
                if random.random() < ( self.p['basicProbAdultMoveOut']
                                       * self.p['probAdultMoveOutModifierByDecade'][ageClass] ):
                    peopleToMove = [person]
                    peopleToMove += self.bringTheKids(person)
                    distance = random.choice(['here','near'])
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " moves out, aged " + str(self.year-person.birthdate) + "."
                        self.textUpdateList.append(messageString)
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                            
                    self.findNewHouse(peopleToMove,distance, policyFolder)
                    person.independentStatus = True
                    

            elif person.independentStatus == True and person.partner == None:
                ## a young-ish person who has left home but is still (or newly) single
                if random.random() < ( self.p['basicProbSingleMove']
                                       * self.p['probSingleMoveModifierByDecade'][int(ageClass)] ):
                    peopleToMove = [person]
                    peopleToMove += self.bringTheKids(person)
                    distance = random.choice(['here','near'])
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " moves to meet new people."
                        self.textUpdateList.append(messageString)
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                            
                    self.findNewHouse(peopleToMove,distance, policyFolder)

            elif person.status == 'retired' and len(person.house.occupants) == 1:
                ## a retired person who lives alone
                for c in person.children:
                    if ( c.dead == False ):
                        distance = self.manhattanDistance(person.house.town,c.house.town)
                        distance += 1.0
                        if self.year < self.p['thePresent']:
                            mbRate = self.p['agingParentsMoveInWithKids']/distance
                        else:
                            mbRate = self.p['variableMoveBack']/distance
                        if random.random() < mbRate:
                            peopleToMove = [person]
                            if person.house == self.displayHouse:
                                messageString = str(self.year) + ": #" + str(person.id) + " is going to live with one of their children."
                                self.textUpdateList.append(messageString)
                                with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                    writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                    writer.writerow([self.year, messageString])
                                
                            self.movePeopleIntoChosenHouse(c.house,person.house,peopleToMove, 0, policyFolder)
                            break
                        
        
            
            elif person.partner != None and person.yearMarried[-1] != self.year:
                ## any other kind of married person, e.g., a normal family with kids
                house = person.house
                household = [x for x in house.occupants]
                
                # Compute relocation probability
                relocationCost = self.p['relocationCostParam']*sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in household])
                supportNetworkFactor = math.exp(self.p['supportNetworkBeta']*house.networkSupport)
                relocationCostFactor = math.exp(self.p['relocationCostBeta']*relocationCost)
                perCapitaIncome = self.computeHouseholdIncome(house)/float(len(household))
                incomeFactor = math.exp(self.p['incomeRelocationBeta']*perCapitaIncome)
                relativeRelocationFactor = (supportNetworkFactor*relocationCostFactor)/incomeFactor
                probRelocation = self.p['baseRelocationRate']/relativeRelocationFactor
               
                if random.random() < probRelocation: #self.p['basicProbFamilyMove']*self.p['probFamilyMoveModifierByDecade'][int(ageClass)]:
                    
                    peopleToMove = [x for x in person.house.occupants]
#                    personChildren = self.bringTheKids(person)
#                    peopleToMove += personChildren
#                    partnerChildren = self.bringTheKids(person.partner)
#                    peopleToMove += [x for x in partnerChildren if x not in personChildren]
#                    stepChildrenPartner = [x for x in personChildren if x not in partnerChildren]
#                    stepChildrenPerson = [x for x in partnerChildren if x not in personChildren]
#                    person.children.extend(stepChildrenPerson)
#                    person.partner.children.extend(stepChildrenPartner)
                    
                    # Add a choice of town which depends on kinship network and available houses.
                    
                    distance = random.choice(['here,''near','far'])
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " and #" + str(person.partner.id) + " move house"
                        if len(peopleToMove) > 2:
                            messageString += " with kids"
                        messageString += "."
                        self.textUpdateList.append(messageString)
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                        
                    self.findNewHouse(peopleToMove,distance, policyFolder)
                    
        
        # Update display house
        if len(self.displayHouse.occupants) < 1:
            self.displayHouse.display = False
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.displayHouse.display = True
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.displayHouse.display = True
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
                
    def manhattanDistance(self,t1,t2):
        """Calculates the distance between two towns"""
        xDist = abs(t1.x - t2.x)
        yDist = abs(t1.y - t2.y)
        return xDist + yDist


    def bringTheKids(self,person):
        """Given a person, return a list of their dependent kids who live in the same house as them."""
        returnList = []
        for i in person.children:
            if ( i.house == person.house
                 and i.independentStatus == False
                 and i.dead == False ):
                returnList.append(i)
        return returnList

    def findNewHouseInNewTown(self, personList, newTown, policyFolder):
        """Find an appropriate empty house for the named person and put them in it."""

        newHouse = None
        person = personList[0]
        departureHouse = person.house
        t = person.house.town
        availableHouses = [x for x in newTown.houses if len(x.occupants) == 0]
        newHouse = random.choice(availableHouses)

        ## Quit with an error message if we've run out of houses
        if newHouse in self.map.occupiedHouses:
            print 'Error in house selection: already occupied!'
            print newHouse.id
            
#        if newHouse == None:
#            print "No houses left for person of SEC " + str(person.sec)
#            sys.exit()

        ## Actually make the chosen move
        self.movePeopleIntoChosenHouse(newHouse, departureHouse, personList, 1, policyFolder)

    def findNewHouse(self, personList, preference, policyFolder):
        """Find an appropriate empty house for the named person and put them in it."""

        newHouse = None
        person = personList[0]
        departureHouse = person.house
        t = person.house.town

        if ( preference == 'here' ):
            ## Anything empty in this town of the right size?
            localPossibilities = [x for x in t.houses
                                  if len(x.occupants) < 1]
            if localPossibilities:
                newHouse = random.choice(localPossibilities)

        if ( preference == 'near' or newHouse == None ):
            ## Neighbouring towns?
            if newHouse == None:
                nearbyTowns = [ k for k in self.map.towns
                                if abs(k.x - t.x) <= 1
                                and abs(k.y - t.y) <= 1 ]
                nearbyPossibilities = []
                for z in nearbyTowns:
                    for w in z.houses:
                        if len(w.occupants) < 1:
                            nearbyPossibilities.append(w)
                if nearbyPossibilities:
                    newHouse = random.choice(nearbyPossibilities)

        if ( preference == 'far' or newHouse == None ):
            ## Anywhere at all?
            if newHouse == None:
                allPossibilities = []
                for z in self.map.allHouses:
                    if len(z.occupants) < 1:
                        allPossibilities.append(z)
                if allPossibilities:
                    newHouse = random.choice(allPossibilities)

        ## Quit with an error message if we've run out of houses
        if newHouse in self.map.occupiedHouses:
            print 'Error in house selection: already occupied!'
            print newHouse.id
            
#        if newHouse == None:
#            print "No houses left for person of SEC " + str(person.sec)
#            sys.exit()

        ## Actually make the chosen move
        self.movePeopleIntoChosenHouse(newHouse,departureHouse,personList, 1, policyFolder)


    def movePeopleIntoChosenHouse(self,newHouse,departureHouse,personList, case, policyFolder):

        ## Put the new house onto the list of occupied houses if it was empty
        household = list(personList)
        
        newHouse.newOccupancy = True
        
        if len(household) != len(set(household)):
            print 'Error in movePeopleIntoChosenHouse: double counting people'
            for member in household:
                print member.id
            sys.exit()
        
        
        ## Move everyone on the list over from their former house to the new one
        for i in household:
            if newHouse.town != departureHouse.town:
                i.yearInTown = 0
#            if i.house == newHouse:
#                print 'Error: new house is the old house!'
#                sys.exit()
                
            oldHouse = i.house
            
#            if i not in oldHouse.occupants:
#                print 'Error: person not in house.'
#                print i.house.id
#                print oldHouse.id
#                sys.exit()
                
            oldHouse.occupants.remove(i)
            
            if len(oldHouse.occupants) == 0:
                self.map.occupiedHouses.remove(oldHouse)
                ##print "This house is now empty: ", oldHouse
                if (self.p['interactiveGraphics']):
                    self.canvas.itemconfig(oldHouse.icon, state='hidden')
            
            newHouse.occupants.append(i)
            
            i.house = newHouse
            i.movedThisYear = True

        ## This next is sloppy and will lead to loads of duplicates in the
        ## occupiedHouses list, but we don't want to miss any -- that's
        ## much worse -- and the problem will be solved by a conversion
        ## to set and back to list int he stats method in a moment
        if case == 1:
            self.map.occupiedHouses.append(newHouse)
        
#        if len(self.map.occupiedHouses) != len(set(self.map.occupiedHouses)):
#            print 'Error: house appears twice in occupied houses!'
#            houses = []
#            for x in self.map.occupiedHouses:
#                if x in houses:
#                    print x.id
#                else:
#                    houses.append(x)
#            sys.exit()
        
        emptyOccupiedHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        
#        if len(emptyOccupiedHouses) > 0:
#            print 'Error: empty houses among occupied ones!'
#            for m in emptyOccupiedHouses:
#                print m.id
#            sys.exit()
        
        if (self.p['interactiveGraphics']):
            self.canvas.itemconfig(newHouse.icon, state='normal')

            
            
        ## Check whether we've moved into the display house
        if newHouse == self.displayHouse:
            messageString = str(self.year) + ": New people are moving into " + newHouse.name
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
            messageString = ""
            for k in personList:
                messageString += "#" + str(k.id) + " "
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
        ## or out of it...
        if departureHouse == self.displayHouse and len(departureHouse.occupants) < 1:
            self.nextDisplayHouse = newHouse
                
    
    def migrationStats_Pre(self):
        self.preEdinburghers = [x for x in self.pop.livingPeople if x.house.town.x == 13 and x.house.town.y == 18]
        self.preGlaswegians_West = [x for x in self.pop.livingPeople if x.house.town.x == 7 and x.house.town.y == 18]
        self.preGlaswegians_East = [x for x in self.pop.livingPeople if x.house.town.x == 8 and x.house.town.y == 18]
        self.preGlaswegians = self.preGlaswegians_West + self.preGlaswegians_East
        self.preAberdonians = [x for x in self.pop.livingPeople if x.house.town.x == 18 and x.house.town.y == 10]
        
    def migrationStats_Post(self):
        self.postEdinburghers = [x for x in self.pop.livingPeople if x.house.town.x == 13 and x.house.town.y == 18]
        self.postGlaswegians_West = [x for x in self.pop.livingPeople if x.house.town.x == 7 and x.house.town.y == 18]
        self.postGlaswegians_East = [x for x in self.pop.livingPeople if x.house.town.x == 8 and x.house.town.y == 18]
        self.postGlaswegians = self.postGlaswegians_West + self.postGlaswegians_East
        self.postAberdonians = [x for x in self.pop.livingPeople if x.house.town.x == 18 and x.house.town.y == 10]
        
        self.popEdinburgh = len(self.postEdinburghers)
        self.popGlasgow = len(self.postGlaswegians)
        self.popAberdeen = len(self.postAberdonians)
        
        self.fromEdinburgh = len([x for x in self.preEdinburghers if x not in self.postEdinburghers])
        self.toEdinburgh = len([x for x in self.postEdinburghers if x not in self.preEdinburghers])
        self.fromGlasgow = len([x for x in self.preGlaswegians if x not in self.postGlaswegians])
        self.toGlasgow = len([x for x in self.postGlaswegians if x not in self.preGlaswegians])
        self.fromAberdeen = len([x for x in self.preAberdonians if x not in self.postAberdonians])
        self.toAberdeen = len([x for x in self.postAberdonians if x not in self.preAberdonians])
        
        self.share_fromEdinburgh = float(self.fromEdinburgh)/float(self.popEdinburgh)
        self.share_toEdinburgh = float(self.toEdinburgh)/float(self.popEdinburgh)
        self.share_fromGlasgow = float(self.fromGlasgow)/float(self.popGlasgow)
        self.share_toGlasgow = float(self.toGlasgow)/float(self.popGlasgow)
        self.share_fromAberdeen = float(self.fromAberdeen)/float(self.popAberdeen)
        self.share_toAberdeen = float(self.toAberdeen)/float(self.popAberdeen)
    
    def doStats(self, policyFolder, dataMapFolder, dataHouseholdFolder):
        """Calculate annual stats and store them appropriately."""

        self.times.append(self.year)

        currentPop = len(self.pop.livingPeople)
        everLivedPop = len(self.pop.allPeople)
        self.pops.append(currentPop)
         
        
        potentialWorkers = [x for x in self.pop.livingPeople if x.age >= self.p['ageOfAdulthood'] and x.age < self.p['ageOfRetirement']]
        employed = [x for x in potentialWorkers if x.status == 'worker' and x.residualWorkingHours > 0]
        potentialHours = sum([self.p['weeklyHours'][x.careNeedLevel] for x in employed])
        actualHours = sum([x.residualWorkingHours for x in employed])
        
        shareEmployed = 0
        if len(potentialWorkers) > 0:
            shareEmployed = float(len(employed))/float(len(potentialWorkers))
        shareWorkHours = 0
        if potentialHours > 0:
            shareWorkHours = float(actualHours)/float(potentialHours)
        self.employmentRate.append(shareEmployed)
        self.shareWorkingHours.append(shareWorkHours)

        ## Check for double-included houses by converting to a set and back again
        self.map.occupiedHouses = list(set(self.map.occupiedHouses))

        parents = []
        for person in self.pop.livingPeople:
            for child in person.children:
                if person.house == child.house and person.partner != None and (child.age <= 15 or (child.age <= 18 and child.status == 'student')): # self.p['maxWtWChildAge']:
                    parents.append(person)
                    break
        numberCouples = float(len(parents))/2
        loneParents = []
        loneFemaleParents = []
        for person in self.pop.livingPeople:
            for child in person.children:
                if person.house == child.house and person.partner == None and (child.age <= 15 or (child.age <= 18 and child.status == 'student')): # self.p['maxWtWChildAge']:
                    loneParents.append(person)
                    if person.sex == 'female':
                        loneFemaleParents.append(person)
                    break
        numberLoneParents = float(len(loneParents))
        shareSingleParents = numberLoneParents/(numberCouples+numberLoneParents)
        shareFemaleSingleParent = 0
        if numberLoneParents > 0:
            shareFemaleSingleParent = float(len(loneFemaleParents))/numberLoneParents
        self.shareLoneParents.append(shareSingleParents)
        self.shareFemaleLoneParents.append(shareFemaleSingleParent)
        
        over64 = [x for x in self.pop.livingPeople if x.age >= 65]
        indipendentOver65 = [x for x in over64 if x.careNeedLevel == 0]
        lowDependencyOver65 = [x for x in over64 if x.careNeedLevel == 1]
        mediumDependencyOver65 = [x for x in over64 if x.careNeedLevel == 2 or x.careNeedLevel == 3]
        highDependencyOver65 = [x for x in over64 if x.careNeedLevel == 4]
        
#        if len(over64) > 0:
#            print 'independent Over 64: ' + str(float(len(indipendentOver65))/float(len(over64)))
#            print 'low dependency Over 64: ' + str(float(len(lowDependencyOver65))/float(len(over64)))
#            print 'medium dependency Over 64: ' + str(float(len(mediumDependencyOver65))/float(len(over64)))
#            print 'high dependency Over 64: ' + str(float(len(highDependencyOver65))/float(len(over64)))
#        
        if self.year == 2017:
            self.sesPops = []
            for i in range(int(self.p['numberClasses'])):
                self.sesPops.append(len([x for x in self.pop.livingPeople if x.age > 23 and x.classRank == i]))
            self.sesPopsShares = [float(x)/float(sum(self.sesPops)) for x in self.sesPops]
            lenFrequency = len(self.incomeDistribution)
            self.incomeFrequencies = [0]*lenFrequency
            households = [y.occupants for y in self.map.occupiedHouses]
            
            self.individualIncomes = [x.income*52 for x in self.pop.livingPeople if x.income > 0]
            
        
            self.householdIncomes = [sum([x.income*52 for x in y]) for y in households]
            
            for i in self.householdIncomes:
                ind = int(i/1000)
                if ind > -1 and ind < lenFrequency:
                    self.incomeFrequencies[ind] += 1

        ## Check for overlooked empty houses
        emptyHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        for h in emptyHouses:
            self.map.occupiedHouses.remove(h)
            if (self.p['interactiveGraphics']):
                self.canvas.itemconfig(h.icon, state='hidden')

        ## Avg household size (easily calculated by pop / occupied houses)
        numHouseholds = len(self.map.occupiedHouses)
        averageHouseholdSize = float(currentPop)/float(numHouseholds)
        self.avgHouseholdSize.append(averageHouseholdSize)

        self.numMarriages.append(self.marriageTally)
        self.numDivorces.append(self.divorceTally)            
        
        
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople])
        totalInformalSocialCare = sum([x.informalSocialCareReceived for x in self.pop.livingPeople])
        totalFormalSocialCare = sum([x.formalSocialCareReceived for x in self.pop.livingPeople])
        totalSocialCare = totalInformalSocialCare + totalFormalSocialCare
        totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople])
        share_InformalSocialCare = 0
        if totalSocialCare > 0:
            share_InformalSocialCare = totalInformalSocialCare/totalSocialCare
        
        print share_InformalSocialCare
        
        share_UnmetSocialCareNeed = 0
        if totalSocialCareNeed > 0:
            share_UnmetSocialCareNeed = totalUnmetSocialCareNeed/totalSocialCareNeed
        
        
        for house in self.map.occupiedHouses:
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in house.occupants])
#        print totalSocialCareNeed
#        if totalInformalSocialCare > 0:
#            print 'Share of in-house informal care: ' + str(float(self.inHouseInformalCare)/totalInformalSocialCare)
#        print share_UnmetSocialCareNeed
#        print ''
        
        outOfWorkSocialCare = [x.outOfWorkSocialCare for x in self.pop.livingPeople]
        totalOWSC = sum(outOfWorkSocialCare)
        shareOWSC = 0
        if totalInformalSocialCare > 0:
            shareOWSC = totalOWSC/totalInformalSocialCare
        totalCostOWSC = sum([x.outOfWorkSocialCare*x.wage for x in self.pop.livingPeople if x.outOfWorkSocialCare > 0])
        
        # By income quintiles
        households = [x for x in self.map.occupiedHouses]
        q1_households = [x for x in households if x.incomeQuintile == 0]
        q1_socialCareNeed = sum([x.totalSocialCareNeed for x in q1_households])
        q2_households = [x for x in households if x.incomeQuintile == 1]
        q2_socialCareNeed = sum([x.totalSocialCareNeed for x in q2_households])
        q3_households = [x for x in households if x.incomeQuintile == 2]
        q3_socialCareNeed = sum([x.totalSocialCareNeed for x in q3_households])
        q4_households = [x for x in households if x.incomeQuintile == 3]
        q4_socialCareNeed = sum([x.totalSocialCareNeed for x in q4_households])
        q5_households = [x for x in households if x.incomeQuintile == 4]
        q5_socialCareNeed = sum([x.totalSocialCareNeed for x in q5_households])
        
        q1_informalSocialCare = sum([x.informalSocialCareReceived for x in q1_households])
        q2_informalSocialCare = sum([x.informalSocialCareReceived for x in q2_households])
        q3_informalSocialCare = sum([x.informalSocialCareReceived for x in q3_households])
        q4_informalSocialCare = sum([x.informalSocialCareReceived for x in q4_households])
        q5_informalSocialCare = sum([x.informalSocialCareReceived for x in q5_households])
        
        q1_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q1_households])
        q2_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q2_households])
        q3_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q3_households])
        q4_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q4_households])
        q5_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q5_households])
        
        q1_formalSocialCare = sum([x.formalSocialCareReceived for x in q1_households])
        q2_formalSocialCare = sum([x.formalSocialCareReceived for x in q2_households])
        q3_formalSocialCare = sum([x.formalSocialCareReceived for x in q3_households])
        q4_formalSocialCare = sum([x.formalSocialCareReceived for x in q4_households])
        q5_formalSocialCare = sum([x.formalSocialCareReceived for x in q5_households])
        
        q1_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q1_households])
        q2_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q2_households])
        q3_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q3_households])
        q4_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q4_households])
        q5_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q5_households])
        
        taxPayers = len([x for x in self.pop.livingPeople if x.status == 'student' or x.status == 'worker'])
        self.numTaxpayers.append(taxPayers)
        
        if totalSocialCareNeed == 0:
            familyCareRatio = 0.0
        else:
            familyCareRatio = (totalSocialCareNeed - totalUnmetSocialCareNeed)/totalSocialCareNeed

        ##familyCareRatio = ( totalCareDemandHours - unmetNeed ) / (1.0 * (totalCareDemandHours+0.01))
        self.totalFamilyCare.append(familyCareRatio)

        taxBurden = ( totalUnmetSocialCareNeed * self.p['hourlyCostOfCare'] * 52.18 ) / ( taxPayers * 1.0 )
        self.totalTaxBurden.append(taxBurden)
        
        ## Count the proportion of adult women who are married
        totalAdultWomen = 0
        totalMarriedAdultWomen = 0

        for person in self.pop.livingPeople:
            age = self.year - person.birthdate
            if person.sex == 'female' and age >= 18:
                totalAdultWomen += 1
                if person.partner != None:
                    totalMarriedAdultWomen += 1
        marriagePropNow = float(totalMarriedAdultWomen) / float(totalAdultWomen)
        self.marriageProp.append(marriagePropNow)

        formalChildCare = sum([x.formalChildCareReceived for x in self.pop.livingPeople])
        formalChildCareCost = formalChildCare*self.p['priceChildCare']
        householdsIncome = sum([x.householdIncome for x in self.map.occupiedHouses])
        childcareIncomeShare = 0
        if householdsIncome > 0:
            childcareIncomeShare = formalChildCareCost/householdsIncome
      
        children = [x for x in self.pop.livingPeople if x.age < self.p['ageTeenagers']]
        totalChildCareNeed = sum([x.netChildCareDemand for x in children])
        unmetChildCareNeed = sum([x.unmetChildCareNeed for x in children])
        
#        print 'Total child care need: ' + str(totalChildCareNeed)
#        print 'Unmet child care need: ' + str(unmetChildCareNeed)
        
        totalInformalChildCare = sum([x.informalChildCareReceived for x in children])
        shareInformalChildCare = 0
        if totalChildCareNeed > 0:
            shareInformalChildCare = totalInformalChildCare/totalChildCareNeed
       
        # Social care stats
        over16Pop = [x for x in self.pop.livingPeople if x.age > 16]
        
        totalSuppliers = [x for x in over16Pop if x.socialWork > 0]
        
        shareCareGivers = float(len(totalSuppliers))/float(len(over16Pop))
        familyCarers = [x for x in over16Pop if x.careForFamily == True]
        
        
        malesOver16 = [x for x in over16Pop if x.sex == 'male']
        femalesOver16 = [x for x in over16Pop if x.sex == 'female']
        maleSuppliers = [x for x in malesOver16 if x.socialWork > 0]
        femaleSuppliers = [x for x in femalesOver16 if x.socialWork > 0]
        ratioFemaleMaleCarers = 0
        if len(totalSuppliers) > 0:
            ratioFemaleMaleCarers = float(len(femaleSuppliers))/float(len(totalSuppliers))
        shareMaleCarers = 0
        if len(malesOver16) > 0:
            shareMaleCarers = float(len(maleSuppliers))/float(len(malesOver16))
        shareFemaleCarers = 0
        if len(femalesOver16) > 0:
            shareFemaleCarers = float(len(femaleSuppliers))/float(len(femalesOver16))
        
        workers = [x for x in self.pop.livingPeople if x.status == 'worker' and x.careNeedLevel < 3]
        employedMales = [x for x in workers if x.sex == 'male']
        employedFemales = [x for x in workers if x.sex == 'female']
        
        meanMaleWage = np.mean([x.wage for x in employedMales])
        meanFemaleWage = np.mean([x.wage for x in employedFemales])
        ratioWage = 0
        if meanMaleWage > 0:
            ratioWage = meanFemaleWage/meanMaleWage
        
        meanMaleIncome = np.mean([x.income for x in employedMales])
        meanFemaleIncome = np.mean([x.income for x in employedFemales])
        ratioIncome = 0
        if meanMaleIncome > 0:
            ratioIncome = meanFemaleIncome/meanMaleIncome
        
        informalSocialCarers = [x for x in self.pop.livingPeople if x.socialWork > 0]
        informalSocialReceivers = [x for x in self.pop.livingPeople if x.informalSocialCareReceived > 0]
        informalCaresSupplied = [x.socialWork for x in informalSocialCarers]
        shareFamilyCarer = 0
        if len(informalSocialCarers) > 0:
            shareFamilyCarer = float(len(familyCarers))/float(len(informalSocialCarers))
        
        over20Hours_FamilyCarers = [x for x in familyCarers if x.socialWork > 20]
        share_over20Hours_FamilyCarers = 0
        if len(familyCarers) > 0:
            share_over20Hours_FamilyCarers = float(len(over20Hours_FamilyCarers))/float(len(familyCarers))
        averageHoursOfCare = np.mean(informalCaresSupplied)
        carers_40to64 = [x for x in informalSocialCarers if x.age >= 40 and x.age <= 64]
        over65_carers = [x for x in informalSocialCarers if x.age >= 65]
        share_40to64_carers = 0
        if len(informalSocialCarers) > 0:
            share_40to64_carers = float(len(carers_40to64))/float(len(informalSocialCarers))
        share_over65_carers = 0
        if len(informalSocialCarers) > 0:
            share_over65_carers = float(len(over65_carers))/float(len(informalSocialCarers))
            
        over70_carers = [x for x in informalSocialCarers if x.age >= 70]  
        TenPlusHours_over70 = [x for x in over70_carers if x.age >= 70 if x.socialWork > 10]
        share_10PlusHours_over70 = 0
        if len(over70_carers) > 0:
            share_10PlusHours_over70 = float(len(TenPlusHours_over70))/float(len(over70_carers))
        
        self.costTaxFreeSocialCare = totalFormalSocialCare*self.p['priceSocialCare']*self.p['socialCareTaxFreeRate']
        
        publicCareToGDP = self.costPublicSocialCare/self.grossDomesticProduct
        
        realPop = sum(self.popData[self.popData.year == self.year]['total'])
        normalizedPop = 1000*realPop/self.initialPop
        
        
        outputs = [self.year, currentPop, normalizedPop, everLivedPop, self.deaths, self.shareDeaths, self.births, self.shareBirths,
                   numHouseholds, averageHouseholdSize, self.marriageTally, marriagePropNow, self.divorceTally, shareSingleParents, 
                   shareFemaleSingleParent, taxPayers, taxBurden, familyCareRatio, shareEmployed, shareWorkHours, 
                   self.publicSocialCare, self.costPublicSocialCare, self.sharePublicSocialCare, self.publicCareExpenses,
                   self.costTaxFreeSocialCare, self.publicChildCare, self.costPublicChildCare, self.sharePublicChildCare, 
                   self.costTaxFreeChildCare, self.totalTaxRevenue, self.totalPensionRevenue, self.pensionExpenditure, 
                   self.totalHospitalizationCost, self.socialClassShares[0], self.socialClassShares[1], self.socialClassShares[2], 
                   self.socialClassShares[3], self.socialClassShares[4], totalInformalChildCare, formalChildCare, childcareIncomeShare, 
                   shareInformalChildCare, shareCareGivers, ratioFemaleMaleCarers, shareMaleCarers, shareFemaleCarers, ratioWage, 
                   ratioIncome, shareFamilyCarer, share_over20Hours_FamilyCarers, averageHoursOfCare, share_40to64_carers, 
                   share_over65_carers, share_10PlusHours_over70, totalSocialCareNeed, totalInformalSocialCare, totalFormalSocialCare, 
                   totalUnmetSocialCareNeed, totalSocialCare, share_InformalSocialCare, share_UnmetSocialCareNeed, 
                   totalOWSC, shareOWSC, totalCostOWSC,
                   q1_socialCareNeed, q1_informalSocialCare, q1_formalSocialCare, q1_unmetSocialCareNeed, q1_outOfWorkSocialCare,
                   q2_socialCareNeed, q2_informalSocialCare, q2_formalSocialCare, q2_unmetSocialCareNeed, q2_outOfWorkSocialCare,
                   q3_socialCareNeed, q3_informalSocialCare, q3_formalSocialCare, q3_unmetSocialCareNeed, q3_outOfWorkSocialCare,
                   q4_socialCareNeed, q4_informalSocialCare, q4_formalSocialCare, q4_unmetSocialCareNeed, q4_outOfWorkSocialCare,
                   q5_socialCareNeed, q5_informalSocialCare, q5_formalSocialCare, q5_unmetSocialCareNeed, q5_outOfWorkSocialCare,
                   self.grossDomesticProduct, publicCareToGDP, self.popEdinburgh, self.share_fromEdinburgh, self.share_toEdinburgh,
                   self.popGlasgow, self.share_fromGlasgow, self.share_toGlasgow, self.popAberdeen, self.share_fromAberdeen, 
                   self.share_toAberdeen]
        
        
        dataMapFile = 'DataMap_' + str(self.year) + '.csv'
        if not os.path.exists(dataMapFolder):
            os.makedirs(dataMapFolder)
        with open(os.path.join(dataMapFolder, dataMapFile), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataMap))
            for house in self.map.allHouses:
                data = [house.town.name, house.town.x, house.town.y, house.x, house.y, len(house.occupants), house.totalUnmetSocialCareNeed]
                writer.writerow(data)
                
        householdFile = 'DataHousehold_' + str(self.year) + '.csv'
        if not os.path.exists(dataHouseholdFolder):
            os.makedirs(dataHouseholdFolder)
        with open(os.path.join(dataHouseholdFolder, householdFile), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.householdData))
            for member in self.displayHouse.occupants:
                data = [member.id, member.sex, member.age, member.careNeedLevel]
                writer.writerow(data)    
        
        houseData = [self.year, self.displayHouse.name, len(self.displayHouse.occupants)]
        with open(os.path.join(policyFolder, "HouseData.csv"), "a") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow(houseData)
        
        malesByNeed = []
        for i in range(int(self.p['numCareLevels'])):
            malesByAge = []
            for j in range(25):
                subgroup = [x for x in self.pop.livingPeople if x.sex == 'male' and int(x.age/5) == j and x.careNeedLevel == i]
                malesByAge.append(len(subgroup))
            malesByNeed.append(malesByAge)
            
        femalesByNeed = []
        for i in range(int(self.p['numCareLevels'])):
            femalesByAge = []
            for j in range(25):
                subgroup = [x for x in self.pop.livingPeople if x.sex == 'female' and int(x.age/5) == j and x.careNeedLevel == i]
                femalesByAge.append(len(subgroup))
            femalesByNeed.append(femalesByAge)
        
        for i in range(int(self.p['numCareLevels'])):
            pyramidData = [self.year]
            pyramidData.extend(malesByNeed[i])
            fileName = 'Pyramid_Male_' + str(i) + '.csv'
            with open(os.path.join(policyFolder, fileName), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(pyramidData)
            
        for i in range(int(self.p['numCareLevels'])):
            pyramidData = [self.year]
            pyramidData.extend(femalesByNeed[i])
            fileName = 'Pyramid_Female_' + str(i) + '.csv'
            with open(os.path.join(policyFolder, fileName), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(pyramidData)
            
        houseData = [self.year, self.displayHouse.name, len(self.displayHouse.occupants)]
        with open(os.path.join(policyFolder, "HouseData.csv"), "a") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow(houseData)
            
        if self.year == self.p['startYear']:
            if not os.path.exists(policyFolder):
                os.makedirs(policyFolder)
            with open(os.path.join(policyFolder, "Outputs.csv"), "w") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow((self.Outputs))
                writer.writerow(outputs)
        else:
            with open(os.path.join(policyFolder, "Outputs.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(outputs)
        
        self.marriageTally = 0
        self.divorceTally = 0
        
        ## Some extra debugging stuff just to check that all
        ## the lists are behaving themselves
        if self.p['verboseDebugging']:
            peopleCount = 0
            for i in self.pop.allPeople:
                if i.dead == False:
                    peopleCount += 1
            print "True pop counting non-dead people in allPeople list = ", peopleCount

            peopleCount = 0
            for h in self.map.occupiedHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of all occupied houses = ", peopleCount

            peopleCount = 0
            for h in self.map.allHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of ALL houses = ", peopleCount

            tally = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for h in self.map.occupiedHouses:
                tally[len(h.occupants)] += 1
            for i in range(len(tally)):
                if tally[i] > 0:
                    print i, tally[i]
            print

            
    def healthCareCost(self):

        peopleWithUnmetNeed = [x for x in self.pop.livingPeople if x.careNeedLevel > 0]
        self.totalHospitalizationCost = 0
        for person in peopleWithUnmetNeed:
            needLevelFactor = math.pow(self.p['needLevelParam'], person.careNeedLevel)
            unmetSocialCareFactor = math.pow(self.p['unmetSocialCareParam'], person.averageShareUnmetNeed)
            averageHospitalization = self.p['hospitalizationParam']*needLevelFactor*unmetSocialCareFactor
            self.totalHospitalizationCost += averageHospitalization*self.p['costHospitalizationPerDay']
        self.hospitalizationCost.append(self.totalHospitalizationCost)
        
    def initializeCanvas(self):
        """Put up a TKInter canvas window to animate the simulation."""
        self.canvas.pack()

        ## Draw some numbers for the population pyramid that won't be redrawn each time
        for a in range(0,int(self.p['num5YearAgeClasses'])):
            self.canvas.create_text(170, 385 - (10 * a),
                                    text=str(5*a) + '-' + str(5*a+4),
                                    font='Helvetica 6',
                                    fill='white')

        ## Draw the overall map, including towns and houses (occupied houses only)
        for t in self.map.towns:
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            self.canvas.create_rectangle(xBasic, yBasic,
                                         xBasic+self.p['pixelsPerTown'],
                                         yBasic+self.p['pixelsPerTown'],
                                         outline='grey',
                                         state = 'hidden' )

        for h in self.map.allHouses:
            t = h.town
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            xOffset = xBasic + 2 + (h.x * 2)
            yOffset = yBasic + 2 + (h.y * 2)

            outlineColour = fillColour = self.p['houseSizeColour'][h.size]
            width = 1

            h.icon = self.canvas.create_rectangle(xOffset,yOffset,
                                                  xOffset + width, yOffset + width,
                                                  outline=outlineColour,
                                                  fill=fillColour,
                                                  state = 'normal' )

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.update()

        for h in self.map.allHouses:
            self.canvas.itemconfig(h.icon, state='hidden')

        for h in self.map.occupiedHouses:
            self.canvas.itemconfig(h.icon, state='normal')

        self.canvas.update()
        self.updateCanvas()

    def updateCanvas(self):
        """Update the appearance of the graphics canvas."""

        ## First we clean the canvas off; some items are redrawn every time and others are not
        self.canvas.delete('redraw')

        ## Now post the current year and the current population size
        self.canvas.create_text(self.p['dateX'],
                                self.p['dateY'],
                                text='Year: ' + str(self.year),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')
        self.canvas.create_text(self.p['popX'],
                                self.p['popY'],
                                text='Pop: ' + str(len(self.pop.livingPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        self.canvas.create_text(self.p['popX'],
                                self.p['popY'] + 30,
                                text='Ever: ' + str(len(self.pop.allPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        ## Also some other stats, but not on the first display
        if self.year > self.p['startYear']:
            self.canvas.create_text(350,20,
                                    text='Avg household: ' + str ( round ( self.avgHouseholdSize[-1] , 2 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,40,
                                    text='Marriages: ' + str(self.numMarriages[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,60,
                                    text='Divorces: ' + str(self.numDivorces[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,100,
                                    text='Total care demand: ' + str(round(self.totalCareDemand[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,120,
                                    text='Num taxpayers: ' + str(round(self.numTaxpayers[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,140,
                                    text='Family care ratio: ' + str(round(100.0 * self.totalFamilyCare[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,160,
                                    text='Tax burden: ' + str(round(self.totalTaxBurden[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,180,
                                    text='Marriage prop: ' + str(round(100.0 * self.marriageProp[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = self.p['fontColour'],
                                    tags = 'redraw')

        

        ## Draw the population pyramid split by care categories
        for a in range(0,int(self.p['num5YearAgeClasses'])):
            malePixel = 153
            femalePixel = 187
            for c in range(0,self.p['numCareLevels']):
                mWidth = self.pyramid.maleData[a,c]
                fWidth = self.pyramid.femaleData[a,c]

                if mWidth > 0:
                    self.canvas.create_rectangle(malePixel, 380 - (10*a),
                                                 malePixel - mWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                malePixel -= mWidth
                
                if fWidth > 0:
                    self.canvas.create_rectangle(femalePixel, 380 - (10*a),
                                                 femalePixel + fWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                femalePixel += fWidth

        ## Draw in the display house and the people who live in it
        if len(self.displayHouse.occupants) < 1:
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
            

        outlineColour = self.p['houseSizeColour'][self.displayHouse.size]
        self.canvas.create_rectangle( 50, 450, 300, 650,
                                      outline = outlineColour,
                                      tags = 'redraw' )
        self.canvas.create_text ( 60, 660,
                                  text="Display house " + self.displayHouse.name,
                                  font='Helvetica 10',
                                  fill='white',
                                  anchor='nw',
                                  tags='redraw')
                                  

        ageBracketCounter = [ 0, 0, 0, 0, 0 ]

        for i in self.displayHouse.occupants:
            age = self.year - i.birthdate
            ageBracket = age / 20
            if ageBracket > 4:
                ageBracket = 4
            careClass = i.careNeedLevel
            sex = i.sex
            idNumber = i.id
            self.drawPerson(age,ageBracket,ageBracketCounter[ageBracket],careClass,sex,idNumber)
            ageBracketCounter[ageBracket] += 1


        ## Draw in some text status updates on the right side of the map
        ## These need to scroll up the screen as time passes

        if len(self.textUpdateList) > self.p['maxTextUpdateList']:
            excess = len(self.textUpdateList) - self.p['maxTextUpdateList']
            self.textUpdateList = self.textUpdateList[excess:excess+self.p['maxTextUpdateList']]

        baseX = 1035
        baseY = 30
        for i in self.textUpdateList:
            self.canvas.create_text(baseX,baseY,
                                    text=i,
                                    anchor='nw',
                                    font='Helvetica 9',
                                    fill = 'white',
                                    width = 265,
                                    tags = 'redraw')
            baseY += 30

        ## Finish by updating the canvas and sleeping briefly in order to allow people to see it
        self.canvas.update()
        if self.p['delayTime'] > 0.0:
            time.sleep(self.p['delayTime'])


    def drawPerson(self, age, ageBracket, counter, careClass, sex, idNumber):
        baseX = 70 + ( counter * 30 )
        baseY = 620 - ( ageBracket * 30 )

        fillColour = self.p['careLevelColour'][careClass]

        self.canvas.create_oval(baseX,baseY,baseX+6,baseY+6,
                                fill=fillColour,
                                outline=fillColour,tags='redraw')
        if sex == 'male':
            self.canvas.create_rectangle(baseX-2,baseY+6,baseX+8,baseY+12,
                                fill=fillColour,outline=fillColour,tags='redraw')
        else:
            self.canvas.create_polygon(baseX+2,baseY+6,baseX-2,baseY+12,baseX+8,baseY+12,baseX+4,baseY+6,
                                fill=fillColour,outline=fillColour,tags='redraw')
        self.canvas.create_rectangle(baseX+1,baseY+13,baseX+5,baseY+20,
                                     fill=fillColour,outline=fillColour,tags='redraw')
            
            
            
        self.canvas.create_text(baseX+11,baseY,
                                text=str(age),
                                font='Helvetica 6',
                                fill='white',
                                anchor='nw',
                                tags='redraw')
        self.canvas.create_text(baseX+11,baseY+8,
                                text=str(idNumber),
                                font='Helvetica 6',
                                fill='grey',
                                anchor='nw',
                                tags='redraw')


    def doGraphs(self):
        """Plot the graphs needed at the end of one run."""
        
        

        p1, = pylab.plot(self.times,self.pops,color="red")
        p2, = pylab.plot(self.times,self.numTaxpayers,color="blue")
        pylab.legend([p1, p2], ['Total population', 'Taxpayers'],loc='lower right')
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Number of people')
        pylab.xlabel('Year')
        pylab.savefig('popGrowth.pdf')
        pylab.show()
        pylab.close()

        pylab.plot(self.times,self.avgHouseholdSize,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Average household size')
        pylab.xlabel('Year')
        pylab.savefig('avgHousehold.pdf')
        pylab.show()
        pylab.close()

        p1, = pylab.plot(self.times,self.totalCareDemand,color="red")
        p2, = pylab.plot(self.times,self.totalCareSupply,color="blue")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.legend([p1, p2], ['Care demand', 'Total theoretical supply'],loc='lower right')
        pylab.ylabel('Total hours per week')
        pylab.xlabel('Year')
        pylab.savefig('totalCareSituation.pdf')
        pylab.show()

        pylab.plot(self.times,self.totalFamilyCare,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of informal social care')
        pylab.xlabel('Year')
        pylab.savefig('informalCare.pdf')
        pylab.show()

        pylab.plot(self.times,self.totalTaxBurden,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Care costs in pounds per taxpayer per year')
        pylab.xlabel('Year')
        pylab.savefig('taxBurden.pdf')
        pylab.show()

        pylab.plot(self.times,self.marriageProp,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of married adult women')
        pylab.xlabel('Year')
        pylab.savefig('marriageProp.pdf')
        pylab.savefig('marriageProp.png')
        pylab.show()
        
        pylab.plot(self.times,self.shareLoneParents,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Share of Lone Parents')
        pylab.xlabel('Year')
        pylab.savefig('shareLoneParents.pdf')
        pylab.savefig('shareLoneParents.png')
        pylab.show()
        
        pylab.plot(self.times, self.shareUnmetNeed, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Share of Unmet Care Need')
        pylab.xlabel('Year')
        pylab.savefig('shareUnmetCareNeed.pdf')
        pylab.savefig('shareUnmetCareNeed.png')
        pylab.show()
        
        pylab.plot(self.times, self.hospitalizationCost, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Hospitalisation Cost')
        pylab.xlabel('Year')
        pylab.savefig('hospitalisationCost.pdf')
        pylab.savefig('hospitalisationCost.png')
        pylab.show()
        
        pylab.plot(self.times, self.employmentRate, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Employment Rate')
        pylab.xlabel('Year')
        pylab.savefig('employmentRate.pdf')
        pylab.savefig('employmentRate.png')
        pylab.show()
        
        pylab.plot(self.times, self.publicCareProvision, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Public Care Provision')
        pylab.xlabel('Year')
        pylab.savefig('publicCareProvision.pdf')
        pylab.savefig('publicCareProvision.png')
        pylab.show()
        
        y_pos = np.arange(len(self.sesPopsShares))
        plt.bar(y_pos, self.sesPopsShares)
        plt.ylabel('SES Populations')
        plt.show()
        
        lenFrequency = len(self.incomeDistribution)
        individualIncomeFrequencies = [0]*lenFrequency

        dK = np.random.normal(0, self.p['wageVar'])
        indDist = np.random.choice(self.incomesPercentiles, len(self.individualIncomes))*math.exp(dK)
        for i in indDist:
            ind = int(i/1000)
            if ind > -1 and ind < lenFrequency:
                individualIncomeFrequencies[ind] += 1
                
        y_pos = np.arange(lenFrequency)
        plt.bar(y_pos, individualIncomeFrequencies)
        plt.ylabel('individual frequency (empirical)')
        plt.show()
        
        lenFrequency = len(self.incomeDistribution)
        individualIncomeFrequencies = [0]*lenFrequency
        for i in self.individualIncomes:
            ind = int(i/1000)
            if ind > -1 and ind < lenFrequency:
                individualIncomeFrequencies[ind] += 1
                
        y_pos = np.arange(lenFrequency)
        plt.bar(y_pos, individualIncomeFrequencies)
        plt.ylabel('individual frequency (simulated)')
        plt.show()
        
        df = pd.DataFrame()
        df[0] = self.individualIncomes
        df[1] = indDist
        fig, ax = plt.subplots(1,1)
        for s in df.columns:
            df[s].plot(kind='density')
        fig.show()
    

class PopPyramid:
    """Builds a data object for storing population pyramid data in."""
    def __init__ (self, ageClasses, careLevels):
        self.maleData = pylab.zeros((int(ageClasses), int(careLevels)),dtype=int)
        self.femaleData = pylab.zeros((int(ageClasses), int(careLevels)),dtype=int)

    def update(self, year, ageClasses, careLevels, pixelFactor, people):
        ## zero the two arrays
        for a in range (int(ageClasses)):
            for c in range (int(careLevels)):
                self.maleData[a,c] = 0
                self.femaleData[a,c] = 0
        ## tally up who belongs in which category
        for i in people:
            ageClass = ( year - i.birthdate ) / 5
            if ageClass > ageClasses - 1:
                ageClass = ageClasses - 1
            careClass = i.careNeedLevel
            if i.sex == 'male':
                self.maleData[int(ageClass), int(careClass)] += 1
            else:
                self.femaleData[int(ageClass), int(careClass)] += 1

        ## normalize the totals into pixels
        total = len(people)        
        for a in range (int(ageClasses)):
            for c in range (int(careLevels)):
                self.maleData[a,c] = pixelFactor * self.maleData[a,c] / total
                self.femaleData[a,c] = pixelFactor * self.femaleData[a,c] / total
