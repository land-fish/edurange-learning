#!/usr/bin/python
# This is a script for processing the bash history files from EDURange
# Use the script like this:
#    ./process_bash_histories /path/to/bash_history_file

import re
import sys
import time

def load_command_list(file_path):
    """reads through a file where values are separated by line breaks
    returns a list of strings
    """
    f = open(file_path)
    command_list = []
    for line in f:
        command_list.append(line.replace('\n',''))
    f.close()
    return command_list

def remove_analytics(input_list):
    """Takes a list of bash history lines and outputs a list of those same
    lines, except without every entry after and including the line
    'Bash Analytics: '
    """
    output_list = []
    analytics_pos = len(input_list)
    for i,line in enumerate(input_list):
        if line == 'Bash Analytics: ':
            analytics_pos = i
        if i <= analytics_pos - 1:
            output_list.append(line)
    return output_list

def sort_by_user(input_list):
    """Takes a list of bash history lines without analytics
    Out puts a dict of lists. The first string in each list
    will be the user, and the all other lines will be bash
    History commands
    """
    usr_dct = {}
    #var to manage user in loop
    cur_usr = ""
    for line in input_list:
        if line[:2] == "##":
            if usr_dct.has_key('%s' % line[3:]):
                cur_usr = '%s' % line[3:] 
            else:
                usr_dct['%s' % line[3:]] = []
                cur_usr = '%s' % line[3:]
        else:
            if cur_usr is not "":
                usr_dct.get(cur_usr).append(line)
    return usr_dct 

def find_just_commands(bash_history_list,bin_list):
    """Takes a list of bash history lines and a list of linux commands
    Outputs a list of commands
    """
    final_list = []
    for line in bash_history_list:
        for word in line.split(' '):
            if word in bin_list:
                final_list.append(word)
    return final_list

def find_legit_lines(bash_history_list,bin_list):
    """Takes a list of bash history lines and a list of linux commands
    Outputs a list of lines that begin with proper commands
    """
    final_list = []
    for line in bash_history_list:
        if line.split(' ')[0] in bin_list:
            final_list.append(line)
    return final_list


def find_commands_and_args(bash_history_list,bin_list):
    """Takes a list of bash history lines and a list of linux commands
    Outputs a list of commands, which are themselves lists,
    with the first entry a command and the rest arguments
    """
    final_list = []
    for line in bash_history_list:
        for command in re.split("[\|;]",line):
            ll = command.split(' ')
            if ll[0] in bin_list:
                final_list.append(ll)
    return final_list

def count_bash_commands(command_list):
    """Takes a list of commands without arguments
    Returns a dict of commands with their counts
    """
    command_count = {}
    for i in command_list:
        command_count[i] = command_count.get(i,0) + 1 
    return command_count

def graph(command_frequency):
    """Takes a dict of commands and their frequency
    Out puts a simple ascii graph by frequency
    """
    graph_str = "" 
    for com_name,com_count in sorted(command_frequency.iteritems(), key=lambda (k,v): (v,k)):
        graph_str += com_name + ":" + (10 - len(com_name)) * " " + command_frequency.get(com_name) * '*' + "\n"
    return graph_str
  
def load(hist_file_path):
    """Takes the file path, and returns a list of bash history lines without
    the weird analytics stuff
    """
    input_file = hist_file_path
    bash_commands = load_command_list(input_file)
    bash_lines = remove_analytics(bash_commands)
    return bash_lines

def human_times(command_list):
    """Takes a list of bash history lines and returns the same list, except
    with times in a human readble format
    """
    readable_list = []
    for line in command_list:
        date_line = re.match('#\d\d\d\d\d\d\d\d\d\d',line)
        if date_line:
            timestamp = time.gmtime(int(date_line.group(0)[1:]))
            formatted_t = time.strftime("%H:%M:%S",timestamp)
            readable_list.append('# ' + formatted_t)
        else:
            readable_list.append(line)
    return readable_list

def file_or_output(command_list):
    """Test function which takes a list of commands and either writes a file or
    prints command output depending on user selection."""
    print("Please choose from the following options:\
            \n  1. Print commands used sorted by user\
            \n  2. Print ascii graph of all commands used\
            \n  3. Print ascii graph of commands by user\
            \n  4. Save a file of graphs by user\
            \n  5. Save seperate file of each user's bash history")
    response = input("Please type a number from 1 - 5 and press enter\n")
    if response == 1:
        #make a dictionary of 
        user_dict = sort_by_user(command_list)
        for i in user_dict.iterkeys():
            print "Bash history for user: %s" % i
            formatted_list = human_times(user_dict.get(i))
            for a in formatted_list:
                print a
    elif response == 2:
        commands = load_command_list('combined_bin_list') 
        list_of_commands = find_just_commands(command_list,commands) 
        final_count = count_bash_commands(list_of_commands)  
        print graph(final_count)
    elif response == 3: 
        commands = load_command_list('combined_bin_list') 
        #make a dictionary of each user, command list
        user_dict = sort_by_user(command_list)
        for i in user_dict.iterkeys():
            print "Command Graph for user: " + str(i) 
            list_of_commands = find_just_commands(user_dict.get(i),commands) 
            final_count = count_bash_commands(list_of_commands)  
            print graph(final_count)
    elif response == 4:  
        commands = load_command_list('combined_bin_list') 
        #make a dictionary of each user, command list
        user_dict = sort_by_user(command_list)
        to_write = ""
        for i in user_dict.iterkeys():
            to_write += "Command Graph for user: " + str(i) + "\n"
            list_of_commands = find_just_commands(user_dict.get(i),commands) 
            final_count = count_bash_commands(list_of_commands)   
            to_write += graph(final_count)
        #write graph to the file the user specifies
        filename = raw_input("Please enter the name of the output file\n")
        filename_string = str(filename)
        f = open(filename_string,'w')
        f.write(to_write)
        f.close
    elif response == 5:
        commands = load_command_list('combined_bin_list') 
        user_dict = sort_by_user(command_list)
        name_prefix = ""
        name_prefix = raw_input("If you would like a prefix in a scenario name,\
                 \nlike recon_4_march, type the prefix and press enter.\
                 \nYour files will be saved as [prefix]_[user].txt\n")
        for user in user_dict.iterkeys():
            bash_lines = user_dict.get(user)
            to_write = "Bash history of user: " + user + "\n"
            formatted_lines = human_times(bash_lines)   # Change from unix timestamp to human readable one
            for i in formatted_lines:
                to_write += i + "\n"
            filename = name_prefix + "_" + user + '.txt'
            f = open(filename,'w')
            f.write(to_write)
            f.close 
    else:
        print("\nNot a recognized option\n") 
        time.sleep(2)
        file_or_output(command_list)

if __name__ == '__main__':   

    #Note: The file 'combined_bin_list' must exist in the same directory as this script
    if len(sys.argv) < 2:
        print("The process bash history script has the following syntax:\
        \n  ./process_bash_histories /path/to/history_file\
        \n  or\
        \n  python process_bash_histories /path/to/history_file")
    elif len(sys.argv) > 2:
        print("When you provide multiple bash history files, this script \
        \nwill cat them together and treat them as one bash history. This \
        \ncan be useful to see activity on a per user or per machine basis \
        \nbut comparisons between files must currently be done independently.")    
        bash_lines = []
        for i in range(len(sys.argv)):
            hist_file = load(str(sys.argv[i]))
            bash_lines += hist_file 
        file_or_output(bash_lines)
    #When there is exactly one argument given
    else:
        hist_file_path = str(sys.argv[1])
        bash_lines = load(hist_file_path)  
        file_or_output(bash_lines) 
