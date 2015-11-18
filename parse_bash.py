#!/usr/bin/python

''' draw a graph for each file/student
  for each student, create a list of cmds
  for each cmd, create a dictionary of options
'''

from cmd import *

options = ['-T4', '-T5', '-sT', '-sP', '-sn', '-sS', '-v', '-A', '-O', '-n', '-sV']

commands = ['nmap', 'sudo', 'ls', 'man', 'cd', 'grep', 'ping', 'cat']

dir = '/home/landfish/coding/edurange-learning/test_data'
in_filename = '22_Statistic_Elf.txt'
out_filename = 'cmds_team'

def main():
    ## read input file  ##
    #filename = input("enter filename ");
    #for i in range(1,7):
        
        #infile = open(dir + '/' + in_filename + str(i), 'r')
        #outfile = open(dir + '/' + out_filename + str(i) + '.dot', 'w')
        infile = open(dir + '/' + in_filename, 'r')
        outfile = open(dir + '/' + out_filename + '.dot', 'w')
        process_files(infile, outfile)
        infile.close()
        outfile.close()


def process_files(infile, outfile):
    lines = infile.readlines()
    listCommands = []

    for l in lines:
        #print(l)
        toks = l.split()
        if 'nmap' in toks:
            print (toks)
            listCommands.append(check_options(toks))
            # convert to a set
            # listCommands.append(Cmd('nmap'))
        else:
            for c in commands:
                if c in toks:
                    listCommands.append(c)
                    break
    print('-------------')
    for c in listCommands:
        print (c)
    make_dot_file(outfile, listCommands)
    
    

def check_options(tokens):
    # test if opt in line/toks
    result = '"nmap'
    for o in options:
        if o in tokens:
            result = result + " " + o + " "
    # join(result)
    result = result + '"'
    return result

def make_dot_file(file, cmds):
    lines = ["digraph G { \n"]
    ## handle the first command 
    c = cmds[0]
    lines.append(c)

    for i in range(1,len(cmds)):
        c = cmds[i]
        lines.append(" -> " + c)

    lines.append("\n } \n")
    file.writelines(lines)

main()
