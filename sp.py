import os, csv, shutil, time, argparse

settings_file = "s.csv"

file_names = {"people_file":"people.csv","projects_file":"p.csv",
              "actions_file":"a.csv","contexts_file":"contexts.csv",
              "states_file":"states.csv", "reminders_file":"r.csv",
              "archives_file":"archives.csv"}

backup_directory = '/Users/migueldeluisespinosa/Dropbox/sppy/bu' # change to your own backup directory

# all these values should be loaded from settings file and stored into some structure


def generate_id(id_type):
    actions = load_file(id_type)
    try:
        last_action_id = int(actions[-1][-1]) + 1
    except:
        last_action_id = 0
    action_id = str(last_action_id)
    return action_id

def generate_backup_file_names(backup_directory,file_names):
    backup_file_names = {}
    backup_common_file_name_part = backup_directory + "/" + "backup_"
    for key in file_names:
        backup_file_names["backup_file_" + key] = backup_common_file_name_part + file_names[key]
    return backup_file_names

backup_file_names = generate_backup_file_names(backup_directory, file_names)

def generate_files(file_names):
    for key in file_names:
        f= open(file_names[key], 'a', newline='')
        f.close

generate_files(file_names)
generate_files(backup_file_names) #this three should go in a setup function

# time_zone = load from settings file

# def load_settings(settings_file): to do

def load_file(file_to_load): #loads a csv file as a list
    csv_file_as_list = []
    with open(file_to_load, newline='') as f:
            csv_file_as_list = []
            reader = csv.reader(f)
            for row in reader:
                csv_file_as_list.append(row)
    
    f.close()        
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

def append_file(file_name, entry):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(entry)

def backup_file(work_file, backup_file_name):
    # copy work back up file to a new time-stamped backup file
    temporal_backup_file = backup_file_name + time.strftime("%d_%m_%Y_at_%H_%M")+ '.csv'
    shutil.copy2(work_file,temporal_backup_file)
    
    # append to work backup file    
    shutil.copy2(work_file,backup_file_name)

def append_new_entry_to_file(entry, work_file, backup_file_name): 
        
    # add entries to file
    append_file(work_file,entry)

    backup_file(work_file, backup_file_name)
    
def evaluate_loop(thing)
    answer = input("\n Another {} (n for no)\t".format(thing))
    evaluation = True
    if answer != "":
        if answer[0].lower() == "n":
            evaluation = False
    return evaluation

def add_action():
    goOn = True
    
    while goOn:
        
        # Entry -  date gathered 0 , Project 1 , description 2 , context 3 , state 4 , date due 5 , person 6 , order 7 , notes 8
        action = [] 
                
        #Date Gathered  0
        action.append(time.strftime("%d/%m/%Y %H:%M"))

        #Project 1
        print("Project this action belongs to")
        action.append(choose_in_file(file_names["projects_file"]))
       
        #Description 2
        action.append(input("\n Short Description: \t").strip(' ').replace(",",";")) # commas replaced with semicolons.

        # Context 3
        print("Context of this action")        
        action.append(choose_in_file(file_names["contexts_file"]))

        # State 4
        print("State")
        action.append(choose_in_file(file_names["states_file"]))

        # State Modified date 5
        action.append(time.strftime("%d/%m/%Y %H:%M"))

        # date due 6
        deadline = input("Is this action under a deadline? Press 'y' to introduce one")
        if deadline == "y":
            action.append(filter_dates())
        else:
            action.append("")

        # person 7
        if action[4] == "waiting for" or action[4] == "assigned to":
            action.append(choose_in_file(file_names["people_file"]))
        else:
            action.append("")

        # Notes 8
        action.append(input("\n Write a note if needed: \t").strip(' ').replace(",","."))
     
        # id 9
        action_id = generate_id(file_names["actions_file"])
        action.append(action_id)

        # Append action to file      
        append_new_entry_to_file(action, file_names["actions_file"], backup_file_names["backup_file_" + "actions_file"])

        #offer to add reminder?

        # Ending the loop
        goOn = evaluate_loop("action")     

def add_project():
    goOn = True

    while goOn:
        
        # Project -  description 0, date gathered 1, date due 2, notes 3
        project = [] 

        #Description 0
        project.append(input("\n Description: \t").strip(' ').replace(",",";")) # commas replaced with semicolons.
        # check there's no project with the same description

        #Date Gathered  1
        project.append(time.strftime("%d/%m/%Y %H:%M:%S"))

        # date due 2
        project.append(filter_dates())

        # Notes 3
        project.append(input("\n Write a note if needed: \t").strip(' ').replace(",","."))

        # Id 4
        project_id = generate_id(file_names["projects_file"])
        project.append(project_id)

        # Append entry to file      
        append_new_entry_to_file(project, file_names["projects_file"], backup_file_names["backup_file_" + "projects_file"])

        # Ending the loop
        goOn = evaluate_loop("project")

def add_context():
    goOn = True
    
    while goOn:
        context = []

        #Name
        context.append(input("\n Name: \t").strip(' ').replace(",",";"))

        #Description
        context.append(input("\n Description: \t").strip(' ').replace(",",";"))

        # Append entry to file      
        append_new_entry_to_file(context, file_names["contexts_file"], backup_file_names["backup_file_" + "contexts_file"])

        # Ending the loop
        goOn = evaluate_loop("context")

def add_reminder():
    goOn = True
    
    while goOn:
        reminder = []

        #Description 0
        reminder.append(input("\n Description: \t").strip(' ').replace(",",";"))

        # date due 1
        reminder.append(filter_dates())

        # generate id
        reminder_id = generate_id(file_names["reminders_file"])
        action.append(reminder_id)

        # Append entry to file      
        append_new_entry_to_file(reminder, file_names["reminders_file"], backup_file_names["backup_file_" + "reminders_file"])

        # Ending the loop
        goOn = evaluate_loop("reminder")

def add_person():
    goOn = True
    
    while goOn:
        person = []

        #Description 0
        person.append(input("\n Name: \t").strip(' ').replace(",",";"))

        # contact_details
        person.append(input("\n Contact: \t").strip(' ').replace(",",";"))

        # Append entry to file      
        append_new_entry_to_file(person, file_names["people_file"], backup_file_names["backup_file_" + "people_file"])

        # Ending the loop
        goOn = evaluate_loop("contact")

def filter_file(value_searched, column, file_to_choose):
    #returns a filtered list from file
    filtered_list = []
    items = load_file(file_to_choose)
    for key in range(0,len(items)):
        if items[key][column] == value_searched:
            filtered_list.append(items[key])
    return filtered_list

def show_reminders():
    reminders = load_file(file_names["reminders_file"])
    for i in range(0, len(reminders)):
        print("Reminder: {}\t Date due: {}".format(reminders[i][0],reminders[i][1])) #should be sorted by date

def show_actions():
    projects = load_file(file_names["projects_file"])
    for i in range(0, len(projects)):
        project_actions = filter_file(projects[i][0],1,file_names["actions_file"])
        if project_actions != []:
            print("\n\tProject: " + projects[i][0] + "\n\n")
            for j in range(0, len(project_actions)):
                this_pa = project_actions[j]
                print("\t{}. {}\n\t\t* Context: {}\tState: {}, since: {}\n\t\t* Date due:{}\n\t\tID: {}".
                    format(j+1, this_pa[2], this_pa[3], this_pa[4], this_pa[5], this_pa[6],this_pa[-1]))
                if this_pa[-2] != "":
                    print("\t\tNotes: {}".format(this_pa[-2]))
                print("\n\t" + "-" * 80 + "\n")
        print("\n\t" + "=" * 80 + "\n")
    return

def choose_action_id():
    choice = input("Input id number or type n for actions\t")
    if choice == "n":
        show_projects()
        choice = input("Input id number")
          
    return choice

def do_action(action_id, actions):
    for i in range(0, len(actions)):
        if actions[i][-1] == action_id:
           actions[i][4] = "done"
    return actions

def write_file(file_name, data):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def archive_entry(entry):
    append_new_entry_to_file(entry, file_names["archives_file"], backup_file_names["backup_file_" + 'archives_file'])

def delete_action(action_id, to_archive):
    found = False
    found_action = []
    backup_file(file_names['actions_file'],backup_file_names["backup_file_" + 'actions_file'])
    actions = load_file(file_names['actions_file'])
    for i in range(0, len(actions)):
        if actions[i][-1] == action_id:
            found_action = actions.pop(i)
            found = True
            print(found_action)
            if to_archive:
                archive_entry(found_action)
            break
    if found:
        write_file(file_names['actions_file'], actions)
        backup_file(file_names['actions_file'],backup_file_names["backup_file_" + 'actions_file']) # perhaps that's a bit over the top

def edit_action():
    print(lame_excuse)

def argument_parser():
    myepilog = 'sp.py Copyright (C) 2014  Miguel de Luis Espinosa.\n This program comes with ABSOLUTELY NO WARRANTY. \n This is free software, and you are welcome to redistribute it under certain conditions'
    parser = argparse.ArgumentParser(description=' Simple personal poductivity app', epilog= myepilog)
    arguments = {"-aa":"add a new action", "-ap": "add a new project", "-ac":"add a new context", 
                 "-aP" : "add a new person", "-ar" : "add reminder",
                 "-sr" : "show reminders", "-sap": "show actions by project", "-da" : "set action as done",
                 "-wr" : "weekly review", "-fp": "file project", "-fa": "file action", 
                 "-ea" : "edit action", "-ep" : "edit project", "-dela": "delete action"}
   
    for key in arguments:
        parser.add_argument(key, action = 'store_true', help= arguments[key])
      
    args = parser.parse_args()

    lame_excuse = "sorry, not implemented yet"

    if args.aa:
        add_action()
    elif args.ap:
        add_project()
    elif args.ac:
        add_context()
    elif args.ar:
        add_reminder()
    elif args.sr:
        show_reminders()
    elif args.sap:
        show_actions()
    elif args.aP:
        add_person()
    elif args.da:
        actions = load_file(file_names["actions_file"])
        action_id = choose_action_id()
        write_file(file_names["actions_file"], do_action(action_id, actions))
        backup_file(file_names["actions_file"], backup_file_names["backup_file_"+ "actions_file"])
    elif args.wr:
        print(lame_excuse)
    elif args.fp:
        print(lame_excuse)
    elif args.fa:
        print(lame_excuse)
    elif args.ea:
        actions = load_file(file_names["actions_file"])
        action_id = choose_action_id()
    elif args.ep:
        print(lame_excuse)
    elif args.dela:
        a = delete_action("3", True) # for testing purposes
        b = delete_action("4", False)
    else:
        print(lame_excuse) 

argument_parser()

