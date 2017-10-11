import csv
from re import *
import time

#count = 0
word_code = '[38866]: '

#start_time = time.perf_counter()
# create a new csv file to write to

def errorlog(fin, fout):
    count = 0
    error_dict = {}
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
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
    
            # -------------- Client Errors --------------
            for line in in_file:
                if search('HttpClientError', line):
    
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Http Client Error'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['HttpClientError'] = count
            in_file.seek(0)
    
            # -------------- Access Denied --------------
            for line in in_file:
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
                    count += 1
            error_dict['AccessDenied'] = count
            count = 0
    
            in_file.seek(0)
    
            # -------------- Runtime Exception --------------
            for line in in_file:
                if search('RuntimeException', line):
                
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Runtime Exception'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['RuntimeException'] = count
            count = 0
            in_file.seek(0)
    
            # -------------- Transport Error --------------
            for line in in_file:
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
                    count += 1
            error_dict['transport error'] = count
            count = 0
            in_file.seek(0)
    
            # -------------- Default Response Handler Error --------------
            for line in in_file:
                if search('DefaultResponseErrorHandler', line):
    
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Default Response Error Handler'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['DefaultResponseErrorHandler'] = count
            count = 0
            in_file.seek(0)
    
            # -------------- WARN --------------
            for line in in_file:
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
                    count += 1
            error_dict['WARN'] = count
            count = 0
            in_file.seek(0)
    
            # -------------- Timeout --------------
            for line in in_file:
                if search('timeout', line):
    
                    end_index = line.index(word_code) + len(word_code)
                    error_type = 'Error'
                    error_name = 'Timeout'
                    error_detail = line[end_index:].rstrip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['timeout'] = count
            count = 0
            in_file.seek(0)
    return error_dict
    
    
        # ------------- Use Cases ----------------
        # ----------------------------------------
        # ----------------------------------------
        # ----------------------------------------

def usagelog(fin, fout):
    count = 0
    error_dict = {}
    with open(fout, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'error', 'date', 'time', 'details'])
    
        # open a syslog file to read from
        with open(fin, 'r') as in_file:
    
            # Use Case 1: Compute/VM - look for "DockerServerController"
            for line in in_file:
                if search('DockerServerController', line):
    
                    this_word_code = 'DockerServerController  :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Docker Server Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['DockerServerController'] = count
            count = 0
            in_file.seek(0)
    
            # Use Case 2: Volumes - look for 'DockerVolumeController'
            for line in in_file:
                if search('DockerVolumeController', line):
    
                    this_word_code = 'DockerVolumeController  :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Docker Volume Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            count = 0
            in_file.seek(0)
    
            # Use Case 3: Containers - look for 'ProvisionController'
            for line in in_file:
                if search('ProvisionController', line):
    
                    this_word_code = 'ProvisionController    :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Provision Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['ProvisionController'] = count
            count = 0
            in_file.seek(0)
    
            # Use Case 4: Blueprints - look for 'BlueprintController'
            for line in in_file:
                if search('BlueprintController', line):
    
                    this_word_code = 'BlueprintController    :'
                    end_index = line.index(this_word_code) + len(this_word_code)
                    error_type = 'Use Case'
                    error_name = 'Blueprint Controller'
                    error_detail = line[end_index:].strip()
                    error_date = search('\w{3}\s\d{1,2}', line).group(0)
                    error_time = search('\d{2}:\d{2}:\d{2}', line).group(0)
    
                    writer.writerow([error_type, error_name, error_date, error_time, error_detail])
                    count += 1
            error_dict['BlueprintController'] = count
            count = 0
            in_file.seek(0)
    return error_dict
#print(time.perf_counter() - start_time)
