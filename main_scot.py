
from sim_scot import Sim
import os
import cProfile
import pylab
import math
import matplotlib.pyplot as plt
import random
import csv
import numpy as np
import pandas as pd
import itertools
from itertools import izip_longest
from collections import OrderedDict
import time
import datetime
import multiprocessing

def meta_params():
    
    m = OrderedDict() # For meta-parameters file
    
    m['numRepeats'] = 1
    m['initialPop'] = 2000
    m['startYear'] = 1855
    m['endYear'] = 2050
    m['mortalityDataFrom'] = 1855
    m['fertilityDataFrom'] = 1945
    m['migrationDataFrom'] = 1952
    m['migrationDataTo'] = 2019
    m['thePresent'] = 2012
    m['statsCollectFrom'] = 1960
    m['policyStartYear'] = 2020
    m['outputYear'] = 2015
    m['minStartAge'] = 20
    m['maxStartAge'] = 40
    m['verboseDebugging'] = False
    m['singleRunGraphs'] = False
    m['favouriteSeed'] = int(time.time())
    m['loadFromFile'] = False
    m['numberClasses'] = 5
    m['numCareLevels'] = 5
    m['timeDiscountingRate'] = 0.035
        ## Description of the map, towns, and houses
    m['mapGridXDimension'] = 20
    m['mapGridYDimension'] = 25    
    m['townGridDimension'] = 25
    m['shareClasses'] = [0.2, 0.35, 0.25, 0.15, 0.05]
    m['classAdjustmentBeta'] = 3.0

    ## Graphical interface details
    m['interactiveGraphics'] = False
    m['delayTime'] = 0.0
    m['screenWidth'] = 1300
    m['screenHeight'] = 700
    m['bgColour'] = 'black'
    m['mainFont'] = 'Helvetica 18'
    m['fontColour'] = 'white'
    m['dateX'] = 70
    m['dateY'] = 20
    m['popX'] = 70
    m['popY'] = 50
    m['pixelsInPopPyramid'] = 2000
    m['careLevelColour'] = ['blue','green','yellow','orange','red']
    m['houseSizeColour'] = ['blue','green','yellow','orange','red', 'lightgrey']
    m['pixelsPerTown'] = 56
    m['maxTextUpdateList'] = 22
    
    # multiprocessing params
    m['multiprocessing'] = False
    m['numberProcessors'] = 4
    
    
    folder = 'defaultSimFolder'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filePath = folder + '/metaParameters.csv'
    c = m.copy()
    for key, value in c.iteritems():
        if not isinstance(value, list):
            c[key] = [value]
    with open(filePath, "wb") as f:
        csv.writer(f).writerow(c.keys())
        csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
    return m
    
def init_params():
    """Set up the simulation parameters."""

    p = OrderedDict()
    
    # Public Finances Parameters
    p['taxBrackets'] = [663, 228, 0]
    p['taxationRates'] = [0.4, 0.2, 0.0]
    
    p['statePension'] = 164.35
    p['minContributionYears'] = 35
    p['employeePensionContribution'] = 0.04
    p['employerPensionContribution'] = 0.03
    p['statePensionContribution'] = 0.01
    p['pensionReturnRate'] = 0.05
    
    #### SES-version parameters   ######
    
    p['maleMortalityBias'] = 0.8   ### SES death bias
    p['femaleMortalityBias'] = 0.9
    p['careNeedBias'] = 0.9   ### Care Need Level death bias
    p['unmetCareNeedBias'] = 0.5  ### Unmet Care Need death bias
    
    p['fertilityBias'] = 0.9  ### Fertility bias
    
    ####  Income-related parameters
    p['workingAge'] = [16, 18, 20, 22, 24]
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0] # [0.64, 0.89, 1.27, 1.66, 2.29] #  
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0] #[0.64, 0.89, 1.15, 1.40, 1.78] #  
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0] #[1.27, 1.91, 2.80, 4.21, 6.37] #  
    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    p['wageVar'] = 0.1
    p['workDiscountingTime'] = 0.75
    p['weeklyHours'] = [40.0, 20.0, 0.0, 0.0, 0.0] 
    
    # Care transition params
    p['unmetNeedExponent'] = 1.0
    p['careBias'] = 0.9
    p['careTransitionRate'] = 0.7
    
    # Care params
    p['priceSocialCare'] = 17.0 
    p['priceChildCare'] = 6.0
    p['quantumCare'] = 4
    
    # Child Care params
    p['childCareDemand'] = 60 #48
    p['maxFormalChildCare'] = 48
    p['ageTeenagers'] = 12
    p['zeroYearCare'] = 84.0 
    
    # Public Child Care Provision Parameters
    # 1st policy parameter
    p['childCareTaxFreeRate'] = 0.2
    ###########################################
    p['maxPublicContribution'] = 2000.0
    p['childcareTaxFreeCap'] = int((p['maxPublicContribution']/52.0)/(p['priceChildCare']*p['childCareTaxFreeRate']))
    p['maxHouseholdIncomeChildCareSupport'] = 300.0
    p['freeChildCareHoursToddlers'] = 12
    
    # 2nd policy parameter
    p['freeChildCareHoursPreSchool'] = 20
    ##############################################
    p['freeChildCareHoursSchool'] = 32
    
    # Public Social Care Provision Parameters
    p['taxBreakRate'] = 0.0
    
    # 4th policy parameter
    p['socialCareTaxFreeRate'] = 0.0
    ##########################################
    # 3rd policy parameter
    p['publicCareNeedLevel'] = 1 # 5
    #############################################
    
    p['publicCareAgeLimit'] = 65 # 1000
    p['minWealthMeansTest'] = 17000.0
    p['maxWealthMeansTest'] = 27250.0
    p['careHomeFees'] = 750.0
    p['maxAccomodationSupport'] = 630.0
    p['freePersonalCare'] = 249.0
    p['wealthToPoundReduction'] = 250.0
    p['contributionForCareRatio'] = 0.5
    p['partialContributionRate'] = 0.5
    p['minimumIncomeGuarantee'] = 189.0
    
    p['distanceExp'] = 0.5
    p['networkExp'] = 0.4
    
    p['incomeCareParam'] = 0.0004 # 0.00005
    p['wealthCareParam'] = 0.000001 # 0.00000005
    
    p['betaInformalCare'] = 1.1
    
    p['betaFormalCare'] = 1.0
    p['shareFinancialWealth'] = 0.3
    p['formalCareDiscountFactor'] = 0.5
    
    # Social Transition params
    p['educationCosts'] = [0.0, 100.0, 150.0, 200.0] #[0.0, 12.74, 19.12, 25.49] # 
    p['eduWageSensitivity'] = 0.4 # 0.2
    p['eduRankSensitivity'] = 4.0 # 3.0
    p['costantIncomeParam'] = 20.0 # 20.0
    p['costantEduParam'] = 4.0 #  5.0
    p['careEducationParam'] = 0.5 # 0.4
    # Alternative Social Transition function
    p['incomeBeta'] = 0.01
    p['careBeta'] = 0.01
    
    p['pandemic'] = False
    p['lockdown'] = False
    p['alternation'] = 0
    p['virusYears'] = [2020, 2022, 2024]
    
    p['networkDistanceDiscount'] = 0.5
    p['retiredMaxSupply'] = 64
    p['employedMaxSupply'] = 24
    p['studentMaxSupply'] = 24
    p['teenagerMaxSupply'] = 16
        
#    p['retiredSupply'] = [64.0, 32.0, 16.0, 8.0] # [56.0, 28.0, 16.0, 8.0]
#    p['employedSupply'] = [24.0, 16.0, 8.0, 4.0] # [16.0, 12.0, 8.0, 4.0]
#    p['studentSupply'] = [24.0, 12.0, 4.0, 0.0] # [16.0, 8.0, 4.0, 0.0]
#    p['teenagerSupply'] = [16.0, 0.0, 0.0, 0.0] # [12.0, 0.0, 0.0, 0.0]
    
    # Marriages params
    p['incomeMarriageParam'] = 0.025
    p['betaGeoExp'] = 2.0
    p['studentFactorParam'] = 0.5
    p['betaSocExp'] = 2.0
    p['rankGenderBias'] = 0.5
    p['deltageProb'] =  [0.0, 0.1, 0.25, 0.4, 0.2, 0.05]
    p['bridesChildrenExp'] = 0.5
    p['manWithChildrenBias'] = 0.7
    p['maleMarriageMultiplier'] = 1.4

    # Unmer Need params
    p['unmetCareNeedDiscountParam'] = 0.5
    p['shareUnmetNeedDiscountParam'] = 0.5
    
    # Hospitalisation costs params
    p['hospitalizationParam'] = 0.5
    p['needLevelParam'] = 2.0
    p['unmetSocialCareParam'] = 2.0
    p['costHospitalizationPerDay'] = 400
    
    # Priced growth  #####
    p['wageGrowthRate'] = 1.0 # 1.01338 # 

    ## Mortality statistics
    p['baseDieProb'] = 0.0001
    p['babyDieProb'] = 0.005
    p['maleAgeScaling'] = 14.0
    p['maleAgeDieProb'] = 0.00021
    p['femaleAgeScaling'] = 15.5
    p['femaleAgeDieProb'] = 0.00019
    p['num5YearAgeClasses'] = 28

    ## Transitions to care statistics
    p['baseCareProb'] = 0.0002
    p['personCareProb'] = 0.0008
    ##p['maleAgeCareProb'] = 0.0008
    p['maleAgeCareScaling'] = 18.0
    ##p['femaleAgeCareProb'] = 0.0008
    p['femaleAgeCareScaling'] = 19.0
    p['cdfCareTransition'] = [ 0.7, 0.9, 0.95, 1.0 ]
    p['careLevelNames'] = ['none','low','moderate','substantial','critical']
    p['careDemandInHours'] = [ 0.0, 8.0, 16.0, 36.0, 80.0 ] # [ 0.0, 8.0, 16.0, 30.0, 80.0 ] #[ 0.0, 12.0, 24.0, 48.0, 96.0 ]
    
    ## Cost of care for tax burden
    p['hourlyCostOfCare'] = 20.0

    ## Fertility statistics
    p['growingPopBirthProb'] = 0.215
    p['steadyPopBirthProb'] = 0.13
    p['transitionYear'] = 1965
    p['minPregnancyAge'] = 17
    p['maxPregnancyAge'] = 42

    ## Class and employment statistics
    p['numOccupationClasses'] = 3
    p['occupationClasses'] = ['lower','intermediate','higher']
    p['cdfOccupationClasses'] = [ 0.6, 0.9, 1.0 ]

    ## Age transition statistics
    p['ageOfAdulthood'] = 16
    p['ageOfRetirement'] = 65
    p['probOutOfTownStudent'] = 0.5
    
    # Migration parameters
    p['minMigrationAge'] = 20
    p['maxMigrationAge'] = 35
    p['medianMigrantAge'] = 27
    p['betaMigration'] = 0.5
    
    ## Marriage and divorce statistics (partnerships really)
    p['basicFemaleMarriageProb'] = 0.25
    p['femaleMarriageModifierByDecade'] = [ 0.0, 0.5, 1.0, 1.0, 1.0, 0.6, 0.5, 0.4, 0.1, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['basicMaleMarriageProb'] =  0.3 
    p['maleMarriageModifierByDecade'] = [ 0.0, 0.16, 0.5, 1.0, 0.8, 0.7, 0.66, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.0, 0.0, 0.0 ]
    p['basicDivorceRate'] = 0.1 # 0.06
    p['variableDivorce'] = 0.1 # 0.06
    p['divorceModifierByDecade'] = [ 0.0, 1.0, 0.9, 0.5, 0.4, 0.2, 0.1, 0.03, 0.01, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0, 0.0 ]
    p['divorceBias'] = 0.85
    p['probChildrenWithFather'] = 0.1
    
    ## Leaving home and moving around statistics
    p['probApartWillMoveTogether'] = 1.0 # 0.3
    p['coupleMovesToExistingHousehold'] = 0.0 # 0.3
    p['basicProbAdultMoveOut'] = 0.22
    p['probAdultMoveOutModifierByDecade'] = [ 0.0, 0.2, 1.0, 0.6, 0.3, 0.15, 0.03, 0.03, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['basicProbSingleMove'] = 0.05
    p['probSingleMoveModifierByDecade'] = [ 0.0, 1.0, 1.0, 0.8, 0.4, 0.06, 0.04, 0.02, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['basicProbFamilyMove'] = 0.03
    p['probFamilyMoveModifierByDecade'] = [ 0.0, 0.5, 0.8, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ]
    p['agingParentsMoveInWithKids'] = 0.1
    p['variableMoveBack'] = 0.1
    
    # Relocation Parameters
    p['careAttractionExp'] = 0.002
    p['networkDistanceParam'] = 0.5
    p['relativeRentExp'] = 0.01
    p['rentExp'] = 0.1
    p['sesShareExp'] = 1.0
    p['knaExp'] = 0.001
    p['yearsInTownBeta'] = 0.5
    p['scalingFactor'] = 0.8
    p['relocationCostBeta'] = 0.5
    
    p['relocationCostParam'] = 0.5
    p['supportNetworkBeta'] = 0.1
    
    p['incomeRelocationBeta'] = 0.0002
    p['baseRelocationRate'] = 0.1
    
    # p['supportNetworkBeta'] = 0.1
    # p['incomeRelocationBeta'] = 0.0002
    # p['baseRelocationRate'] = 0.1

    # Save default parameters in separated folder
    folder = 'defaultSimFolder'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filePath = folder + '/defaultParameters.csv'
    c = p.copy()
    for key, value in c.iteritems():
        if not isinstance(value, list):
            c[key] = [value]
    with open(filePath, "wb") as f:
        csv.writer(f).writerow(c.keys())
        csv.writer(f).writerows(itertools.izip_longest(*c.values()))

    return p


def loadScenarios():
    defaultParams = pd.read_csv('defaultParameters.csv', sep=',', header=0)
    sensitivityParams = pd.read_csv('sensitivityParameters.csv', sep=',', header=0)
    names = sensitivityParams.columns
    numberRows = sensitivityParams.shape[0]
    defaultScenario = defaultParams.copy()
    defaultScenario['scenarioIndex'] = np.nan

    scenarios = []
    if sensitivityParams['combinationKey'][0] == 0: # Single scenario: default parameters
        defaultScenario['scenarioIndex'][0] = 0
        scenarios.append(defaultScenario)
        
    elif sensitivityParams['combinationKey'][0] == 1: # One scenario for each row of the sensitivityParams file (missing values are set to default)
        index = 0
        for n in range(numberRows):
            newScenario = defaultScenario.copy()
            for i in names[1:]:
                if not pd.isnull(sensitivityParams[i][n]):
                    newScenario[i][0] = sensitivityParams[i][n]
            newScenario['scenarioIndex'][0] = index
            index += 1
            scenarios.append(newScenario)
            
    elif sensitivityParams['combinationKey'][0] == 2: # One scenario for each value in the sensitivityParams file
        index = 0
        for n in range(numberRows):
            for i in names[1:]:
                newScenario = defaultScenario.copy()
                if pd.isnull(sensitivityParams[i][n]):
                    continue
                else:
                    newScenario[i][0] = sensitivityParams[i][n]
                newScenario['scenarioIndex'][0] = index
                index += 1
                scenarios.append(newScenario)
                
    else:  # All the different combinations of values in the sensitivityParams file
        scenariosParametersList = []
        parNames = []
        for i in names[1:]:
            if pd.isnull(sensitivityParams[i][0]):
                continue
            parNames.append(i)
            scenariosParametersList.append([x for x in sensitivityParams[i] if pd.isnull(x) == False])
        combinations = list(itertools.product(*scenariosParametersList))
        index = 0
        for c in combinations:
            newScenario = defaultScenario.copy()
            for v in c:
                newScenario[parNames[c.index(v)]][0] = v
            newScenario['scenarioIndex'][0] = index
            index += 1
            scenarios.append(newScenario)
        
    print 'The number of scenarios is: ' + str(len(scenarios))

    return scenarios

def loadPolicies(scenarios):
    policiesParams = pd.read_csv('policyParameters.csv', sep=',', header=0)
    names = policiesParams.columns
    numberRows = policiesParams.shape[0]
  
    policies = [[] for x in xrange(len(scenarios))]
    
    for i in range(len(scenarios)):
        index = 0
        policyParams = pd.DataFrame()
        policyParams['policyIndex'] = np.nan
        for j in names[1:]:
            policyParams[j] = scenarios[i][j]
        policyParams['policyIndex'][0] = index
        policies[i].append(policyParams)
        index += 1
        
        if policiesParams['combinationKey'][0] != 0:
            if policiesParams['combinationKey'][0] == 1: # One policy for each row of the policyParams file (missing values are set to default)
                for n in range(numberRows):
                    policyParams = policies[i][0].copy()
                    for j in names[1:]:
                        if not pd.isnull(policiesParams[j][n]):
                            policyParams[j][0] = policiesParams[j][n]
                    policyParams['policyIndex'][0] = index
                    index += 1
                    policies[i].append(policyParams)

            elif policiesParams['combinationKey'][0] == 2: # One scenario for each value in the policyParams file
                for n in range(numberRows):
                    for j in names[1:]:
                        policyParams = policies[i][0].copy()
                        if not pd.isnull(policiesParams[j][n]):
                            policyParams[j][0] = policiesParams[j][n]
                        else:
                            continue
                        policyParams['policyIndex'][0] = index
                        index += 1
                        policies[i].append(policyParams)
        
            else: # All the different combinations of values in the policyParams file
                policyList = []
                parNames = []
                for j in names[1:]:
                    if pd.isnull(policiesParams[j][0]):
                        continue
                    parNames.append(j)
                    policyList.append([x for x in policiesParams[j] if pd.isnull(x) == False])
                combinations = list(itertools.product(*policyList))
                for c in combinations:
                    policyParams = policies[i][0].copy()
                    for v in c:
                        policyParams[parNames[c.index(v)]][0] = v
                    policyParams['policyIndex'][0] = index
                    index += 1
                    policies[i].append(policyParams)
    
    
    
    # From dataframe to dictionary
    policiesParams = []
    for i in range(len(policies)):
        scenarioPoliciesParams = []
        for j in range(len(policies[i])):
            numberRows = policies[i][j].shape[0]
            keys = list(policies[i][j].columns.values)
            values = []
            for column in policies[i][j]:
                colValues = []
                for r in range(numberRows):
                    if pd.isnull(policies[i][j].loc[r, column]):
                        break
                    colValues.append(policies[i][j][column][r])
                values.append(colValues)
            p = OrderedDict(zip(keys, values))
            for key, value in p.iteritems():
                if len(value) < 2:
                    p[key] = value[0]
            scenarioPoliciesParams.append(p)
        policiesParams.append(scenarioPoliciesParams)
    
    return policiesParams

# multiprocessing functions
def multiprocessParams(scenariosParams, policiesParams, numRepeats, fSeed, folder, n):
    params = []
    for j in range(int(numRepeats)):
        randSeed = int(time.time()/(j+1))
        for i in range(len(scenariosParams)):
            scenPar = OrderedDict(scenariosParams[i])
            scenPar['scenarioIndex'] = i
            scenPar['repeatIndex'] = j
            scenPar['rootFolder'] = folder
            scenPar['randomSeed'] = -1
            if j == 0:
                scenPar['randomSeed'] = fSeed
            else:
                scenPar['randomSeed'] = randSeed
            if n == 0:
                z = OrderedDict(policiesParams[i][0])
                z['policyIndex'] = 0
                z['scenarioIndex'] = i
                z['repeatIndex'] = j
                z['randomSeed'] = scenPar['randomSeed']
                z['rootFolder'] = folder
                params.append([scenPar, z])
            else:
                for k in range(len(policiesParams[i][1:])):
                    z = OrderedDict(policiesParams[i][1:][k])
                    z['policyIndex'] = k+1
                    z['scenarioIndex'] = i
                    z['repeatIndex'] = j
                    z['randomSeed'] = scenPar['randomSeed']
                    z['rootFolder'] = folder
                    params.append([scenPar, z])

    return params

def multiprocessingSim(params):
    # Create Sim instance
    folderRun = params[0]['rootFolder'] + '/Rep_' + str(params[0]['repeatIndex'])
    
    s = Sim(params[0]['scenarioIndex'], params[0], folderRun)
    
    print''
    print 'Policy index: ' + str(params[1]['policyIndex'])
    print 'Random seed: ' + str(params[1]['randomSeed'])
    print 'Params: ' + str(params[1])
    
    s.run(params[1]['policyIndex'], params[1], params[1]['randomSeed'])
        

if __name__ == "__main__":
    
    # Create a folder for the simulation
    timeStamp = datetime.datetime.today().strftime('%Y_%m_%d-%H_%M_%S')
    folder = os.path.join('Simulations_Folder', timeStamp)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Create or update file for graphs
    if not os.path.isfile('./graphsParams.csv'):
        with open("graphsParams.csv", "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((['simFolder', 'doGraphs', 'numRepeats', 'numScenarios', 'numPolicies']))
    else:
        graphsDummy = pd.read_csv('graphsParams.csv', sep=',', header=0)
        numberRows = graphsDummy.shape[0]
        for i in range(numberRows):
            graphsDummy['doGraphs'][i] = 0
        graphsDummy.to_csv("graphsParams.csv", index=False)
        
    
    parametersFromFiles = True
    
    scenariosParams = []
    policiesParams = [[[]]]
    
    numberScenarios = -1
    numberPolicies = -1
    
    if parametersFromFiles == False:
        
        numberScenarios = 1
        numberPolicies = 1
        
        metaParams = meta_params()
        initParams = init_params()
        
        z = metaParams.copy()   # start with x's keys and values
        z.update(initParams) 
        scenariosParams.append(z)
        
    else:
        # Import initial, sensitivity and policy parameters from csv files
        # Create list of scenarios to feed into Sim
        # Create list of policies to feed into Sim.run
        
        # Load meta-parameters
        mP = pd.read_csv('metaParameters.csv', sep=',', header=0)
        numberRows = mP.shape[0]
        keys = list(mP.columns.values)
        values = []
        for column in mP:
            colValues = []
            for i in range(numberRows):
                if pd.isnull(mP.loc[i, column]):
                    break
                colValues.append(mP[column][i])
            values.append(colValues)
        metaParams = OrderedDict(zip(keys, values))
        for key, value in metaParams.iteritems():
            if len(value) < 2:
                metaParams[key] = value[0]
        
        scenarios = loadScenarios()
        
        numberScenarios = len(scenarios)
        
        # From dataframe to dictionary
        scenariosParams = []
        for scenario in scenarios:
            numberRows = scenario.shape[0]
            keys = list(scenario.columns.values)
            values = []
            for column in scenario:
                colValues = []
                for i in range(numberRows):
                    if pd.isnull(scenario.loc[i, column]):
                        break
                    colValues.append(scenario[column][i])
                values.append(colValues)
            p = OrderedDict(zip(keys, values))
            for key, value in p.iteritems():
                if len(value) < 2:
                    p[key] = value[0]
            
            z = metaParams.copy()   # start with x's keys and values
            z.update(p) 
            scenariosParams.append(z)
        
        policiesParams = loadPolicies(scenarios)
        
        numberPolicies = len(policiesParams[0])
    
    # Add graph parameters to graphsParam.csvs file
    with open("graphsParams.csv", "a") as file:
        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
        writer.writerow([timeStamp, 1, int(metaParams['numRepeats']), numberScenarios, numberPolicies])
    
    numRepeats = int(metaParams['numRepeats'])
    fSeed = int(metaParams['favouriteSeed'])
    
    if metaParams['multiprocessing'] == False or parametersFromFiles == False:
    
        for r in range(numRepeats):
            # Create Run folders
            folderRun = folder + '/Rep_' + str(r)
            if not os.path.exists(folderRun):
                os.makedirs(folderRun)
            # Set seed
            seed = fSeed
            if r > 0:
                seed = int(time.time()/(r+1))
            for i in range(len(scenariosParams)):
                n = OrderedDict(scenariosParams[i])
                s = Sim(i, n, folderRun)
                for j in range(len(policiesParams[i])):
                    p = OrderedDict(policiesParams[i][j])
                    s.run(j, p, seed) # Add policy paramters later
                    
    else:
        processors = int(metaParams['numberProcessors'])
        if processors > multiprocessing.cpu_count():
            processors = multiprocessing.cpu_count()
            
        pool = multiprocessing.Pool(processors)
        # Create a list of dictionaries (number repetitions times number of scenarios), adding repeat index for folders' creation
        params = multiprocessParams(scenariosParams, policiesParams, metaParams['numRepeats'], fSeed, folder, 0)
        pool.map(multiprocessingSim, params)
        pool.close()
        pool.join()
        
        if numberPolicies > 1:
            # multiporcessing for the policies
            pool = multiprocessing.Pool(processors)
            # Create a list of policy parameters (numer of policies times number of scenarios times number of repeats)
            params = multiprocessParams(scenariosParams, policiesParams, metaParams['numRepeats'], fSeed, folder, 1)
            pool.map(multiprocessingSim, params)
            pool.close()
            pool.join()
        

























