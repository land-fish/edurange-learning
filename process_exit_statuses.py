#!/usr/bin/python
# This is a script for processing the exit status files from EDURange
# The input for this script is a script log file, or a list of script
# log files.

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

# Takes a list of lines
# Returns a list with lines and their exit statuses
def get_exit_status(lines):
    exit_list = []
    for i,line in enumerate(lines):
        if re.search("(\d\d:\d\d:\d\d)",line) and not re.search("(\d\d\d\d-\d\d-\d\d)",line):
            exit_list.append([re.split("(\d\d:\d\d:\d\d)",line)[2][1:],lines[i-1]])
    return exit_list


# main
if __name__ == '__main__':

    exit_lines = load_command_list('test_data/17_Exit_Status_Strace.txt')
    print "All lines:"
    print exit_lines

    print "\nSplit command lines:"
    exit_list = get_exit_status(exit_lines)
    for i in exit_list:
        print i
