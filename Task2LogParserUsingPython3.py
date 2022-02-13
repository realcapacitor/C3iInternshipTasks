#!/usr/bin/python3
import collections
from email import parser
from operator import mod
import re
import csv
import argparse
from collections import Counter

def getData(log):
    httpdata = re.findall(r"(\d{4}.\d{2}.\d{2})(\s\d{2}:\d{2}:\d{2}).+HTTP.+(POST|GET).+.(\'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\',)", log)
    ftpdata = re.findall(r"(\d{4}.\d{2}.\d{2})(\s\d{2}:\d{2}:\d{2}).+FTP.+.(\'\d{1,3}[^0]\.\d{1,3}\.\d{1,3}\.\d{1,3}\'){1}",log)
    modbusdata = re.findall(r"(\d{4}.\d{2}.\d{2})(\s\d{2}:\d{2}:\d{2}).+Modbus.+.(\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", log)
    snmpdata = re.findall(r'(\d{4}.\d{2}.\d{2})(\s\d{2}:\d{2}:\d{2}).+SNMP.+.(\'\d{1,3}[^0]\.\d{1,3}\.\d{1,3}\.\d{1,3}\'){1}', log)
    bacnetdata = re.findall(r"(\d{4}.\d{2}.\d{2})(\s\d{2}:\d{2}:\d{2}).+Bacnet.+.(\s\d{1,3}[^0]\.\d{1,3}\.\d{1,3}\.\d{1,3})", log)
    return httpdata, ftpdata, modbusdata, snmpdata, bacnetdata

def raw(httpdata, ftpdata, modbusdata, snmpdata, bacnetdata):
    with open('raw.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        header = ["Protocol" ,'Date', 'Time', 'Request', 'IP']
        writer.writerow(header)
    write_raw_csv(httpdata, "HTTP")
    write_raw_csv(ftpdata, "FTP")
    write_raw_csv(modbusdata, "MODBUS")
    write_raw_csv(bacnetdata, "BACnet")
    print("Exported data to raw.csv successfully!")

def write_raw_csv(data, type1):
       with open('raw.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for i in data:
                try:
                    writer.writerow((type1,i[0], i[1], i[2], i[3]))
                except:
                    writer.writerow((type1,i[0], i[1],"None" ,i[2]))



def analyse(httpdata, ftpdata, modbusdata, snmpdata, bacnetdata):
    with open('analyse.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        header = ["Protocol", "IP" ,'Frequency']
        writer.writerow(header)
    http_ips = []
    ftp_ips = []
    modbus_ips = []
    snmp_ips = []
    bacnet_ips = []
    for i in httpdata:
        http_ips.append(i[3])
    for i in ftpdata:
        ftp_ips.append(i[2])
    for i in modbusdata:
        modbus_ips.append(i[2])
    for i in snmpdata:
        snmp_ips.append(i[2])
    for i in bacnetdata:
        bacnet_ips.append(i[2])
    analyseCount(http_ips, "HTTP")
    analyseCount(ftp_ips, "FTP")
    analyseCount(modbus_ips, "MODBUS")
    analyseCount(snmp_ips, "SNMP")
    analyseCount(bacnet_ips, "BACnet")
    print("Done")

def analyseCount(ips, protocol):
    analyseWriteCSV(Counter(ips), protocol)

def analyseWriteCSV(data, protocol):
    with open('analyse.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for i in data:
            writer.writerow((protocol, i, data[i]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", help="Name of log file")
    args = parser.parse_args()
    with open(args.fileName) as file:
        log = file.read()
        print("Processing logs...")
    httpdata, ftpdata, modbusdata, snmpdata, bacnetdata = getData(log)
    choice = input("Enter \'raw\' to export data to the raw.csv file and extract information such as Timestamp, IP, IP Country, Request etc.\nOR\nEnter \'analyse\' to export data to the analyse.csv in form of frequency of each IP : ")
    if choice.lower() == 'raw':
        raw(httpdata, ftpdata, modbusdata, snmpdata, bacnetdata)
    elif choice.lower() == 'analyse':
        analyse(httpdata, ftpdata, modbusdata, snmpdata, bacnetdata)
    else:
        print("okay")
    print("Thank you!!!\nQuiting...")
