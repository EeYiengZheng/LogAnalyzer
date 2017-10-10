import matplotlib.pyplot as plt

from logAnalytics import errorlog, usagelog

import csv

failureList = ['HttpClientError', 'AccessDenied', 'RuntimeException', \
			'transport error', 'DefaultResponseErrorHandler', 'WARN', \
			'timeout']
errorRequests = ['HttpClientError', 'RuntimeException', \
            'transport error', 'DefaultResponseErrorHandler']


def requestReliability(fs):
    errorcount = 0
    total = 0;
    errorfound = False
    with open(fs, 'r') as in_file:
    	for line in in_file:
            for error in errorRequests:
            	if error in line:
            		errorfound = True
            if errorfound:
            	errorcount += 1
            total += 1
            errorfound = False
    return float(errorcount / total)

def sessionReliability(fs):
    count = 0
    total = 0;
    failurefound = False
    with open(fs, 'r') as in_file:
        for line in in_file:
            for fail in failureList:
                if fail in line:
                    failurefound = True
            if failurefound:
                count += 1
            total += 1
            failurefound = False
    return float(count / total)

def meanTransactionsBeforeFailure(fs):
    datalist = []
    count = 0
    failurefound = False
    with open(fs, 'r') as in_file:
        for line in in_file:
            for fail in failureList:
                if fail in line:
                    failurefound = True
            if failurefound and count != 0:
                datalist.append(count)
                count = 0
            else:
                count += 1
                failurefound = False
    return float(sum(datalist) / len(datalist))

def terminalFailureProbability(fs):
    return

def averageSessionLength(fs):
    return

def errorPieChart(fin, fout):
    dictionary = errorlog(fin, fout)
    errors = list(dictionary.keys())
    counts = list(dictionary.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red', 
            'salmon', 'peru']
    patches, texts = plt.pie(counts, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, errors, loc="best")
    plt.axis('equal')
    plt.show()

def usagePieChart(fin, fout):
    dictionary = usagelog(fin, fout)
    entries = list(dictionary.keys())
    counts = list(dictionary.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    patches, texts = plt.pie(counts, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, entries, loc="best")
    plt.axis('equal')
    plt.show()

def errorRate(fin, fout):
    return


print(requestReliability("syslog3.log"))
print(sessionReliability("syslog3.log"))
print(meanTransactionsBeforeFailure("syslog3.log"))
errorPieChart("syslog3.log", "errorlog.csv")
usagePieChart("syslog3.log", "usagelog.csv")