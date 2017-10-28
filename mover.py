import shutil
import os
import configparser
from time import sleep
from datetime import datetime

loop = True
while loop is True:
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        settings = config['CONFIGURATION']
        rules = config['RULES']

        if 'loop' in settings:
            loop = settings['loop']
            if(loop == "True" or loop == "true"):
                loop = True
            else:
                loop = False
        else:
            loop = False
        
        if 'base_path' in settings:
            basepath = settings['base_path'] + "/"
        else:
            basepath = ""
            
        originalpath = settings['search_path']
        if(originalpath == ""):
            originalpath = ""
        else:
            originalpath = originalpath + "/"

        for rule in rules:
            pass
            #print(rule, rules[rule])

        for filename in os.listdir(basepath + originalpath):
            name, file_extension = os.path.splitext(basepath + originalpath + filename)
            if file_extension in rules:
                #print(basepath + originalpath + filename)
                #print(basepath + rules[file_extension])
                try:
                    shutil.move(basepath + originalpath + filename, basepath + rules[file_extension])
                except Exception as e:
                    logname = "log.txt"
                    if os.path.exists(logname):
                        file = open(logname, 'a')
                        file.write(str(datetime.now()) + " ----> " + str(e) + "\n")
                        file.close()
        print("No errors encountered, successfully executed")

        if(loop is True):
            delay = float(settings["delay"])
            print("delaying for " + str(delay) + " seconds")
            sleep(delay)
                
    except Exception as e:
        logname = "log.txt"
        if os.path.exists(logname):
            file = open(logname, 'a')
            file.write(str(datetime.now()) + " ----> FATAL " + str(e) + "\n")
            file.close()
        print(e)
        break
                
