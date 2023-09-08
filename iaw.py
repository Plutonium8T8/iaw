import json
import os
import re
import datetime
import stat

OUTPUT_FILE = open("output.txt", "w")

def GetPath():
    print("Input the path of the directory you want to analyse: ")
    dirPath = input()

    while (not os.path.isdir(dirPath)):
        print("The path you input is not valid, please input another path: ")
        dirPath = input()

    return dirPath

def GetConditions():
    conditionsFile = open("conditions.json")

    return json.load(conditionsFile)["conditions"]

def GetNecessaryInfo():
    necessaryInfoFile = open("necessary_information.json")

    return json.load(necessaryInfoFile)["necessary_information"] # [" necessary_information"]

def GetFilesInDir(dirPath):
    try:
        files = os.listdir(dirPath)

        return files, dirPath
    except FileNotFoundError:
        print(f"'{dirPath}' does not exist.")
    except PermissionError:
        print(f"Program does not have access to '{dirPath}'")
    except Exception as e:
        print(f"An error occured while trying to access '{dirPath}': {e}")

    return -1

def ParseDirFiles(dirData):
    conditions = GetConditions()

    necessaryInfo = GetNecessaryInfo()

    for file in dirData[0]:
        if (dirData[1][len(dirData[1]) - 1] == '\\'):
            filePath = dirData[1] + file
        else:
            filePath = dirData[1] + '\\' + file

        if (os.path.exists(filePath)):
            if (os.path.isfile(filePath)):
                if (file.split('.')[len(file.split('.')) - 1] in conditions["extension"]):
                    conditionSatisfied = True

                    for timestamp in conditions["days since its creation"]:
                        if (re.match(r'^[1-9][0-9]+$', timestamp)):
                            for condition in conditions["days since its creation"]:
                                if (condition == "more"):
                                    if ((datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(filePath).st_ctime)).days < int(timestamp)):
                                        conditionSatisfied = False
                                elif (condition == "less"):
                                    if ((datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(filePath).st_ctime)).days > int(timestamp)):
                                        conditionSatisfied = False

                    for timestamp in conditions["days since last access"]:
                        if (re.match(r'^[1-9][0-9]+$', timestamp)):
                            for condition in conditions["days since last access"]:
                                if (condition == "more"):
                                    if ((datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(filePath).st_atime)).days < int(timestamp)):
                                        conditionSatisfied = False
                                elif (condition == "less"):
                                    if ((datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(filePath).st_atime)).days > int(timestamp)):
                                        conditionSatisfied = False
                                    
                    if (conditionSatisfied):
                        if ("file name" in necessaryInfo):
                            OUTPUT_FILE.write("file name: " + file + '\n')
                        if ("last access date" in necessaryInfo):
                            OUTPUT_FILE.write("last access date: " + str(datetime.datetime.fromtimestamp(os.stat(filePath).st_atime)) + '\n')
                        if ("last modification date" in necessaryInfo):
                            OUTPUT_FILE.write("last modification date: " + str(datetime.datetime.fromtimestamp(os.stat(filePath).st_mtime)) + '\n')
                        if ("last metadata change date" in necessaryInfo):
                            OUTPUT_FILE.write("last metadata change date: " + str(datetime.datetime.fromtimestamp(os.stat(filePath).st_ctime)) + '\n')
                        if ("author name" in necessaryInfo):
                            OUTPUT_FILE.write("author name (UID): " + str(os.stat(filePath).st_uid) + '\n')
                        if ("file size" in necessaryInfo):
                            OUTPUT_FILE.write("file size: " + str(os.stat(filePath).st_size) + '\n')
                        if ("file mode" in necessaryInfo):
                            OUTPUT_FILE.write("file mode: " + str(stat.filemode(os.stat(filePath).st_mode)) + '\n')
                        if ("number of hard links" in necessaryInfo):
                            OUTPUT_FILE.write("number of hard links: " + str(os.stat(filePath).st_nlink) + '\n')
                        if ("author group" in necessaryInfo):
                            OUTPUT_FILE.write("author group (GID): " + str(os.stat(filePath).st_gid) + '\n')
                        if ("device" in necessaryInfo):
                            OUTPUT_FILE.write("device: " + str(os.stat(filePath).st_dev) + '\n')
                        if ("file path" in necessaryInfo):
                            OUTPUT_FILE.write("file path: " + filePath + '\n')

                        OUTPUT_FILE.write('\n')
                                
                                

            elif (os.path.isdir(filePath)):
                fileData = GetFilesInDir(filePath)

                if (fileData != -1):
                    ParseDirFiles(fileData)
            else:
                print("Item is not a file nor a directory.")

fileData = GetFilesInDir(GetPath())

if (fileData != -1):
    ParseDirFiles(fileData)

OUTPUT_FILE.close()