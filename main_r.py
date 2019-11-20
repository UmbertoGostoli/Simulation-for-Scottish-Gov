 
#from simulation import Sim
from simulation_r import Sim
import multiprocessing
import itertools
from collections import OrderedDict
import time
import datetime
import os
import csv

import pandas as pd
import numpy as np


def init_params():
    """Set up the simulation parameters."""
    p = OrderedDict()

    p['noPolicySim'] = False
    p['multiprocessing'] = False
    p['numberProcessors'] = 9
    p['numRepeats'] = 1
    
    p['startYear'] = 1860
    p['endYear'] = 2040
    p['thePresent'] = 2012
    p['statsCollectFrom'] = 1990
    p['regressionCollectFrom'] = 1960 
    p['implementPoliciesFromYear'] = 2020
    p['yearOutcome'] = 2015
    
    p['favouriteSeed'] = int(time.time()) # 123
    p['loadFromFile'] = False
    p['verboseDebugging'] = False
    p['singleRunGraphs'] = False
    p['saveChecks'] = True
    p['getCheckVariablesAtYear'] = 2015
    # To change through command-line arguments

    p['numberPolicyParameters'] = 2
    p['valuesPerParam'] = 1
    p['numberScenarios'] = 3
    
    ############  Policy Parameters    #######################
    
    # 5th sensitivity parameter - values: [0.00025, 0.0005, 0.001]
    p['incomeCareParam'] = 0.0005 #[0.00025 - 0.001]
    
    p['taxBreakRate'] = 0.0
    p['ageOfRetirement'] = 65
    p['socialSupportLevel'] = 5 # 5: No public support
    p['publicCareAgeLimit'] = 18 # 1000
    p['minWealthMeansTest'] = 14250
    p['maxWealthMeansTest'] = 23250
    p['wealthToPoundReduction'] = 250.0
    p['minimumIncomeGuarantee'] = 189.0
    # p['educationCosts']
    #############################################################
    p['socialCareCreditShare'] = 0.0
    p['maxWtWChildAge'] = 5
     # The basics: starting population and year, etc.
    
    p['discountingFactor'] = 0.03
    
    
    p['initialPop'] = 600   
    
    p['minStartAge'] = 24
    p['maxStartAge'] = 45
    p['numberClasses'] = 5
    p['socialClasses'] = ['unskilled', 'skilled', 'lower', 'middle', 'upper']
    p['initialClassShares'] = [0.2, 0.35, 0.25, 0.15, 0.05]
    p['initialUnemployment'] = [0.25, 0.2, 0.15, 0.1, 0.1]
    p['unemploymentAgeBandParam'] = 0.3
    
    # doDeath function parameters
    p['mortalityBias'] = 0.85 # After 1950
    p['careNeedBias'] = 0.9
    p['unmetCareNeedBias'] = 0.5
    p['baseDieProb'] = 0.0001
    p['babyDieProb'] = 0.005
    p['maleAgeScaling'] = 14.0
    p['maleAgeDieProb'] = 0.00021
    p['femaleAgeScaling'] = 15.5
    p['femaleAgeDieProb'] = 0.00019
    
    p['orphansRelocationParam'] = 0.5
    
    # doBirths function parameters
    p['minPregnancyAge'] = 17
    p['maxPregnancyAge'] = 42
    p['growingPopBirthProb'] = 0.215
    p['fertilityCorrector'] = 1.0
    p['fertilityBias'] = 0.9
    
    # careTransitions function parameters
    p['zeroYearCare'] = 80.0
    p['childcareDecreaseRate'] = 0.25
    p['personCareProb'] = 0.0008
    p['maleAgeCareScaling'] = 18.0 # p['maleAgeCareProb'] = 0.0008
    p['femaleAgeCareScaling'] = 19.0 # p['femaleAgeCareProb'] = 0.0008
    p['baseCareProb'] = 0.0002
    p['careBias'] = 0.9
    p['careTransitionRate'] = 0.7
    p['unmetNeedExponent'] = 1.0 # 0.005 #[0.005 - 0.02]
    
    p['numCareLevels'] = 5
    p['careLevelNames'] = ['none','low','moderate','substantial','critical']
    p['careDemandInHours'] = [ 0.0, 8.0, 16.0, 32.0, 80.0 ]
    p['quantumCare'] = 4.0
    
    # careSupplies getCare and probSuppliers function parameters
    
    ########   Key parameter 1  ##############
    
    
    p['weeklyHours'] = 40.0
    
    
    p['priceChildCare'] = 6 
    p['schoolAge'] = 5
    p['maxFormalChildcareHours'] = 48
    p['schoolHours'] = 30
    p['freeChildcareHours'] = 15
    p['workingParentsFreeChildcareHours'] = 30
    p['minAgeStartChildCareSupport'] = 3
    p['minAgeStartChildCareSupportByIncome'] =  2
    p['maxHouseholdIncomeChildCareSupport'] = 40 # 320
    
    ########   Key parameter 2  ##############
     # 5: No public supply 
    
    p['retiredHours'] = [56.0, 32.0, 16.0, 8.0] # 60.0
    p['studentHours'] = [16.0, 8.0, 4.0, 0.0]
    p['teenAgersHours'] = [16.0, 0.0, 0.0, 0.0]
    p['unemployedHours'] = [28.0, 16.0, 8.0, 4.0]
    p['employedHours'] = [16.0, 8.0, 4.0, 0.0]
    p['formalCareDiscountFactor'] = 0.5

    p['networkDistanceParam'] = 2.0
    p['unmetCareNeedDiscountParam'] = 0.5
    p['shareUnmetNeedDiscountParam'] = 0.5
    # p['pastShareUnmetNeedWeight'] = 0.5
    p['networkSizeParam'] = 10.0 # 1.0

    p['careIncomeParam'] = 0.001
    
    # Hospitalization Costs
    p['qalyBeta'] = 0.18
    p['qalyAlpha'] = 1.5
    p['qalyDiscountRate'] = 0.035
    p['qalyIndexes'] = [1.0, 0.8, 0.6, 0.4, 0.2]
    p['unmetCareHealthParam'] = 0.1
    p['hospitalizationParam'] = 0.5
    p['needLevelParam'] = 2.0
    p['unmetSocialCareParam'] = 2.0
    p['costHospitalizationPerDay'] = 400
    
    # ageTransitions, enterWorkForce and marketWage functions parameters
    p['ageTeenagers'] = 12
    p['minWorkingAge'] = 16
    
    ########   Key parameter 3  ##############
    
    p['careBankingSchemeOn'] = False
    p['socialCareBankingAge'] = 65
    
    p['absoluteCreditQuantity'] = False
    p['quantityYearlyIncrease'] = 0.0
    p['socialCareCreditQuantity'] = 0
    p['kinshipNetworkCarePropension'] = 0.5
    p['volunteersCarePropensionCoefficient'] = 0.01
    p['pensionContributionRate'] = 0.05
    
    p['hillHealthLevelThreshold'] = 3
    p['seriouslyHillSupportRate'] = 0.5
    
    ###   Prices   ####
    p['pricePublicSocialCare'] = 20.0 # [2.55] # 20
    p['priceSocialCare'] = 17.0 # [2.29] # 18
    p['taxBrackets'] = [663, 228, 0] # [28.16, 110.23] # [221, 865]
    p['taxBandsNumber'] = 3
    p['bandsTaxationRates'] = [0.4, 0.2, 0.0] # [0.0, 0.2, 0.4]
    # Tax Break Policy

    
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0] # [0.64, 0.89, 1.27, 1.66, 2.29] #  
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0] #[0.64, 0.89, 1.15, 1.40, 1.78] #  
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0] #[1.27, 1.91, 2.80, 4.21, 6.37] #  
    p['educationCosts'] = [0.0, 100.0, 150.0, 200.0] #[0.0, 12.74, 19.12, 25.49] # 
    
    # Priced growth  #####
    p['wageGrowthRate'] = 1.0 # 1.01338 # 

    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    
    # SES inter-generational mobility parameters
    p['leaveHomeStudentsProb'] = 0.5
    
    p['eduWageSensitivity'] = 0.5 # 0.5
    p['eduRankSensitivity'] = 4.0 # 4.0
    p['costantIncomeParam'] = 40.0 # 40.0
    p['costantEduParam'] = 5.0 #  5.0
    p['careEducationParam'] = 0.1       # 0.05
    
    # p['eduWageSensitivity'] = 0.4 
    # p['eduRankSensitivity'] = 4.0 
    # p['costantIncomeParam'] = 20.0 
    # p['costantEduParam'] = 4.0 
    # p['careEducationParam'] = 0.5 
    
    # p['incEduExp'] = 0.25
    p['educationLevels'] = ['GCSE', 'A-Level', 'HND', 'Degree', 'Higher Degree']
    p['workingAge'] = [16, 18, 20, 22, 24]
    
    # doDivorce function parameters
    p['basicDivorceRate'] = 0.06
    p['variableDivorce'] = 0.06
    p['divorceModifierByDecade'] = [ 0.0, 1.0, 0.9, 0.5, 0.4, 0.2, 0.1, 0.03, 0.01, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['divorceBias'] = 0.85
    
    # doMarriages function parameters
    p['maleMarriageMultiplier'] = 1.4
    p['basicFemaleMarriageProb'] = 0.25
    p['femaleMarriageModifierByDecade'] = [ 0.0, 0.5, 1.0, 1.0, 1.0, 0.6, 0.5, 0.4, 0.1, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['deltageProb'] =  [0.0, 0.1, 0.25, 0.4, 0.2, 0.05]
    p['incomeMarriageParam'] = 0.025
    p['studentFactorParam'] = 0.5
    ########   Key parameter 4  ##############
    p['betaGeoExp'] = 2.0 #[1.0 - 4.0]
    
    p['betaSocExp'] = 2.0
    p['rankGenderBias'] = 0.5
    p['basicMaleMarriageProb'] =  0.9
    p['maleMarriageModifierByDecade'] = [ 0.0, 0.16, 0.5, 1.0, 0.8, 0.7, 0.66, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.0, 0.0, 0.0, 0.0 ]
    
    # jobMarket, updateWork and unemploymentRate functions parameters
    p['unemploymentClassBias'] = 0.75
    p['unemploymentAgeBias'] = [1.0, 0.55, 0.35, 0.25, 0.2, 0.2]
    p['numberAgeBands'] = 6
    p['jobMobilitySlope'] = 0.004
    p['jobMobilityIntercept'] = 0.05
    p['ageBiasParam'] = [7.0, 3.0, 1.0, 0.5, 0.35, 0.15]
    p['deltaIncomeExp'] = 0.05
    p['unemployedCareBurdernParam'] = 0.025
    # Potential key parameter
    p['relocationCareLossExp'] = 1.0 # 40.0 # 
    p['incomeSocialCostRelativeWeight'] = 0.5
    
    p['firingParam'] = 0.2
    p['wageVar'] = 0.1
    p['workDiscountingTime'] = 0.75  # 0.8
    p['sizeWeightParam'] = 0.7
    p['minClassWeightParam'] = 1.0
    p['incomeDiscountingExponent'] = 4.0
    p['discountingMultiplier'] = 2.0
    #p['incomeDiscountingParam'] = 2.0
    
    # relocationPensioners function parameters
    p['agingParentsMoveInWithKids'] = 0.1
    p['variableMoveBack'] = 0.1
    p['retiredRelocationParam'] = 0.001 # 0.005
    
    # houseMap function parameters
    p['geoDistanceSensitivityParam'] = 2.0
    p['socDistanceSensitivityParam'] = 2.0
    p['classAffinityWeight'] = 4.0
    p['distanceSensitivityParam'] = 0.5
    
    # relocationProb function parameters
    p['baseRelocatingProb'] = 0.05
    p['relocationParameter'] = 1.0 
    p['apprenticesRelocationProb'] = 0.5
    #p['expReloc'] = 1.0
    
    # computeRelocationCost and relocation Propensity functions parameters
    p['yearsInTownSensitivityParam'] = 0.5
    p['incomeRelocationFactor'] = 0.01
    
    
     ########   Key parameter 5  ##############
    p['relocationCostParam'] = 0.5 # 1.0 
    
    ########   Key parameter 6  ##############
    p['propensityRelocationParam'] = 1.0 # 2.0 
    p['townRelocationWeight'] = 0.5
    
     ## Description of the map, towns, and houses
    p['mapGridXDimension'] = 8
    p['mapGridYDimension'] = 12    
    p['townGridDimension'] = 70
    p['cdfHouseClasses'] = [ 0.6, 0.9, 5.0 ]
    p['ukMap'] = [0.0, 0.1, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0,
                  0.1, 0.1, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0,
                  0.0, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.2, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0,
                  0.4, 0.0, 0.2, 0.2, 0.4, 0.0, 0.0, 0.0,
                  0.6, 0.0, 0.0, 0.3, 0.8, 0.2, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.6, 0.8, 0.4, 0.0, 0.0,
                  0.0, 0.0, 0.2, 1.0, 0.8, 0.6, 0.1, 0.0,
                  0.0, 0.0, 0.1, 0.2, 1.0, 0.6, 0.3, 0.4,
                  0.0, 0.0, 0.5, 0.7, 0.5, 1.0, 1.0, 0.0,
                  0.0, 0.0, 0.2, 0.4, 0.6, 1.0, 1.0, 0.0,
                  0.0, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]

    p['ukClassBias'] = [0.0, -0.05, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0,
                        -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, -0.05, -0.05, 0.05, 0.0, 0.0, 0.0, 0.0,
                        -0.05, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0,
                        -0.05, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0,
                        0.0, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0,
                        0.0, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, -0.05, 0.0, -0.05, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, -0.05, 0.0, 0.2, 0.15, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.15, 0.0,
                        0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    p['mapDensityModifier'] = 0.6
    # p['numHouseClasses'] = 3
    # p['houseClasses'] = ['small','medium','large']
    
    ## Graphical interface details
    p['interactiveGraphics'] = False #True
    p['delayTime'] = 0.0
    p['screenWidth'] = 1300
    p['screenHeight'] = 700
    p['bgColour'] = 'black'
    p['mainFont'] = 'Helvetica 18'
    p['fontColour'] = 'white'
    p['dateX'] = 70
    p['dateY'] = 20
    p['popX'] = 70
    p['popY'] = 50
    p['pixelsInPopPyramid'] = 2000
    p['num5YearAgeClasses'] = 28
    p['careLevelColour'] = ['blue','green','yellow','orange','red']
    p['houseSizeColour'] = ['brown','purple','yellow']
    p['pixelsPerTown'] = 56
    p['maxTextUpdateList'] = 22
    
    # p['eduEduSensitivity'] = 0.5
    # p['mortalityBias'] = [1.0, 0.92, 0.84, 0.76, 0.68]
    # p['fertilityBias'] = [1.0, 0.92, 0.84, 0.76, 0.68]
    # p['divorceBias'] = [2.0, 1.5, 1.0, 0.75, 0.5]

    ## Transitions to care statistics
    
    ## Availability of care statistics
    
    #p['childHours'] = 5.0
    # p['employedHours'] = 12.0
    #p['homeAdultHours'] = 30.0
    #p['workingAdultHours'] = 25.0
    #p['maxEmployedHours'] = 60.0
    
    #p['lowCareHandicap'] = 0.5
    #p['hourlyCostOfCare'] = 20.0
    
    ## Fertility statistics
    
   # p['steadyPopBirthProb'] = 0.13
   # p['transitionYear'] = 1965
    
    ## Class and employment statistics
    # p['numClasses'] = 5
    # p['occupationClasses'] = ['lower','intermediate','higher']
    # p['cdfOccupationClasses'] = [ 0.6, 0.9, 1.0 ]

    ## Age transition statistics
    # p['ageOfAdulthood'] = 17
    
    ## Marriage function parameters

    # p['femaleMarriageProb'] =  [0.01, 0.15, 0.3, 0.2, 0.1, 0.1, 0.06, 0.05, 0.02, 0.01, 0.01, 0.005]
    # p['maleMarriageProb'] =  [0.005, 0.08, 0.25, 0.25, 0.15, 0.1, 0.07, 0.05, 0.03, 0.02, 0.01, 0.005]
    
    ## Leaving home and moving around statistics
    # p['probApartWillMoveTogether'] = 0.3
    # p['coupleMovesToExistingHousehold'] = 0.3
    # p['basicProbAdultMoveOut'] = 0.22
    # p['probAdultMoveOutModifierByDecade'] = [ 0.0, 0.2, 1.0, 0.6, 0.3, 0.15, 0.03, 0.03, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    # p['basicProbSingleMove'] = 0.05
    # p['probSingleMoveModifierByDecade'] = [ 0.0, 1.0, 1.0, 0.8, 0.4, 0.06, 0.04, 0.02, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    # p['basicProbFamilyMove'] = 0.03
    # p['probFamilyMoveModifierByDecade'] = [ 0.0, 0.5, 0.8, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ]
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

def multiprocessParams(scenariosParams, policiesParams, numRepeats, fSeed, folder, n):
    params = []
    for j in range(int(numRepeats)):
        randSeed = int(time.time()*(j+1))
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
    print params[1]['policyIndex']
    print''
    
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
        
        initParams = init_params()
        
        p = initParams.copy()   
        scenariosParams.append(p)
        
    else:
        # Import initial, sensitivity and policy parameters from csv files
        # Create list of scenarios to feed into Sim
        # Create list of policies to feed into Sim.run
        
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
            
            z = p.copy()   # start with x's keys and values
            scenariosParams.append(z)
        
        policiesParams = loadPolicies(scenarios)
        
        numberPolicies = len(policiesParams[0])
    
    # Add graph parameters to graphsParam.csvs file
    with open("graphsParams.csv", "a") as file:
        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
        writer.writerow([timeStamp, 1, int(p['numRepeats']), numberScenarios, numberPolicies])
    
    numRepeats = int(p['numRepeats'])
    fSeed = int(p['favouriteSeed'])
    
    if p['multiprocessing'] == False or parametersFromFiles == False:
    
        for r in range(numRepeats):
            # Create Run folders
            folderRun = folder + '/Rep_' + str(r)
            if not os.path.exists(folderRun):
                os.makedirs(folderRun)
            # Set seed
            seed = fSeed
            if r > 0:
                seed = int(time.time()*(r+1))
            for i in range(len(scenariosParams)):
                n = OrderedDict(scenariosParams[i])
                s = Sim(i, n, folderRun)
                for j in range(len(policiesParams[i])):
                    p = OrderedDict(policiesParams[i][j])
                    s.run(j, p, seed) # Add policy paramters later
                    
    else:
        processors = int(p['numberProcessors'])
        if processors > multiprocessing.cpu_count():
            processors = multiprocessing.cpu_count()
        
        pool = multiprocessing.Pool(processors)
        # Create a list of dictionaries (number repetitions times number of scenarios), adding repeat index for folders' creation
        params = multiprocessParams(scenariosParams, policiesParams, p['numRepeats'], fSeed, folder, 0)
        pool.map(multiprocessingSim, params)
        pool.close()
        pool.join()
        
        if numberPolicies > 1:
            # multiporcessing for the policies
            pool = multiprocessing.Pool(processors)
            # Create a list of policy parameters (numer of policies times number of scenarios times number of repeats)
            params = multiprocessParams(scenariosParams, policiesParams, p['numRepeats'], fSeed, folder, 1)
            pool.map(multiprocessingSim, params)
            pool.close()
            pool.join()
                
            
    
    
    














