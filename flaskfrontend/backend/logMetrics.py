import matplotlib.pyplot as plt, mpld3
from matplotlib import rcParams
from backend import logAnalytics, logSearch
import datetime
import calendar
import csv



rcParams['figure.figsize'] = (10, 4)

failureList = ['HttpClientError', 'AccessDenied', 'RuntimeException', \
               'transport error', 'DefaultResponseErrorHandler', 'WARN', \
               'timeout']
errorRequests = ['HttpClientError', 'RuntimeException', \
                 'transport error', 'DefaultResponseErrorHandler']


# With these three following methods, should I use a csv reader?

def requestReliability(fs):
    errorcount = 0
    total = 0
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
    total = 0
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
    with open(fs, 'r') as in_file:
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
    dictionary = logAnalytics.errorlog(fin, fout)
    return dictionary


def usagePieChart(fin, fout):
    dictionary = logAnalytics.usagelog(fin, fout)
    entries = list(dictionary.keys())
    counts = list(dictionary.values())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    patches, texts = plt.pie(counts, colors=colors, startangle=90)
    plt.legend(patches, entries, loc='upper right')
    plt.tight_layout()
    plt.axis('equal')
    fig = plt.figure()
    return mpld3.fig_to_html(fig, template_type='simple')


def errorRate(fs):
    format = "%b %d %H:%M:%S %Y"
    rate_dictionary = {}
    currentdate = datetime.datetime.now()
    currenthour = 0.5
    count = 0
    logSearch.sortbyDate(fs, "logforRate.csv")
    with open("logforRate.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            error_date = row[2]
            error_time = row[3]
            if error_date != 'date':
                date = datetime.datetime.strptime(error_date + " " + error_time \
                                                  + " 2017", format)
                if currenthour == 0.5:
                    currenthour = date.hour
                    currentdate = date
                    firstdate = date
                    count = 1
                    time = str(calendar.month_abbr[date.month]) + \
                           " " + str(date.day) + " " + str(date.hour) + ":00"
                elif date.hour == currenthour \
                        and date.month == currentdate.month \
                        and date.day == currentdate.day:
                    count += 1
                    rate_dictionary[time] = count
                else:
                    currenthour = date.hour
                    currentdate = date
                    time = str(calendar.month_abbr[date.month]) + " " + str(date.day) \
                           + " " + str(date.hour) + ":00"
                    count = 0
    times = list(rate_dictionary.keys())
    x = range(len(rate_dictionary))
    y = list(rate_dictionary.values())
    plt.title("Number of Errors per hour")
    plt.xlabel("Time")
    plt.ylabel("Number of Errors")
    plt.scatter(x, y)
    plt.xticks([i * 4 for i in range(int(len(rate_dictionary) / 4))], \
               [str(datetime.datetime.combine(firstdate, datetime.time(4 * i)).strftime("%b %d %H:00")) \
                for i in range(int(len(rate_dictionary) / 4))])
    plt.plot(x, y)
    fig = plt.figure()
    return mpld3.fig_to_html(fig, template_type='simple')

"""
Statements used for testing

user = 'Emp' # <--- your computer username
file = '/Users/{}/Desktop/syslog3.log'.format(user)

print("Request Reliability: " + str(requestReliability(file)))
print("Session Reliability: " + str(sessionReliability(file)))
print("Mean Transaction Before Failure: " + str(meanTransactionsBeforeFailure(file)))
errorPieChart(file, "logAnalytics.errorlog.csv")
usagePieChart(file, "logAnalytics.usagelog.csv")
errorRate("logAnalytics.errorlog.csv")
"""