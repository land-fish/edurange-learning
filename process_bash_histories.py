#!/usr/bin/python

import re

# reads through a list where values are separated by line breaks
# returns an array of strings
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
    
    

if __name__ == '__main__':
    commands = load_command_list('combined_bin_list')
    #print commands

    bash_commands = load_command_list('test_data/14_Statistic_Elf.txt')
    bash_lines = remove_analytics(bash_commands)
    list_of_commands = find_just_commands(bash_lines,commands)

    list_of_lines = find_legit_lines(bash_lines,commands)
    print list_of_lines

    
    final_count = count_bash_commands(list_of_commands)
    
    analytics = find_commands_and_args(bash_lines,commands)

    print analytics
    
    #print final_count
