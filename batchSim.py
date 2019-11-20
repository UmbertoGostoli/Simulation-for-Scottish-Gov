# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:36:11 2018

@author: Umberto Gostoli
"""


from simulation import Sim
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import time
import random
import os
from sklearn.externals import joblib
import fnmatch


class Simulation:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, params):
        
        self.p = dict(params)
        
        # self.year = self.p['startYear']
        # self.times = []
        
        # Output variables
        self.shareUnmetCareDemand = []
        self.averageUnmetCareDemand = []
        self.totalQALY = []
        self.averageQALY = []
        self.discountedQALY = []
        self.averageDiscountedQALY = []
        self.perCapitaHealthCareCost = []
        self.returnList = []
        
    def run(self, params):
        
        self.returnList = []
        # sys.setrecursionlimit(10000)
        # print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        
        if self.p['noPolicySim'] == True:
                
            folder  = 'N:/Social Care Model II/Charts/NoPolicy_Sim/Repeat_' + str(params)
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
           
            filename = folder + '/parameterValues.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))
                
            self.times = []
            
            random.seed(self.p['favouriteSeed'])
            np.random.seed(self.p['favouriteSeed'])
            self.randomSeed = self.p['favouriteSeed']
            
            if self.p['numRepeats'] > 1:
                rdTime = (int)(time.time())
                self.randomSeed = rdTime
                random.seed(rdTime)
                np.random.seed(rdTime)
                
            values = zip(np.array([self.randomSeed, self.p['incomeCareParam'], self.p['tbrPolicyChange'], self.p['ageOfRetirement'], 
                        self.p['socialSupportLevel']]))
            names = ('randomSeed, incomeCareParam, tbrPolicyChange, ageOfRetirement, socialSupportLevel')
            np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="")
            
            s = Sim(self.p, self.randomSeed, folder)
            s.initializePop()
            
            
            for self.year in range(self.p['startYear'], self.p['endYear']+1):
                
                print(" ")
                print('No policy - Run ' + str(params) + ' - ' + str(self.year))
                
                s.doOneYear(self.year) 
                        
                # self.times.append(self.year)
                
            # s.outputFile(folder)
            
            if self.p['singleRunGraphs']:
                s.doGraphs_fromFile(folder)
                
                # s.doGraphs(folder)
                
            s.interactiveGraphics()
            
            # outputVariables = s.getOutputs()
            
            # s.emptyLists()
            
#            for i in outputVariables:
#                self.returnList.append(i)
#            self.returnList.append(self.times)
#        
#            # Add return statement
#            return self.returnList
                
        else:   
             
            random.seed(self.p['favouriteSeed'])
            np.random.seed(self.p['favouriteSeed'])
            self.randomSeed = self.p['favouriteSeed']
                
            print('Policy Combination: ' + str(params[-1]))
            
            folder  = 'N:/Social Care Model II/Charts/SocPolicy_Sim/Policy_' + str(params[-1]) #
            if not os.path.isdir(os.path.dirname(folder)):
                os.makedirs(folder)
            
            f = Sim(self.p, self.randomSeed, folder)
            f.initializePop()
                     
            policyParameters = [] 
            
            for i in range(self.p['numberPolicyParameters']):
                policyParameters.append(params[i])
            
            
           
            filename = folder + '/parameterValues.csv'
            if not os.path.isdir(os.path.dirname(filename)):
                os.mkdir(os.path.dirname(filename))

            values = zip(np.array([self.randomSeed, self.p['incomeCareParam']*params[0], self.p['tbrPolicyChange']+params[1], 
                        self.p['ageOfRetirement']+params[2], self.p['socialSupportLevel']+params[3]]))
            names = ('randomSeed, incomeCareParam, tbrPolicyChange, ageOfRetirement, socialSupportLevel')
            np.savetxt(filename, np.transpose(values), delimiter=',', fmt='%f', header=names, comments="")
        
            for self.year in range(self.p['startYear'], self.p['endYear']+1):
                
                print(" ")
                print('Policy ' + str(params[-1]) + ' - ' + str(self.year))
                
                if self.year == self.p['implementPoliciesFromYear']:
                    
                    f.updatePolicyParameters(policyParameters)
                
                f.doOneYear(self.year) 
                
                # self.times.append(self.year)
                
            # f.outputFile(folder)
            
            if self.p['singleRunGraphs']:
                f.doGraphs_fromFile(folder)
                
                # s.doGraphs(folder)
                
            f.interactiveGraphics()
            
            # outputVariables = f.getOutputs()
            
#            f.emptyLists()
#
#            for i in outputVariables:
#                self.returnList.append(i)
#            self.returnList.append(self.times)
#        
#            # Add return statement
#            return self.returnList
            
     
    def saveLists(self, listOfLists, names):
        for singleList in listOfLists:
            p = self.subLists(singleList)
            for h in p:
                joblib.dump(h, names[listOfLists.index(singleList)] + '_' + str(p.index(h)) + '.pkl')
        
    def loadList(self, names):
        allLists = []
        for name in names:
            listOfObjects = []
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*' + name + '*.pkl'):
                    listOfObjects.extend(joblib.load(file))
            allLists.append(listOfObjects)
        return allLists
        
    def subLists(self, aList):
        itemsPerGroup = 100
        subLength = (int)(len(aList)/itemsPerGroup)
        remain = len(aList)-subLength*itemsPerGroup
        p = []
        for i in range (subLength):
            h = itemsPerGroup*i
            p.append(aList[h:(h+itemsPerGroup)])
        if remain > 0:
            h = itemsPerGroup*subLength
            p.append(aList[h:(h+remain)])
        return p
        
#        # Sensitivity Chart 6: Shares of Social Care
#        lowSharesSocialCare_M = self.sharesSocialCare_M[0::2]
#        lowSharesSocialCare_SD = self.sharesSocialCare_SD[0::2]
#        highSharesSocialCare_M = self.sharesSocialCare_M[1::2]
#        highSharesSocialCare_SD = self.sharesSocialCare_SD[1::2]
#        
#        N = len(lowSharesSocialCare_M)
#        fig, ax = plt.subplots()
#        index = np.arange(N)    # the x locations for the groups
#        bar_width = 0.35         # the width of the bars
#        p1 = ax.bar(index, lowSharesSocialCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesSocialCare_SD, 
#                    label = 'Low')
#        p2 = ax.bar(index + bar_width, highSharesSocialCare_M, bar_width,color='g', bottom = 0, yerr = highSharesSocialCare_SD, 
#                    label = 'High')
#        ax.set_ylabel('Share of Social Care')
#        ax.set_xlabel('Parameters')
#        ax.set_title('Shares of Social Care Received')
#        ax.set_xticks(index + bar_width/2)
#        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1])
#        fig.tight_layout()
#        filename = folder + '/SharesSocialCareSensitivityGroupedBarChart.pdf'
#        if not os.path.isdir(os.path.dirname(filename)):
#            os.mkdir(os.path.dirname(filename))
#        pp = PdfPages(filename)
#        pp.savefig(fig)
#        pp.close()
#        
#        # Sensitivity Chart 7: Shares of Informal Care
#        lowSharesInformalCare_M = self.sharesInformalCare_M[0::2]
#        lowSharesInformalCare_SD = self.sharesInformalCare_SD[0::2]
#        highSharesInformalCare_M = self.sharesInformalCare_M[1::2]
#        highSharesInformalCare_SD = self.sharesInformalCare_SD[1::2]
#        
#        N = len(lowSharesSocialCare_M)
#        fig, ax = plt.subplots()
#        index = np.arange(N)    # the x locations for the groups
#        bar_width = 0.35         # the width of the bars
#        p1 = ax.bar(index, lowSharesInformalCare_M, bar_width, color='b', bottom = 0, yerr = lowSharesInformalCare_SD, 
#                    label = 'Low')
#        p2 = ax.bar(index + bar_width, highSharesInformalCare_M, bar_width,color='g', bottom = 0, yerr = highSharesInformalCare_SD, 
#                    label = 'High')
#        ax.set_ylabel('Share of Informal Care')
#        ax.set_xlabel('Parameters')
#        ax.set_title('Shares of Informal Care Received')
#        ax.set_xticks(index + bar_width/2)
#        plt.xticks(index + bar_width/2, ('P1', 'P2', 'P3', 'P4'))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1])
#        fig.tight_layout()
#        filename = folder + '/SharesInformalCareSensitivityGroupedBarChart.pdf'
#        if not os.path.isdir(os.path.dirname(filename)):
#            os.mkdir(os.path.dirname(filename))
#        pp = PdfPages(filename)
#        pp.savefig(fig)
#        pp.close()
            
                
            
            
            
            
            
            