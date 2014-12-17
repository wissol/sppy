import os
import csv
import shutil
import time

settings_file = "s.csv"

people_file = "people.csv"
projects_file = "p.csv"
actions_file = "a.csv" # next actions in GTD parlance
backup_directory = '/Users/migueldeluisespinosa/Dropbox/sppy/bu' # change to your own backup directory
backup_file = backup_directory + "/" + "f_backup.csv"
contexts_file = "contexts.csv" 
states_file = "states.csv" # these values should be loaded from settings file

# def load_settings(settings_file): to do

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
    # to be split into two functions append_new_entry_to_file(new_entry, file) and backup_file(file)
    
    # add entries to file
    append_file(work_file,entry)

    # copy work back up file to a new time-stamped backup file
    temporal_backup_file = 'f_backup_'+ time.strftime("%d_%m_%Y_at_%H_%M")+ '.csv'
    shutil.copy2(backup_file,temporal_backup_file)
    shutil.move(temporal_backup_file,backup_directory)

    # append to work backup file    
    shutil.copy2(work_file,backup_file)

def add_action():    
    goOn = True
    
    while goOn:
        
        # Entry -  date gathered 0 , Project 1 , description 2 , context 3 , state 4 , date due 5 , person 6 , order 7 , notes 8
        entry = [] 
                
        #Date Gathered  0
        entry.append(time.strftime("%d/%m/%Y %H:%M:%S"))

        #Project 1
        # to be implemented
       
        #Description 2
        entry.append(input("\n Description: \t").strip(' ').replace(",",";")) # commas replaced with semicolons.

        # Context 3        
        entry.append(choose_in_file(contexts_file))

        # State 4
        entry.append(choose_in_file(states_file))

        # date due 5
        entry.append(filter_dates())

        # person 6
        entry.append(choose_in_file(people_file))

        # order 7
        entry.append("")

        # Notes 8
        entry.append(input("\n Write a note if needed: \t").strip(' ').replace(",","."))

        # Append entry to file      
        append_new_entry_to_file(entry, tasks_file)

        # Ending the loop
        goOn = input("\n Another entry? (n for no)\t")
        if goOn != "":
            if goOn[0].lower() == "n":
                goOn = False


def main_menu():
    
    print("\n")

    for key in sorted(menu_choices):
            print("Enter {} for {}".format(key,menu_choices[key]))

    menu = input("\n Choose an option:\t").strip(" ,")  
        
    try:
        return menu_choices[menu]
    except KeyError:
        print("Try again")
        menu_choices(menu_choices)

menu_choices = {"a":"Add new action", "p":"Add new Project", "l":"Log Work", "w":"Add co-worker", "c":"Add context", "h":"help"}

main_menu(menu_choices)
