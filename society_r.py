# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:40:07 2017

@author: ug4d
"""
import random
import numpy as np
import math
import networkx as nx

class Population:
    """The population class stores a collection of persons."""
    def __init__ (self, initialPop, startYear, minStartAge, maxStartAge,
                  nc, soc, edu, ics, iu, up, wa, il, fl, gr, wdt, wv):
        self.allPeople = []
        self.livingPeople = []
        
        ranks = []
        for n in range(nc):
            ranks.extend([n]*(int)(ics[n]*(initialPop/2)))
        
        for i in range(initialPop/2):
            
            ageMale = random.randint(minStartAge, maxStartAge)
            ageFemale = ageMale - random.randint(-2,5)
            if ( ageFemale < 24 ):
                ageFemale = 24
            mab = self.ageBand(ageMale)
            fab = self.ageBand(ageFemale)
            maleBirthYear = startYear - ageMale
            femaleBirthYear = startYear - ageFemale
            classes = [0, 1, 2, 3, 4]
            probClasses = [0.2, 0.35, 0.25, 0.15, 0.05]
            classRank = np.random.choice(classes, p = probClasses)
            um = self.unemploymentRate(mab, classRank, iu, up)
            uf = self.unemploymentRate(fab, classRank, iu, up)
            socialClass = soc[classRank]
            eduLevel = edu[classRank]
            
            workingTimeMale = 0
            for i in range(int(ageMale-wa[classRank])):
                workingTimeMale *= wdt
                workingTimeMale += 1
            workingTimeFemale = 0
            for i in range(int(ageFemale-wa[classRank])):
                workingTimeFemale *= wdt
                workingTimeFemale += 1
            dK = np.random.normal(0, wv)
            newK = fl[classRank]*math.exp(dK)    
            c = np.math.log(il[classRank]/newK)
            maleWage = newK*np.math.exp(c*np.math.exp(-1*gr[classRank]*workingTimeMale))
            femaleWage = newK*np.math.exp(c*np.math.exp(-1*gr[classRank]*workingTimeFemale))
            maleIncome = maleWage*40.0
            femaleIncome = femaleWage*40.0
            manStatus = 'employed'
            finalIncome = fl[classRank]
            if random.random() < um :
                manStatus = 'unemployed'
                maleIncome = 0
                finalIncome = 0
            yearsInTown = random.randint(0, 10)
            tenure = 1.0
            newMan = Person(None, None, ageMale, maleBirthYear, 'male', manStatus, 
                            None, classRank, socialClass, eduLevel, maleWage, 
                            maleIncome, 0, finalIncome, workingTimeMale, yearsInTown, tenure, 0.02)
            status = 'employed'
            finalIncome = fl[classRank]
            if random.random() < uf and manStatus == 'employed':
                status = 'unemployed'
                femaleIncome = 0
                finalIncome = 0
            yearsInTown = random.randint(0, 10)
            newWoman = Person(None, None, ageFemale, femaleBirthYear, 'female', 
                              status, None, classRank, socialClass, eduLevel, 
                              femaleWage, femaleIncome, 0, finalIncome, workingTimeFemale, yearsInTown, tenure, 0.02)
            
            newMan.independentStatus = True
            newWoman.independentStatus = True

            newMan.partner = newWoman
            newWoman.partner = newMan

            self.allPeople.append(newMan)
            self.livingPeople.append(newMan)
            self.allPeople.append(newWoman)
            self.livingPeople.append(newWoman)

    def ageBand(self, age):
        if age <= 19:
            band = 0
        elif age >= 20 and age <= 24:
            band = 1
        elif age >= 25 and age <= 34:
            band = 2
        elif age >= 35 and age <= 44:
            band = 3
        elif age >= 45 and age <= 54:
            band = 4
        else: 
            band = 5
        return (band)
    
    def unemploymentRate(self, i, j, iu, up):
        classFactor = iu[j]
        ageFactor = math.pow(up, i)
        unemploymentRate = classFactor*ageFactor
        return (unemploymentRate)

class Person:
    """The person class stores information about a person in the sim."""
    counter = 1

    def __init__(self, mother, father, age, birthYear, sex, status, house,
                 classRank, sec, edu, wage, income, wlt, finalIncome, workingTime, yit, tenure, ur):
        
#        random.seed(rs)
#        np.random.seed(rs)
        
        self.mother = mother
        self.father = father
        self.children = []
        self.household = []
        self.age = age
        self.yearAfterPolicy = 0
        self.birthdate = birthYear
        self.visitedCarer = False
        self.careNeedLevel = 0
        self.hoursDemand = 0
        self.residualNeed = 0
        
        self.motherID = -1 # For pickle
        self.fatherID = -1 # For pickle
        self.childrenID = [] # For pickle
        self.houseID = -1 # For pickle
        
        self.hoursSocialCareDemand = 0
        self.residualSocialCareNeed = 0
        self.hoursChildCareDemand = 0
        self.residualChildCareNeed = 0
        
        self.netHouseholdCare = 0
        self.householdName = 0
        self.netIndividualCare = 0
        
       
        self.hoursSupply = 0
        
        
        self.socialWork = 0
        self.workToCare = 0
        
        self.socialCareCredits = 0
        self.volunteerCareSupply = 0
        self.creditNeedRatio = 0
        self.maxNokSupply = 0
        self.residualNetNeed = 0
        self.potentialVolunteer = False
        
        self.cumulativeUnmetNeed = 0
        self.totalDiscountedShareUnmetNeed = 0
        self.totalDiscountedTime = 0
        self.averageShareUnmetNeed = 0
        self.informalSupplyByKinship = []
        self.formalSupplyByKinship = []
        self.networkSupply = 0
        
        self.maxInformalSupply = 0
        self.residualInformalSupply = [0.0, 0.0, 0.0, 0.0]
        self.hoursInformalSupply = [0.0, 0.0, 0.0, 0.0]
        self.extraworkCare = [0.0, 0.0, 0.0, 0.0]
        self.residualFormalSupply = [0.0, 0.0, 0.0, 0.0]
        self.hoursFormalSupply = [0.0, 0.0, 0.0, 0.0]
        self.residualIncomeCare = 0
        self.offWorkCare = 0
        
        self.hoursCareSupply = 0
        self.mortalityRate = 0
        self.fertilityRate = 0
        
        self.residualWorkingHours = 0
        self.incomeByTaxBands = []
        self.maxFormalCareSupply = 0
        self.qaly = 0
        self.residualSupply = 0
        self.formalCare = 0
        self.informalCare = 0
        self.careReceived = 0
        self.socialNetwork = []
        
        self.careNetwork = nx.Graph()
        self.numSuppliers = 0
        self.supplyNetwork = nx.Graph()
        
        self.householdSupply = 0
        
        self.householdTotalSupply = 0
        
        self.careReceivers = []
        self.totalCareSupplied = []
        
        self.totalSupply = 0
        
        self.totalInformalSupply = 0
        self.socialCareProvider = False
        self.babyCarer = False
        self.yearOfSchoolLeft = 0
        self.dead = False
        self.partner = None
        self.numberPartner = 0
        if sex == 'random':
            self.sex = random.choice(['male', 'female'])
        else:
            self.sex = sex
        if self.sex == 'female':
            self.sexIndex = 1
        else:
            self.sexIndex = 0
        self.house = house
        self.socialCareMap = []
        self.classRank = classRank
        self.temporaryClassRank = 0
        self.sec = sec
        self.education = edu
        self.ageStartWorking = -1
        self.yearMarried = -1
        self.yearsSeparated = 0
        self.wage = wage
        self.hourlyWage = wage
        self.income = income
        self.cumulativeIncome = 0
        self.wealth = wlt
        self.netIncome = income
        self.disposableIncome = income
        self.finalIncome = finalIncome
        self.jobOffers = []
        self.workingTime = workingTime
        self.status = status
        self.independentStatus = False
        self.elderlyWithFamily = False
        self.yearIndependent = 0
        self.jobLocation = None
        self.jobLocationID = -1
        self.searchJob = False
        self.jobChange = False
        self.newTown = None
        self.newK = 0
        self.newWage = 0
        self.unemploymentDuration = 0
        self.jobTenure = tenure
        self.yearsInTown = yit
        self.justMarried = None
        self.unemploymentRate = ur
        # Introducing care needs of babies
        if age < 1:
            self.careRequired = 80
        self.careAvailable = 0
        self.movedThisYear = False
        self.id = Person.counter
        Person.counter += 1
        

        
        
        
        
        