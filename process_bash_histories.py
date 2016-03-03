#!/usr/bin/python
# This is a script for processing the bash history files from EDURange
# Use the script like this:
#    ./process_bash_histories /path/to/bash_history_file


import re
import sys

# reads through a file where values are separated by line breaks
# returns a list of strings
def load_command_list(file_path):
    f = open(file_path)
    command_list = []
    for line in f:
        command_list.append(line.replace('\n',''))
    f.close()
    return command_list

# Takes a list of bash history lines and outputs a list of those same
# lines, except without every entry after and including the line
# 'Bash Analytics: '
def remove_analytics(input_list):
    output_list = []
    analytics_pos = len(input_list)
    for i,line in enumerate(input_list):
        if line == 'Bash Analytics: ':
            analytics_pos = i
        if i <= analytics_pos - 1:
            output_list.append(line)
    return output_list

# Takes a list of bash history lines without analytics
# Out puts a dict of lists. The first string in each list
# will be the user, and the all other lines will be bash
# History commands
def sort_by_user(input_list):
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

# Takes a list of bash history lines and a list of linux commands
# Outputs a list of commands
def find_just_commands(bash_history_list,bin_list):
    final_list = []
    for line in bash_history_list:
        for word in line.split(' '):
            if word in bin_list:
                final_list.append(word)
    return final_list

# Takes a list of bash history lines and a list of linux commands
# Outputs a list of lines that begin with proper commands
def find_legit_lines(bash_history_list,bin_list):
    final_list = []
    for line in bash_history_list:
        if line.split(' ')[0] in bin_list:
            final_list.append(line)
    return final_list


# Takes a list of bash history lines and a list of linux commands
# Outputs a list of commands, which are themselves lists,
# with the first entry a command and the rest arguments
def find_commands_and_args(bash_history_list,bin_list):
    final_list = []
    for line in bash_history_list:
        for command in re.split("[\|;]",line):
            ll = command.split(' ')
            if ll[0] in bin_list:
                final_list.append(ll)
    return final_list

# Takes a list of commands without arguments
# Returns a dict of commands with their counts
def count_bash_commands(command_list):
    command_count = {}
    for i in command_list:
        command_count[i] = command_count.get(i,0) + 1
    
    return command_count

# Takes a dict of commands and their frequency
# Out puts a simple ascii graph by frequency
def graph(command_frequency):
    graph_str = "" 
    for com_name,com_count in sorted(command_frequency.iteritems(), key=lambda (k,v): (v,k)):
        graph_str += com_name + ":" + (10 - len(com_name)) * " " + command_frequency.get(com_name) * '*' + "\n"
    return graph_str
  
# Takes the file path, and returns a list of bash history lines without
# the weird analytics stuff
def load(hist_file_path):
    input_file = hist_file_path
    bash_commands = load_command_list(input_file)
    bash_lines = remove_analytics(bash_commands)
    return bash_lines

if __name__ == '__main__':

    #The file 'combined_bin_list' must exist in the same directory as this script
    hist_file_path = str(sys.argv[1])
    bash_lines = load(hist_file_path)   
    
    #make a dictionary of 
    user_dict = sort_by_user(bash_lines)
  
    for i in user_dict.iterkeys():
        print "Bash history for user: %s" % i
        for a in user_dict.get(i):
            print a
    

    commands = load_command_list('combined_bin_list') 
    list_of_commands = find_just_commands(bash_lines,commands) 
    final_count = count_bash_commands(list_of_commands)  
    print graph(final_count)
   #This script is a work in progress, please ignore the content below
    """
    list_of_lines = find_legit_lines(bash_lines,commands)
    print "List of bash commands: "
    print list_of_lines
    print " " 
    analytics = find_commands_and_args(bash_lines,commands) 
    print "List of lists: commands and thier arguments"
    for a_list in analytics:
        print a_list
    print " " 
    print "Count of commands used: "
    for counts in final_count:
        print counts + ": " + str(final_count.get(counts))
    print "\nCool chart of commands used:"
    """
