import csv
from re import *
import time
import datetime

count = 0
word_code = '[38866]: '

#start_time = time.perf_counter()
# create a new csv file to write to


"""
Find a term from the error log fs.
Function searches each row of the error file and writes rows that contain
the key word to an output file.
"""
def searchTerm(fs, term):
    with open ('search_term.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])
        with open(fs, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if term in row:
                    error_type = row[0]
                    error_name = row[1]
                    error_date = row[2]
                    error_time = row[3]
                    error_detail = row[4]
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])

"""
Find the errors in file fs from a certain time period.
Search queries must be in form ''
Function converts a 'start' and 'end' date and/or time to datetime format.
Then the function writes the errors that occurred between those times to the output file.
"""
def searchPeriod(fs, start, end):
    format = "%b %d %H:%M:%S %Y"
    s = datetime.datetime.strptime(start + " 2017", format)
    e = datetime.datetime.strptime(end +  " 2017", format)
    if s > e:
        tmp = e
        e = s
        s = tmp
    with open('search_period.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])
        with open(fs, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                error_type = row[0]
                error_name = row[1]
                error_date = row[2]
                error_time = row[3]
                error_detail = row[4]
                if error_date != 'date':
                    date  = datetime.datetime.strptime(error_date + " " + error_time + " 2017", format)
                    if date >= s and date <= e:
                        writer.writerow([error_type, error_name, error_date, error_time, error_detail])

"""
Sort a given log file fs of errors by date.
"""
def sortbyDate(fs):
    errors = []
    format = "%b %d %H:%M:%S %Y"
    with open('sorted_log.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])
        with open(fs, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[2] != 'date':
                    errors.append(row)
        errors = sorted(errors, key=lambda entry: datetime.datetime.strptime(entry[2]+ " " + entry[3] + " 2017", format))
        for entry in errors:
            print(entry[2], entry[3])
        for entry in errors:
                error_type = entry[0][0]
                error_name = entry[0][1]
                error_date = entry[0][2]
                error_time = entry[0][3]
                error_detail = entry[0][4]
                writer.writerow([error_type, error_name, error_date, error_time, error_detail])
"""
Example commands used for debugging
"""
searchTerm("log_test.csv", "Access Denied")
searchPeriod("log_test.csv", "Aug 24 00:00:00", "Aug 22 00:00:00")
sortbyDate("log_test.csv")