# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 15:45:43 2019

@author: ug4d
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
from collections import OrderedDict
import pandas as pd
import csv


def doGraphs(graphsParams, metaParams, sensitivityParams):
    
    folder = graphsParams[0]
    numRepeats = graphsParams[2]
    numScenarios = graphsParams[3]
    numPolicies = graphsParams[4]
    yearOutput = metaParams['yearOutcome']
    simFolder = 'Simulations_Folder/' + folder
    
    multipleRepeatsDF = []
    for repeatID in range(numRepeats):
        repFolder = simFolder + '/Rep_' + str(repeatID)
        multipleScenariosDF = []
        
        with open(os.path.join(repFolder, "Scenarios_Parameters.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((sensitivityParams))
            
        for scenarioID in range(numScenarios):
            scenarioFolder = repFolder + '/Scenario_' + str(scenarioID)
            senParams = pd.read_csv(scenarioFolder + '/scenarioParameters.csv', sep=',', header=0)
            sensitivityData = []
            for par in sensitivityParams[:-1]:
                sensitivityData.append(senParams[par].iloc[0])
            
            multiplePoliciesDF = []
            for policyID in range(numPolicies):
                policyFolder = scenarioFolder + '/Policy_' + str(policyID)
                outputsDF = pd.read_csv(policyFolder + '/Outputs.csv', sep=',', header=0)
                
                if graphsDummy:
                    singlePolicyGraphs(outputsDF, policyFolder, metaParams)
                    
                if policyID == 0:
                    sensitivityData.append(outputsDF.loc[outputsDF['year'] == yearOutput, sensitivityParams[-1]].values[0])
                    with open(os.path.join(repFolder, "Scenarios_Parameters.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow(sensitivityData)
                multiplePoliciesDF.append(outputsDF)
            if numPolicies > 1:
                if graphsDummy:
                    multiplePoliciesGraphs(multiplePoliciesDF, scenarioFolder, metaParams, numPolicies)
            multipleScenariosDF.append(multiplePoliciesDF)
        if numScenarios > 1:
            if graphsDummy:
                multipleScenariosGraphs(multipleScenariosDF, repFolder, metaParams, numPolicies, numScenarios)
        multipleRepeatsDF.append(multipleScenariosDF)
    if numRepeats > 1:
        if graphsDummy:
            multipleRepeatsGraphs(multipleRepeatsDF, simFolder, metaParams, numPolicies, numScenarios, numRepeats)
    
    
def singlePolicyGraphs(output, policyFolder, p):
    
    folder = policyFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    policyYears = int((p['endYear']-p['implementPoliciesFromYear']) + 1)
    
    # Fig. 1: Met social care needs by kind and unmet social care need (hours per week)
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalSocialCareReceived'], output['formalSocialCareReceived'], 
                 output['publicSupply'], output['unmetSocialCareNeed'],
                 labels = ['Informal Care','Formal Care', 'Public Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.label.set_fontsize(12)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    # ax.set_title('Social Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Figure 2: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalSocialCareReceived'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalSocialCareReceived'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['publicSupply'], linewidth = 3, label = 'Public Care')
    p4, = ax.plot(output['year'], output['unmetSocialCareNeed'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Delivered and Unmet Care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    # plt.ylim(0, 25)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    # Figure 2: informal and formal care and unmet care need
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Informal Care')
    p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Formal Care')
    p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0, 25)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 3: informal and formal social care received and unmet social care need by care need level
    n_groups = p['numCareLevels']-1
    meanInformalCareReceived_1 = np.mean(output['meanInformalSocialCareReceived_N1'][-policyYears:])
    meanFormalCareReceived_1 = np.mean(output['meanFormalSocialCareReceived_N1'][-policyYears:])
    meanUnmetNeed_1 = np.mean(output['meanUnmetSocialCareNeed_N1'][-policyYears:])
    meanInformalCareReceived_2 = np.mean(output['meanInformalSocialCareReceived_N2'][-policyYears:])
    meanFormalCareReceived_2 = np.mean(output['meanFormalSocialCareReceived_N2'][-policyYears:])
    meanUnmetNeed_2 = np.mean(output['meanUnmetSocialCareNeed_N2'][-policyYears:])
    meanInformalCareReceived_3 = np.mean(output['meanInformalSocialCareReceived_N3'][-policyYears:])
    meanFormalCareReceived_3 = np.mean(output['meanFormalSocialCareReceived_N3'][-policyYears:])
    meanUnmetNeed_3 = np.mean(output['meanUnmetSocialCareNeed_N3'][-policyYears:])
    meanInformalCareReceived_4 = np.mean(output['meanInformalSocialCareReceived_N4'][-policyYears:])
    meanFormalCareReceived_4 = np.mean(output['meanFormalSocialCareReceived_N4'][-policyYears:])
    meanUnmetNeed_4 = np.mean(output['meanUnmetSocialCareNeed_N4'][-policyYears:])
    informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                    meanInformalCareReceived_4)
    formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                  meanFormalCareReceived_4)
    sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
    unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4)
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
    p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
    p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('NL 1', 'NL 2', 'NL 3', 'NL 4'), fontsize = 12)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Informal, Formal and Unmet Social Care by Care Need Level')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCarePerRecipientByNeedLevelStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 4: Hours of informal and formal social care and unmet social care need per recipient by SES
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = np.mean(output['informalSocialCarePerRecipient_1'][-policyYears:])
    meanFormalCareReceived_1 = np.mean(output['formalSocialCarePerRecipient_1'][-policyYears:])
    meanUnmetNeed_1 = np.mean(output['unmetSocialCarePerRecipient_1'][-policyYears:])
    meanInformalCareReceived_2 = np.mean(output['informalSocialCarePerRecipient_2'][-policyYears:])
    meanFormalCareReceived_2 = np.mean(output['formalSocialCarePerRecipient_2'][-policyYears:])
    meanUnmetNeed_2 = np.mean(output['unmetSocialCarePerRecipient_2'][-policyYears:])
    meanInformalCareReceived_3 = np.mean(output['informalSocialCarePerRecipient_3'][-policyYears:])
    meanFormalCareReceived_3 = np.mean(output['formalSocialCarePerRecipient_3'][-policyYears:])
    meanUnmetNeed_3 = np.mean(output['unmetSocialCarePerRecipient_3'][-policyYears:])
    meanInformalCareReceived_4 = np.mean(output['informalSocialCarePerRecipient_4'][-policyYears:])
    meanFormalCareReceived_4 = np.mean(output['formalSocialCarePerRecipient_4'][-policyYears:])
    meanUnmetNeed_4 = np.mean(output['unmetSocialCarePerRecipient_4'][-policyYears:])
    meanInformalCareReceived_5 = np.mean(output['informalSocialCarePerRecipient_5'][-policyYears:])
    meanFormalCareReceived_5 = np.mean(output['formalSocialCarePerRecipient_5'][-policyYears:])
    meanUnmetNeed_5 = np.mean(output['unmetSocialCarePerRecipient_5'][-policyYears:])
    informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                    meanInformalCareReceived_4, meanInformalCareReceived_5)
    formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                  meanFormalCareReceived_4, meanFormalCareReceived_5)
    sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
    unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    
    fig, ax = plt.subplots()
    p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
    p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
    p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'), fontsize = 12)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Informal, Formal and Unmet Social Care Need per Recipient')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCarePerRecipientByClassStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 5: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales'], linewidth = 3, color = 'red')
    # p2, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_1'], label = 'Class I')
    # p3, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_2'], label = 'Class II')
    # p4, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_3'], label = 'Class III')
    # p5, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_4'], label = 'Class IV')
    # p6, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care')
    # ax.set_xlabel('Year')
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(loc = 'lower left')
    # ax.legend_.remove()
    # ax.set_title('Share of Informal Care supplied by Women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    # ax.set_ylim([0, 0.8])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareCareWomedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 6: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['ratioIncome'], linewidth = 3, color = 'red')
    # p2, = ax.plot(output['year'], output['ratioIncome_1'], label = 'Class I')
    # p3, = ax.plot(output['year'], output['ratioIncome_2'], label = 'Class II')
    # p4, = ax.plot(output['year'], output['ratioIncome_3'], label = 'Class III')
    # p5, = ax.plot(output['year'], output['ratioIncome_4'], label = 'Class IV')
    # p6, = ax.plot(output['year'], output['ratioIncome_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Income Ratio')
    # ax.set_xlabel('Year')
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(loc = 'upper left')
    # ax.set_title('Women and Men Income Ratio')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenIncomeRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 7: informal and formal care supplied by kinship network distance (mean of last 20 years) # Modified y lim
    n_groups = 5
    meanInformalCareHousehold = np.mean(output['sumNoK_informalSupplies[0]'][-policyYears:])
    meanFormalCareHousehold = np.mean(output['sumNoK_formalSupplies[0]'][-policyYears:])
    meanInformalCare_K1 = np.mean(output['sumNoK_informalSupplies[1]'][-policyYears:])
    meanFormalCare_K1 = np.mean(output['sumNoK_formalSupplies[1]'][-policyYears:])
    meanInformalCare_K2 = np.mean(output['sumNoK_informalSupplies[2]'][-policyYears:])
    meanFormalCare_K2 = np.mean(output['sumNoK_formalSupplies[2]'][-policyYears:])
    meanInformalCare_K3 = np.mean(output['sumNoK_informalSupplies[3]'][-policyYears:])
    meanFormalCare_K3 = np.mean(output['sumNoK_formalSupplies[3]'][-policyYears:])
    meanPublicCare = np.mean(output['publicSupply'][-policyYears:])
    informalCare = (meanInformalCareHousehold, meanInformalCare_K1, meanInformalCare_K2, meanInformalCare_K3, 0)
    formalCare = (meanFormalCareHousehold, meanFormalCare_K1, meanFormalCare_K2, meanFormalCare_K3, 0)
    publicCare = (0, 0, 0, 0, meanPublicCare)
    totCare = [sum(x) for x in zip(informalCare, formalCare, publicCare)]
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
    p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
    p3 = ax.bar(ind, publicCare, width, bottom = [sum(x) for x in zip(informalCare, formalCare)], label = 'Public Care')
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_ylabel('Total hours of care')
    ax.set_xticks(ind)
    plt.xticks(ind, ('Household', 'I', 'II', 'III', 'Public Care'), fontsize=12)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.yaxis.label.set_fontsize(12)
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    # ax.set_title('Informal and Formal Care per Kinship Level')
    fig.tight_layout()
    path = os.path.join(folder, 'InformalFormalCareByKinshipStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 8: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['perCapitaHospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    # ax.set_title('Per Capita Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaHealthCareCostChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['currentPop'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Population')
    # ax.set_xlabel('Year')
    # ax.set_title('Public share of social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'currentPopChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['perCapitaUnmetCareDemand'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of Unmet Care Need')
    # ax.set_xlabel('Year')
    # ax.set_title('Public share of social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareDemandChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['sharePublicSocialCare'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of Total Care')
    # ax.set_xlabel('Year')
    # ax.set_title('Public share of social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'sharePublicSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareUnmetCareDemand'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of Care Need')
    # ax.set_xlabel('Year')
    # ax.set_title('Public share of social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemandChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 10: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['costPublicSocialCare'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    # ax.set_xlabel('Year')
    # ax.set_title('Cost of public social care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.yaxis.label.set_fontsize(12)
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'costPublicSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    

def multiplePoliciesGraphs(output, scenarioFolder, p, numPolicies):
    
    folder = scenarioFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    
    policyYears = int(p['endYear']-p['implementPoliciesFromYear']) + 1
    
    # Add graphs across policies (within the same run/scenario)
    
    #############################  Population   #######################################
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['currentPop'], label = labelPolicy))
    # ax.set_title('Populations')
    ax.set_ylabel('Number of people')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
    # ax.set_xlim(left = p['statsCollectFrom'])
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    # ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
    fig.tight_layout()
    path = os.path.join(folder, 'popGrowth_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['perCapitaUnmetCareDemand'], label = labelPolicy))
    # ax.set_title('Populations')
    ax.set_ylabel('Hours of Unmet Care Need')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareDemand_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCareNeed'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCareNeed_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    

    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient_1'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_I_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient_2'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_II_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient_3'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_III_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient_4'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_IV_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['unmetSocialCarePerRecipient_5'], label = labelPolicy))
    # ax.set_title('Unmet Social Care Need')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipient_V_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['shareUnmetCareDemand'], label = labelPolicy))
    # ax.set_title('Share of Unmet Care Demand')
    ax.set_ylabel('Share of care demand')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['totalCareReceived'], label = labelPolicy))
    # ax.set_title('Share of Unmet Care Demand')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'totalCareReceived_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['costPublicSocialCare'], label = labelPolicy))
    # ax.set_title('Cost of Public Social Care')
    ax.set_ylabel('Pounds per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'costPublicSocialCare_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['informalSocialCareReceived'], label = labelPolicy))
    # ax.set_title('Informal Social Care')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'informalSocialCareReceived_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots() # Argument: figsize=(5, 3)
    graph = []
    for i in range(numPolicies):
        labelPolicy = 'Policy ' + str(i)
        if i == 0:
            labelPolicy = 'Benchmark'
        graph.append(ax.plot(output[i]['year'], output[i]['formalSocialCareReceived'], label = labelPolicy))
    # ax.set_title('Formal Social Care')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    handels, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower right')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(int(p['statsCollectFrom']), int(p['endYear']+1), 10))
    fig.tight_layout()
    path = os.path.join(folder, 'formalSocialCareReceived_axPol.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()

    ########################### Share of Umnet Care Needs    #################################
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(output[i]['totalCareReceived'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    # plt.ylim(500000, 600000)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Hours of Care')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Total Social Care Received')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaCareReceivedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemandBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_1'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_I_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_2'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_II_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_3'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_III_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_4'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_IV_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_5'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_V_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    ind = np.arange(len(objects))
    width = 0.15
    sharesByClass = []
    for j in range(5):
        shareUnmetCareDemand = []
        for i in range(numPolicies):
            shareUnmetCareDemand.append(np.mean(output[i]['shareUnmetCareDemand_' + str(j+1)][-policyYears:]))
        sharesByClass.append(shareUnmetCareDemand)
    rects1 = ax.bar(ind - width*2, sharesByClass[0], width, label='Class I') # yerr=degreeSuppliers['sd1'],
    rects2 = ax.bar(ind - width, sharesByClass[1], width, label='Class II') # yerr=degreeSuppliers['sd1'],
    rects3 = ax.bar(ind, sharesByClass[2], width, label='Class III') # yerr=degreeSuppliers['sd12'],
    rects4 = ax.bar(ind + width, sharesByClass[3], width, label='Class IV') # yerr=degreeSuppliers['sd123'],
    rects5 = ax.bar(ind + width*2, sharesByClass[4], width, label='Class V')
    
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(0.32, 0.45)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share Unmet Need')
    ax.yaxis.label.set_fontsize(12)
    ax.set_title('Unmet Care Needs Shares across policies by SES')
    
    fig.tight_layout()
    path = os.path.join(folder, 'shareUnmetCareDemand_GroupedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['unmetSocialCarePerRecipient'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    plt.ylim(12, 14)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Share Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'unmetSocialCarePerRecipientBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['totalCareNeed'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Total care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'totalCareNeedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.mean(output[i]['totalCareNeed'][-policyYears:])/np.mean(output[i]['currentPop'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Average care need')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Average Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'averageCareNeedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    # Fig. 9: Bar charts of total unmet care need by Policy
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(output[i]['unmetSocialCareNeed'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.ylim(400000, 500000)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Hours of Unmet Care')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Total Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalUnmetCareNeedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 10: bar chart of direct policy costs (net of tax revenue changes)
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        totalCost = np.sum(output[i]['costPublicSocialCare'][-policyYears:]) + np.sum(output[i]['totalTaxRefund'][-policyYears:])
        shareUnmetCareDemand.append(totalCost)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Pounds per week')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Total Policy Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalPolicyCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 11: bar chart of ICER
    fig, ax = plt.subplots()
    objects = ('Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    benchmarkRevenue = np.sum(output[0]['taxRevenue'][-policyYears:])/np.sum(output[0]['currentPop'][-policyYears:])
    benchmarkCost = np.sum(output[0]['costPublicSocialCare'][-policyYears:]) + np.sum(output[0]['totalTaxRefund'][-policyYears:])/np.sum(output[0]['currentPop'][-policyYears:])
    benchmarkBudget = benchmarkCost - benchmarkRevenue
    print 'Benchmark budget:' + str(benchmarkBudget)
    benchmarkUnmetCareNeed = np.mean(output[0]['shareUnmetCareDemand'][-policyYears:])
    for i in range(1, numPolicies):
        policyRevenue = np.sum(output[i]['taxRevenue'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:])
        policyCost = np.sum(output[i]['costPublicSocialCare'][-policyYears:]) + np.sum(output[i]['totalTaxRefund'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:])
        policyBudget = policyCost - policyRevenue
        print 'Policy budget:' + str(policyBudget)
        policyUnmetCareNeed = np.mean(output[i]['shareUnmetCareDemand'][-policyYears:])
        # icer = (benchmarkBudget-policyBudget)/(benchmarkUnmetCareNeed-policyUnmetCareNeed)
        # icer = (policyCost-benchmarkCost)/(benchmarkUnmetCareNeed-policyUnmetCareNeed)
        percentageIncreaseCost = (policyBudget/benchmarkBudget)
        percentageDecreaseShareUnmetCareNeed = benchmarkUnmetCareNeed/policyUnmetCareNeed
        icer = percentageIncreaseCost/percentageDecreaseShareUnmetCareNeed
        
        shareUnmetCareDemand.append(icer)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per hour')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('ICER')
    fig.tight_layout()
    path = os.path.join(folder, 'ICERB.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 12: bar chart of ICER based on percentage variations
    fig, ax = plt.subplots()
    objects = ('Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    benchmarkRevenue = np.sum(output[0]['taxRevenue'][-policyYears:])/np.sum(output[0]['currentPop'][-policyYears:])
    benchmarkCost = np.sum(output[0]['costPublicSocialCare'][-policyYears:]) + np.sum(output[0]['totalTaxRefund'][-policyYears:])/np.sum(output[0]['currentPop'][-policyYears:])
    benchmarkBudget = benchmarkRevenue - benchmarkCost
    benchmarkUnmetCareNeed = np.mean(output[0]['shareUnmetCareDemand'][-policyYears:])
    # benchmarkUnmetCareNeed = np.mean(output[0]['unmetSocialCarePerRecipient'][-policyYears:])
    for i in range(1, numPolicies):
        policyRevenue = np.sum(output[i]['taxRevenue'][-policyYears:])/np.sum(output[0]['currentPop'][-policyYears:])
        policyCost = np.sum(output[i]['costPublicSocialCare'][-policyYears:]) + np.sum(output[i]['totalTaxRefund'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:])
        percentageIncreaseCost = (policyCost-benchmarkCost)/benchmarkCost
        policyBudget = policyRevenue - policyCost
        policyUnmetCareNeed = np.mean(output[i]['shareUnmetCareDemand'][-policyYears:])
        # policyUnmetCareNeed = np.mean(output[i]['unmetSocialCarePerRecipient'][-policyYears:])
        percentageDecreaseShareUnmetCareNeed = benchmarkUnmetCareNeed-policyUnmetCareNeed
        # icer = (benchmarkBudget-policyBudget)/(benchmarkUnmetCareNeed-policyUnmetCareNeed)
        icer = percentageIncreaseCost/percentageDecreaseShareUnmetCareNeed
        print icer
        shareUnmetCareDemand.append(icer)
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('RICER')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Relative ICER')
    fig.tight_layout()
    path = os.path.join(folder, 'RICERB.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 12: bar chart of hospitalization costs
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append((np.sum(output[i]['hospitalizationCost'][-policyYears:])/52.0)/np.sum(output[i]['currentPop'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Total Hospitalization Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalHospitalizationCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 12: bar chart of hospitalization costs
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(output[i]['informalSocialCareReceived'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    plt.ylim(2.0, 3.0)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Informal Social Care')
    fig.tight_layout()
    path = os.path.join(folder, 'InformalSocialCareBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Fig. 12: bar chart of hospitalization costs
    fig, ax = plt.subplots()
    objects = ('Benchmark', 'Tax Deduction', 'Direct Funding')
    y_pos = np.arange(len(objects))
    shareUnmetCareDemand = []
    for i in range(numPolicies):
        shareUnmetCareDemand.append(np.sum(output[i]['formalSocialCareReceived'][-policyYears:])/np.sum(output[i]['currentPop'][-policyYears:]))
    ax.bar(y_pos, shareUnmetCareDemand, align='center', alpha=0.5)
    # plt.ylim(400000, 500000)
    plt.xticks(y_pos, objects, fontsize=12)
    ax.xaxis.set_ticks_position('none')
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylabel('Hours per week')
    ax.yaxis.label.set_fontsize(12)
    # ax.set_title('Informal Social Care')
    fig.tight_layout()
    path = os.path.join(folder, 'formalSocialCareBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    
   
   
def multipleScenariosGraphs(output, repFolder, p, numPolicies, numScenarios):
    
    folder = repFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    scenarios = []
    for i in range(numScenarios):
        scenarios.append('Scenario ' + str(i+1))
        
    # Add graphs across scenarios (for the same policies)
    for j in range(numPolicies):
        
        # Plots of values in the period 1990-2040, for each scenario (single run)
        fig, ax = plt.subplots() # Argument: figsize=(5, 3)
        graph = []
        for i in range(numScenarios):
            graph.append(ax.plot(output[i][j]['year'], output[i][j]['currentPop'], label = 'Scenario ' + str(i+1)))
        # p2, = ax.plot(output[1][0]['year'], output[1]['currentPop'], color="blue", label = 'Policy 1')
        ax.set_title('Populations - P' + str(j))
        ax.set_ylabel('Number of people')
        handels, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower right')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
        ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
        fig.tight_layout()
        path = os.path.join(folder, 'popGrowth_axScen_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Bar Charts of mean values in the period 2025-2035, for each sceanario (single run)
        meansOutput = []
        sdOutput = []
        for i in range(numScenarios):
            policyWindow = []
            for yearOutput in range(2025, 2036, 1):
                policyWindow.append(output[i][j].loc[output[i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
            meansOutput.append(np.mean(policyWindow))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(scenarios))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios)
        ax.set_title('Unmet Social Care (mean 2025-2035) - P' + str(j))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
    
    

def multipleRepeatsGraphs(output, simFolder, p, numRepeats, numPolicies, numScenarios):
    
    folder = simFolder + '/Graphs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    

    # Add graphs across runs (for the same scenario/policy combinations)
    # For each policy scenario, take the average of year 2010-2020 for each run, and do a bar chart with error bars for each outcome of interest
    
    # Policy comparison: make charts by outcomes with bars representing the different policies.
    
    
    # Graphs to compare policies across scenarios
    policies = ['Benchmark', 'Policy 1', 'Policy 2']
    
    for i in range(numScenarios):
        
        scenarioFolder = folder + '/Scenario ' + str(i+1)
        if not os.path.exists(scenarioFolder):
            os.makedirs(scenarioFolder)
        
        # Unmet Social Care: mean and sd across the n repeats for the 5 policies.
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Unmet Social Care (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Hospitalization Costs
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'hospitalizationCost'].values[0]/52.0)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per week')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Hospitalization Costs (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'hospitalizationCosts_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Framework for cost graphs
        meansOutput = []
        sdOutput = []
        for j in range(numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    psc = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    tr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    policyWindow.append(psc+tr)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(policies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per week')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(policies)
        ax.set_title('Direct Policy Cost (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'directPolicyCost_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Framework for ICER graphs
        newPolicies = policies[1:]
        meansOutput = []
        sdOutput = []
        for j in range(1, numPolicies):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    ptr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'taxRevenue'].values[0]
                    pdc = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    pr = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    policyBudget = ptr-(pdc+pr)
                    btr = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'taxRevenue'].values[0]
                    bdc = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'costPublicSocialCare'].values[0]
                    br = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'totalTaxRefund'].values[0]
                    benchmarkBudget = btr-(bdc+br)
                    deltaBudget = benchmarkBudget-policyBudget
                    hourUnmetCarePolicy = output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0]
                    hourUnmetCareBenchmark = output[z][i][j].loc[output[z][i][0]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0]
                    deltaCare = hourUnmetCareBenchmark-hourUnmetCarePolicy
                    policyWindow.append(deltaBudget/deltaCare)
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(newPolicies))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Pounds per hour')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(newPolicies)
        ax.set_title('Direct Cost ICER (mean 2025-2035) - S' + str(i+1))
        ax.yaxis.grid(True)
        
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'directICER_S' + str(i+1) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
    # Graphs to compare scenarios across policies
    scenarios = []
    for i in range(numScenarios):
        scenarios.append('Scenario ' + str(i+1))
        
    for j in range(numPolicies):
        
        scenarioFolder = folder + '/Policy ' + str(j)
        if not os.path.exists(scenarioFolder):
            os.makedirs(scenarioFolder)
            
        # Share of Unmet Social Care: mean and sd across the n repeats for the 5 policies.
        meansOutput = []
        sdOutput = []
        for i in range(numScenarios):
            values = []
            for z in range(numRepeats):
                policyWindow = []
                for yearOutput in range(2025, 2036, 1):
                    policyWindow.append(output[z][i][j].loc[output[z][i][j]['year'] == yearOutput, 'unmetSocialCareNeed'].values[0])
                values.append(np.mean(policyWindow))
            meansOutput.append(np.mean(values))
            sdOutput.append(np.std(values))
        fig, ax = plt.subplots()
        x_pos = np.arange(len(scenarios))
        ax.bar(x_pos, meansOutput, yerr=sdOutput, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Unmet Care Needs (h/w)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenarios)
        ax.set_title('Unmet Social Care (mean 2025-2035) - P' + str(j))
        ax.yaxis.grid(True)
    
        fig.tight_layout()
        path = os.path.join(scenarioFolder, 'unmetSocialCareNeed_P' + str(j) + '.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()

    # Add graphs across runs (for the same scenario/policy combinations)
    # For each policy scenario, take the average of year 2010-2020 for each run, and do a bar chart with error bars for each outcome of interest
    
    # Policy comparison: make charts by outcomes with bars representing the different policies.
    
    for j in range(numPolicies):
        for i in range(numScenarios):
            fig, ax = plt.subplots() # Argument: figsize=(5, 3)
            graph = []
            for z in range(numRepeats):
                graph.append(ax.plot(output[z][i][j]['year'], output[z][i][j]['currentPop'], label = 'Run ' + str(z+1)))
            ax.set_title('Populations - ' + 'Scenario ' + str(i+1) + '/Policy ' + str(j))
            ax.set_ylabel('Number of people')
            handels, labels = ax.get_legend_handles_labels()
            ax.legend(loc = 'lower right')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
            ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
            fig.tight_layout()
            path = os.path.join(folder, 'popGrowth_axRep_S' + str(i+1) + '_P' + str(j) + '.pdf')
            pp = PdfPages(path)
            pp.savefig(fig)
            pp.close()
            
    for j in range(numPolicies):
        for i in range(numScenarios):
            fig, ax = plt.subplots() # Argument: figsize=(5, 3)
            graph = []
            for z in range(numRepeats):
                graph.append(ax.plot(output[z][i][j]['year'], output[z][i][j]['unmetSocialCareNeed'], label = 'Run ' + str(z+1)))
            ax.set_title('Unmet Care Needs - ' + 'Scenario ' + str(i+1) + '/Policy ' + str(j))
            ax.set_ylabel('Unmet Care Needs (h/w)')
            handels, labels = ax.get_legend_handles_labels()
            ax.legend(loc = 'lower right')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_xlim(left = int(p['statsCollectFrom']), right = int(p['endYear']))
            ax.set_xticks(range(int(p['statsCollectFrom']), int(p['endYear'])+1, 20))
            fig.tight_layout()
            path = os.path.join(folder, 'unmetCareNeeds_axRep_S' + str(i+1) + '_P' + str(j) + '.pdf')
            pp = PdfPages(path)
            pp.savefig(fig)
            pp.close()


defaultParams = pd.read_csv('defaultParameters.csv', sep=',', header=0)
sensitivityParams = pd.read_csv('sensitivityParameters.csv', sep=',', header=0)
outputVariable = 'shareUnmetCareDemand'
names = sensitivityParams.columns
df = pd.DataFrame(columns = names[1:])
df[outputVariable] = np.nan
columnNames = list(df.columns)

mP = pd.read_csv('defaultParameters.csv', sep=',', header=0)
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

        
graphsParams = pd.read_csv('graphsParams.csv', sep=',', header=0)
dummy = list(graphsParams['doGraphs'])
graphsDummy = True
for i in range(len(dummy)):
    if dummy[i] == 1:
        print df
        doGraphs(graphsParams.loc[i], metaParams, columnNames)

        

