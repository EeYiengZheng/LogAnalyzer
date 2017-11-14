import csv
import datetime
from re import *
from dateutil import parser

word_code = '[38866]: '


def errorlog(fin, fout):
    error_dict = {'HttpClientError': 0, 'AccessDenied': 0, 'RuntimeException': 0, 'transport error': 0,
                  'DefaultResponseErrorHandler': 0, 'WARN': 0, 'timeout': 0}
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])

        # open a syslog file to read from
        with open(fin, 'r') as in_file:

            # ------------ Errors --------------------
            # ----------------------------------------
            # ----------------------------------------
            # fail  <---- nothing in the logs
            # unauthorized <---- httpclienterror
            # refused <---- nothing in the logs
            # NoSuchPageException <---- nothing in the logs
            # 500 <---- nothing in the logs

            for line in in_file:
                # -------------- Client Errors --------------
                if search('HttpClientError', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Http Client Error'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['HttpClientError'] += 1

                # -------------- Access Denied --------------
                if search('AccessDenied', line):
                    if search('AuditListener', line):
                        this_word_code = 'AuditListener     :'
                        end_index = line.index(this_word_code) + len(this_word_code)
                    else:
                        end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Access Denied'
                    error_detail = line[end_index:].rstrip()
                    if search('1 --- ', error_detail):
                        end_index = error_detail.index('1 --- ') + len('1 --- ')
                        error_detail = error_detail[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['AccessDenied'] += 1

                # -------------- Runtime Exception --------------
                if search('RuntimeException', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Runtime Exception'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['RuntimeException'] += 1

                # -------------- Transport Error --------------
                if search('transport error', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Transport Error'
                    error_detail = line[end_index:].rstrip()
                    if search('1 --- ', error_detail):
                        end_index = error_detail.index('1 --- ') + len('1 --- ')
                        error_detail_start = error_detail.index('sockJsScheduler')
                        error_detail = error_detail[end_index:53] + " - " + error_detail[error_detail_start:]
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['transport error'] += 1

                # -------------- Default Response Handler Error --------------
                if search('DefaultResponseErrorHandler', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Default Response Error Handler'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['DefaultResponseErrorHandler'] += 1

                # -------------- WARN --------------
                if search('WARN', line):
                    this_word_code = 'WARN '
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Error'
                    error_name = 'Warning'
                    error_detail = line[end_index:].rstrip()
                    if match('1 --- ', error_detail):
                        error_detail = error_detail[5:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['WARN'] += 1

                # -------------- Timeout --------------
                if search('timeout', line):
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Timeout'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    error_dict['timeout'] += 1

    return (error_dict, fout)


    # ------------- Use Cases ----------------
    # ----------------------------------------
    # ----------------------------------------
    # ----------------------------------------


def usagelog(fin, fout):
    usage_dict = {'DockerServerController': 0, 'DockerVolumeController': 0, 'ProvisionController': 0,
                  'BlueprintController': 0}
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])

        # open a syslog file to read from
        with open(fin, 'r') as in_file:

            for line in in_file:
                # Use Case 1: Compute/VM - look for "DockerServerController"
                if search('DockerServerController', line):
                    this_word_code = 'DockerServerController  :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Docker Server Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    usage_dict['DockerServerController'] += 1

                # Use Case 2: Volumes - look for 'DockerVolumeController'
                if search('DockerVolumeController', line):
                    this_word_code = 'DockerVolumeController  :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Docker Volume Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    usage_dict['DockerVolumeController'] += 1

                # Use Case 3: Containers - look for 'ProvisionController'
                if search('ProvisionController', line):
                    this_word_code = 'ProvisionController    :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Provision Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    usage_dict['ProvisionController'] += 1

                # Use Case 4: Blueprints - look for 'BlueprintController'
                if search('BlueprintController', line):
                    this_word_code = 'BlueprintController    :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Blueprint Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)

                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    usage_dict['BlueprintController'] += 1
    return (usage_dict, fout)


"""def errorPieChart(fin, fout):
    dictionary = errorlog(fin, fout)
    return dictionary


def usagePieChart(fin, fout):
    dictionary = usagelog(fin, fout)
    return dictionary"""

"""
Find a term from the error log fs.
Function searches each row of the error file and writes rows that contain
the key word to an output file.
Returns fs, the output file
"""


def searchTerm(fs, term):
    with open('search_term.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
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
    return fs


"""
Find the usage cases in file fs from a certain time period.
Search queries must be in form ''
Function converts a 'start' and 'end' date and/or time to datetime format.
Then the function writes the errors that occurred between those times to the output file, fs.
Returns fs, the output file
"""


def usagePeriod(fs, fout, start, end):
    usage_dict = {'Docker Server Controller': 0, 'Docker Volume Controller': 0, 'Provision Controller': 0,
                  'Blueprint Controller': 0}
    format = "%b %d %H:%M:%S %Y"
    if start > end:
        tmp = end
        end = start
        start = tmp
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])
        with open(fs, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                usage_type = row[0]
                usage_name = row[1]
                usage_date = row[2]
                usage_time = row[3]
                usage_detail = row[4]
                if usage_date != 'date':
                    date = datetime.datetime.strptime(usage_date + " " + usage_time + " 2017", format)
                    if date >= start and date <= end:
                        writer.writerow([usage_type, usage_name, usage_date, usage_time, usage_detail])
                        if usage_name in usage_dict.keys():
                            usage_dict[usage_name] += 1
    return (usage_dict, fout)

"""
Find the errors in file fs from a certain time period.
Search queries must be in form ''
Function converts a 'start' and 'end' date and/or time to datetime format.
Then the function writes the errors that occurred between those times to the output file, fs.
Returns fs, the output file
"""


def errorPeriod(fs, fout, start, end):
    error_dict = {'Http Client Error': 0, 'Access Denied': 0, 'Runtime Exception': 0, 'Transport Error': 0,
                  'Default Response Error Handler': 0, 'Warning': 0, 'Timeout': 0}
    format = "%b %d %H:%M:%S %Y"
    if start > end:
        tmp = end
        end = start
        start = tmp
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
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
                    date = datetime.datetime.strptime(error_date + " " + error_time + " 2017", format)
                    if date >= start and date <= end:
                        writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                        if error_name in error_dict.keys():
                            error_dict[error_name] += 1
    return (error_dict, fout)

"""
Returns the date of the earliest entry
"""
def earliestDate(fin):
    errors = []
    format = "%b %d %H:%M:%S %Y"
    with open(fin, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[2] != 'date':
                errors.append(row)
    errors = sorted(errors, key=lambda entry: datetime.datetime.strptime(entry[2]
                                                                             + " " + entry[3] + " 2017", format))
    return datetime.datetime.strptime(errors[0][2] + " " + errors[0][3] + " 2017", format)

"""
Returns the date of the latest entry
"""
def latestDate(fin):
    errors = []
    format = "%b %d %H:%M:%S %Y"
    with open(fin, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[2] != 'date':
                errors.append(row)
    errors = sorted(errors, key=lambda entry: datetime.datetime.strptime(entry[2]
                                                                             + " " + entry[3] + " 2017", format))
    lastindex = len(errors) - 1
    return datetime.datetime.strptime(errors[lastindex][2] + " " + errors[lastindex][3] + " 2017", format)