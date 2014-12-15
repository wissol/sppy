# Main Module

# contexts
import os
import csv
import shutil
import time

entries = []
work_file = "f.csv" 
people_file = "people.csv"

backup_directory = '/yourBackupPath' #change to your own backup directory (somewhere in your dropbox folder could be a neat idea)
backup_file = backup_directory + "/" + "f_backup.csv"

entryTypes = "entryTypes.csv"
contexts = "contexts.csv" 
states = "states.csv" 


def load_file(file_to_load): #loads a csv file as a list
    csv_file_as_list = []
    with open(file_to_load, newline='') as f:
            csv_file_as_list = []
            reader = csv.reader(f)
            for row in reader:
                csv_file_as_list.append(row)
            f.close

    return csv_file_as_list

def filter_dates():
    day = ""
    month = ""

    while len(day) != 2 or int(day) < 1 or int(day) > 31:
        day = input("\n Day (dd): \t").strip(',')

    while len(month) != 2 or int(month) <1 or int(month) > 12:
        month = input("\n Month (mm): \t").strip(',')

    return day + "/" + month

def choose_in_file(file_to_choose):

    file_as_list = load_file(file_to_choose)
    
    for key in range(0,len(file_as_list)):
        print("Enter {} for {}".format(key,file_as_list[key][0]))

    menu = input("\n Choose an item or add a new one \t")

    try:
        return file_as_list[int(menu)][0]
    except Exception:
        with open(file_to_choose, 'a', newline='') as g:
            g.write(menu)
            g.close()
        return menu

def append_file(file_name,entries):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(entries)

def append_new_entry_to_file(entry):
    
    # add entries to file

    append_file(work_file,entry)

    # copy work back up file to a new time-stamped backup file

    temporal_backup_file = 'f_backup_'+ time.strftime("%d_%m_%Y_at_%H_%M")+ '.csv'

    shutil.copy2(backup_file,temporal_backup_file)

    shutil.move(temporal_backup_file,backup_directory)

    # append to work backup file
    
    shutil.copy2(work_file,backup_file)

    #shutil.move(backup_file,backup_directory)

def add_entry():    
    goOn = True
    book = load_file(work_file)

    while goOn:
        
        entry = ["","","","","","","","",""] 
        # Entry -  date gathered 0 , type 1 , description 2 , context 3 , state 4 , date due 5 , person 6 , order 7 , notes 8
        
        entry_key = 0       

        #Date Gathered  0   

        entry[entry_key] = time.strftime("%d/%m/%Y %H:%M:%S")
        entry_key += 1

        #Type 1

        entry[entry_key] = choose_in_file(entryTypes)
        entry_key += 1

        #Description 2

        entry[entry_key] = input("\n Description: \t").strip(' ').replace(",",";") # commas replaced with semicolons.
        entry_key += 1

        # Context 3     
        
        entry[entry_key] = choose_in_file(contexts)
        entry_key += 1

        # State 4

        entry[entry_key] = choose_in_file(states)
        entry_key += 1

        # date due 5

        entry[entry_key] = filter_dates()
        entry_key += 1

        # person 6

        entry[entry_key] = choose_in_file(people_file)
        entry_key += 1

        # order 7

        entry[entry_key] = "" #to be implemented
        entry_key += 1

        # Notes 8

        entry[entry_key] = input("\n Write a note if needed: \t").strip(' ').replace(",",".")

        # Append entry to entries
        
        append_new_entry_to_file(entry) 

        goOn = input("\n Another entry? (n for no)\t")
        if goOn != "":
            if goOn[0].lower() == "n":
                goOn = False

add_entry()

# to do

# menu 
# 1 add new entry (done)
# 2 filter entries 
# 3 log work 
