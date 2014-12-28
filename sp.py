import os, csv, shutil, time, argparse, collections
from datetime import datetime, date

file_names = {"people_file":"people.csv","projects_file":"p.csv",
              "actions_file":"a.csv","contexts_file":"contexts.csv",
              "reminders_file":"r.csv", "archives_file":"archives.csv",
              "last_id_file":"id.csv", "trash_file":"trash.csv", "settings_file":"s.csv"}

arguments = {"-aa":"add a new action", "-ap": "add a new project", "-ac":"add a new context", 
                 "-aP" : "add a new person", "-ar" : "add reminder",
                 "-sr" : "show reminders", "-sa": "show actions by project", "-da" : "set action as done",
                 "-wr" : "weekly review", "-fp": "file project and its actions", "-fa": "file action", 
                 "-ea" : "edit action", "-ep" : "edit project", "-dela": "delete action",
                 "-delp" : "delete project and its actions", "-sp":"show projects"}

settings_file = file_names["settings_file"]

backup_directory = '../sppy/bu' # move to settings

temporary_backup_directory = '/tmp'

if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

if not os.path.exists(backup_directory + temporary_backup_directory):
    os.makedirs(backup_directory + temporary_backup_directory)

states = {"t":"to do", "x":"done", "d": "delegated to", "w": "waiting for"}

lame_excuse = "sorry, not implemented yet"

def generate_id():
    last_id = load_file("id.csv")
    try:
        new_id = int(last_id[0][0]) + 1
    except:
        new_id = 0
    new_id = str(new_id)
    write_file("id.csv", new_id)
    return new_id

def generate_backup_file_names(backup_directory,file_names):
    backup_file_names = {}
    backup_common_file_name_part = backup_directory + "/" + "backup_"
    for key in file_names:
        backup_file_names["backup_file_" + key] = backup_common_file_name_part + file_names[key]
    return backup_file_names

def generate_files(file_names):
    for key in file_names:
        f= open(file_names[key], 'a', newline='')
        f.close

def load_default_settings(settings_file):
    generate_files(file_names)
    generate_files(backup_file_names)
    settings = load_file(settings_file)
    contexts = load_file(file_names["contexts_file"])
    actions = load_file(file_names["actions_file"])
    projects = load_file(file_names["projects_file"])
    reminders = load_file(file_names["reminders_file"])
    people = load_file(file_names["people_file"])
    if len(projects) == 0:
        default_projects_data=",,,,"
        projects = settings[1]
        projects_headers = settings[6]
        append_file(file_names["projects_file"], projects_headers)
        for i in range(0, len(projects)):
            with open(file_names["projects_file"], 'a') as g:
                g.write(projects[i] + default_projects_data + "pd" + str(i) + "\n")
    if len(actions) == 0:            
        actions_headers = settings[2]
        append_file(file_names["actions_file"], actions_headers)
    if len(contexts) == 0:
        contexts = settings[0]
        contexts_headers = settings[3]
        append_file(file_names["contexts_file"],contexts_headers)
        default_contexts_data=",,"
        for i in range(0, len(contexts)):
            with open(file_names["contexts_file"], 'a') as f:
                f.write(contexts[i]+ default_contexts_data + "cd" + str(i) + "\n")
    if len(reminders) == 0:
        reminders_headers = settings[4]
        append_file(file_names["reminders_file"], reminders_headers)
    if len(people) == 0:
        people_headers = settings[5]
        append_file(file_names["people_file"], people_headers)

def load_file(file_to_load): #loads a csv file as a list
    csv_file_as_list = []
    with open(file_to_load, newline='') as f:
            csv_file_as_list = []
            reader = csv.reader(f)
            for row in reader:
                csv_file_as_list.append(row)
    
    f.close()        
    return csv_file_as_list

def filter_dates(thing):
    day = ""
    month = ""
    year = ""
    hour = "0"
    minute = "0"
    
    while len(day) == 0 or int(day) < 1 or int(day) > 31:
        day = input("\n Day (dd): \t").strip(', ')

    while len(month) == 0 or int(month) <1 or int(month) > 12:
        month = input("\n Month (mm): \t").strip(', ')
        
    while len(year) == 0 or int(year) < 2013 or int(year) > 2114:
        year = input("\n Year (mm): \t").strip(', ')

    add_hour = input("Does this {} must be accomplished before a certain hour? Type y for 'yes'\t".format(thing))
    if add_hour == "y":
        while len(hour) == 0 or int(hour) > 24 or int(hour) < 1:
            hour = input("\n Hour (24): \t").strip(', ')
        while len(minute) == 0 or int(minute) > 60 or int(minute) < 1:
            minute = input("\n Minute: \t").strip(', ')  

    return "{}-{}-{} {}:{}".format(year,month,day,hour,minute)

def make_dictionary_from_list(file_as_list):
    dictionary_from_list = {}
    for i in range(1, len(file_as_list)):
        dictionary_from_list[str(i)] = file_as_list[i][0]
    return dictionary_from_list

def choose_in_dictionary(args):
    #returns a list containing the chosen key and the object referenced by the key
    chosen_dict = []
    print("\n")
    for key in sorted(args):
        print("\t* {}   \t{}".format(key, args[key]))

    menu = input("\n\tEnter your choice\t")

    if menu not in args:
        choose_in_dictionary(args)
    else:
        chosen_dict.append(menu)
        chosen_dict.append(args[menu])
        return chosen_dict

def choose_in_file(file_to_choose):

    file_as_dictionary = make_dictionary_from_list(load_file(file_to_choose))

    return choose_in_dictionary(file_as_dictionary)

def append_file(file_name, entry):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(entry)

def backup_file(work_file, backup_file_name):
    # copy work back up file to a new time-stamped backup file
    temporal_backup_file = backup_file_name[:10] + temporary_backup_directory + backup_file_name[10:-4] + time.strftime("%d_%m_%Y_at_%H_%M")+ '.csv'
    shutil.copy2(work_file,temporal_backup_file)
    
    # append to work backup file    
    shutil.copy2(work_file,backup_file_name)

def append_new_entry_to_file(entry, work_file, backup_file_name): 
        
    # add entries to file
    append_file(work_file,entry)

    backup_file(work_file, backup_file_name)
    
def evaluate_loop(thing):
    answer = input("\n Another {} (n for no)\t".format(thing))
    evaluation = True
    if answer != "":
        if answer[0].lower() == "n":
            evaluation = False
    return evaluation

def add_deadline(thing):
    deadline = input("\n Is this {} under a deadline? Press 'y' to add one\t".format(thing))
    if deadline == "y":
        return filter_dates(thing)
    else:
        return ""

def add_action():
    goOn = True
    
    while goOn:
        
        # Entry -  date gathered 0 , Project 1 , description 2 , context 3 , state 4 , date due 5 , person 6 , order 7 , notes 8
        action = [] 
                
        #Date Gathered  0
        action.append(datetime.today())
        #Project 1
        print("Project this action belongs to")
        project_chosen = choose_in_file(file_names["projects_file"])
        action.append(project_chosen.pop())       
        #Description 2
        action.append(input("\n Short Description: \t").strip(' ').replace(",",";")) # commas replaced with semicolons.
        # Context 3
        print("Context of this action")        
        action.append(choose_in_file(file_names["contexts_file"]).pop())
        # State 4
        print("State")
        action.append(choose_in_dictionary(states)[0]) # I want the key in states
        # State Modified date 5
        action.append(datetime.today())
        # date due 6
        action.append(add_deadline("action"))
        # person 7
        if action[4] == "w" or action[4] == "d":
            print("\t Person associated with this action:\n")
            action.append(choose_in_file(file_names["people_file"]).pop())
        else:
            action.append("")
        # Notes 8
        action.append(input("\n Write a note if needed: \t").strip(' ').replace(",","."))     
        # id 9
        action_id = "a" + generate_id()
        action.append(action_id)
        # Append action to file      
        append_new_entry_to_file(action, file_names["actions_file"], backup_file_names["backup_file_" + "actions_file"])

        #offer to add reminder?
        #autor_reminder() ?

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
        project.append(datetime.today())
        # date due 2
        project.append(add_deadline("project"))        
        # Notes 3
        project.append(input("\n Write a note if needed: \t").strip(' ').replace(",","."))
        # Id 4
        project_id = "p" + generate_id()
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
        #Id
        context_id = "c" + generate_id()
        context.append(context_id)
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
        action.append(add_deadline("reminder"))

        # generate id
        reminder_id = "r" + generate_id()
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
        person.append(input("\n Contact data: \t").strip(' ').replace(",",";"))
        
        # id
        person_id = "person" + generate_id()
        person.append(person_id)

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

def show_projects():
    projects = load_file(file_names["projects_file"])
    for i in range(0, len(projects)):
        project_actions = filter_file(projects[i][0],1,file_names["actions_file"])
        number_actions = len(project_actions)
        done_actions = 0
        print("\n\tProject: " + projects[i][0])
        print("\n\tId: {}\tDate due: {}\n".format(projects[i][-1], projects[i][2]))
        for j in range(0, len(project_actions)):
            this_pa = project_actions[j]
            if this_pa[4] == "x":
                done_actions += 1
        print("\n\tActions: {}\tDone: {}".format(number_actions, done_actions))
        print("\n\t" + "=" * 80 + "\n")
    return

def choose_id(thing):
    choice = input("\n\tEnter id or type s to show {}\t".format(thing))
    if choice == "s":
        if thing == "action":
            show_actions()
        else:
            show_projects()
        choice = input("Enter id\t")
    return choice

def do_action(action_id, actions):
    for i in range(0, len(actions)):
        if actions[i][-1] == action_id:
           actions[i][4] = "x"
    return actions

def write_file(file_name, data):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def archive_entry(entry):
    append_new_entry_to_file(entry, file_names["archives_file"], backup_file_names["backup_file_" + 'archives_file'])

def trash_file(entry):
    append_new_entry_to_file(entry, file_names["trash_file"], backup_file_names["backup_file_" + 'trash_file'])

def delete_action(action_id, to_archive):
    found = False
    found_action = []
    backup_file(file_names['actions_file'],backup_file_names["backup_file_" + 'actions_file'])
    actions = load_file(file_names['actions_file'])
    print(actions)
    for i in range(0, len(actions)):
        if actions[i][-1] == action_id:
            found_action = actions.pop(i)
            found = True
            if to_archive:
                archive_entry(found_action)
            else:
                trash_file(found_action)
            break
    if found:
        write_file(file_names['actions_file'], actions)
        backup_file(file_names['actions_file'],backup_file_names["backup_file_" + 'actions_file']) # perhaps that's a bit over the top
        return found_action

def delete_project(project_id, to_archive):
    found = False
    found_project = []
    backup_file(file_names['projects_file'],backup_file_names["backup_file_" + 'projects_file'])
    projects = load_file(file_names['projects_file'])
    for i in range(0, len(projects)):
        if projects[i][-1] == project_id:
            found_project = projects.pop(i)
            found = True
            if to_archive:
                archive_entry(found_project)
            else:
                trash_file(found_project)
            break
    if found:
        write_file(file_names['projects_file'], projects)
        backup_file(file_names['projects_file'],backup_file_names["backup_file_" + 'projects_file']) # perhaps that's a bit over the top
        return found_project

def edit_action(action_id):
    # get action
    actions = load_file(file_names["actions_file"])
    action_to_edit = ""
    for i in range(0, len(actions)):
        if actions[i][-1] == action_id:
            action_to_edit = actions.pop(i)
            break
    # display edit menu
    print(action_to_edit)
    column = input("Choose column to edit:\t")
    data = input("Introduce new data")
    # change data
    action_to_edit[int(column)] = data
    # save and backup
    write_file(file_names['actions_file'], actions)
    append_new_entry_to_file(action_to_edit, file_names["actions_file"], backup_file_names["backup_file_actions_file"])

def gather_project_actions(project_id):
    all_actions = load_file(file_names["actions_file"])
    projects = load_file(file_names["projects_file"])
    project_actions_ids = []
    for i in range(0, len(projects)):
        if projects[i][-1] == project_id:
            project_description = projects[i][0]
    for i in range(0, len(all_actions)):
        if all_actions[i][1] == project_description:
            project_actions_ids.append(all_actions[i][-1])
    return project_actions_ids

def delete_project_actions(project_actions_ids, tofile):
    for i in range(0, len(project_actions_ids)):
        delete_action(project_actions_ids[i],tofile)

def file_project(project_id):
    project_actions_ids = gather_project_actions(project_id)
    print(project_actions_ids)
    delete_project_actions(project_actions_ids, True)
    project_filed = delete_project(project_id, True)
    print("{} filed".format(project_filed))

def weekly_review():
    print(lame_excuse)

def file_action():
    action_id = choose_id("action")   
    deleted_action = delete_action(action_id, True)
    print("Action filed: \n{}".format(deleted_action))

def choose_and_do_action():
    actions = load_file(file_names["actions_file"])
    action_id = choose_id("action")
    write_file(file_names["actions_file"], do_action(action_id, actions))
    backup_file(file_names["actions_file"], backup_file_names["backup_file_"+ "actions_file"])

def choose_and_file_project():
    project_id = choose_id("project")
    file_project(project_id)

def choose_and_edit_action():
    action_id = choose_id("action")
    edit_action(action_id)

def update_list(value_searched, column_to_search, column_to_edit, datum, list_to_update):
    for i in range(0, len(list_to_update)):
        if value_searched == list_to_update[i][column_to_search]:
            list_to_update[i][column_to_edit] = datum
    return list_to_update

def edit_project(project_id):
    # get project
    projects = load_file(file_names["projects_file"])
    project_to_edit = ""
    for i in range(0, len(projects)):
        if projects[i][-1] == project_id:
            project_to_edit = projects.pop(i)
            break
    # display edit menu
    print(project_to_edit)
    column = input("Choose column to edit:\t")
    datum = input("Introduce new data")
    # change data
    project_to_edit[int(column)] = datum
    if column == "0": #changing the name of a project
        project_actions_ids = gather_project_actions(project_id)
        actions_list = load_file(file_names["actions_file"])
        for i in project_actions_ids:
            updated_actions = update_list(i, -1, 1, datum, actions_list)
        write_file(file_names['actions_file'], updated_actions)
        backup_file(file_names['actions_file'], backup_file_names["backup_file_actions_file"])
    # save and backup
    write_file(file_names['projects_file'], projects)
    append_new_entry_to_file(project_to_edit, file_names["projects_file"], backup_file_names["backup_file_projects_file"])

def choose_and_edit_project():
    project_id = choose_id("project")
    edit_project(project_id)

def choose_and_delete_action():
    action_id = choose_id("action")
    deleted_action = delete_action(action_id, False)
    print("Action deleted: \n{}".format(deleted_action))

def choose_and_delete_project():
    project_id = choose_id("project")
    project_actions_ids = gather_project_actions(project_id)
    print(project_actions_ids)
    delete_project_actions(project_actions_ids, False)
    project_filed = delete_project(project_id, False)
    print("{} deleted".format(project_filed))

def show_menu():
    choice = choose_in_dictionary(arguments)
    print("\n\tYou have chosen to {}".format(arguments[choice]))
    evaluate_menu(choice[1:])

def evaluate_menu(choice):
    print("choice {}".format(choice))
    arguments_as_funtion_names[choice]()
    show_menu()

arguments = {"-aa":"add a new action", "-ap": "add a new project", "-ac":"add a new context", 
                 "-aP" : "add a new person", "-ar" : "add reminder",
                 "-sr" : "show reminders", "-sa": "show actions by project", "-doa" : "set an action as done",
                 "-wr" : "do a weekly review", "-fp": "file project and its actions", "-fa": "file action", 
                 "-ea" : "edit action", "-ep" : "edit project", "-dela": "delete action",
                 "-delp" : "delete project and its actions", "-sp":"show projects",
                 "-im" : "show interactive menu", "-quit":"exit application, useful in interactive mode"}

arguments_as_funtion_names = {"aa":add_action, "ap":add_project, "ac":add_context,
                              "aP":add_person, "ar":add_reminder,
                              "sr":show_reminders, "sa":show_actions, "doa":choose_and_do_action,
                              "wr":weekly_review, "fp":choose_and_file_project, "fa":file_action,
                              "ea":edit_action, "ep":choose_and_edit_project, "dela":choose_and_delete_action,
                              "delp":choose_and_delete_project, "sp":show_projects, "im":show_menu, "quit":quit}

def evaluate_arguments(args):
    dict_args = vars(args)
    found_argument = False
    for key in dict_args:
        if dict_args[key]:
            arguments_as_funtion_names[key]()
            found_argument = True
            break
    if not found_argument:
        show_menu()

def argument_parser(arguments):
    myepilog = 'sp.py Copyright (C) 2014  Miguel de Luis Espinosa.\n This program comes with ABSOLUTELY NO WARRANTY. \n This is free software, and you are welcome to redistribute it under certain conditions'
    parser = argparse.ArgumentParser(description=' Simple personal poductivity app', epilog= myepilog)
    for key in arguments:
        parser.add_argument(key, action = 'store_true', help= arguments[key])
      
    args = parser.parse_args()
    evaluate_arguments(args)

backup_file_names = generate_backup_file_names(backup_directory, file_names)
load_default_settings(settings_file)
argument_parser(arguments)
