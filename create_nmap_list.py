#!/usr/bin/python


def generate_bash_statistics(f, relevant_commands):
    bash_file = f
    command_list = []

    # For building a list of command options that have been used
    option_dict = {}

    for line in bash_file:
        if len(line) > 1:
            # seek out nmap command from bash history
            if line.split()[0] in relevant_commands:
                # and add the command w/its args to a list
                command_list.append(line)

    multi_command_list = ["--min-rate", "--host-timeout", "--max-retries",
        "-iL","-iR","exclude","excludefile"]

    # take out anything after a >> operator
    command_list = map(lambda c: c.split(),
                       [command[:command.find('>>')] if '>>' in command
                        else command[:command.find('>')]
                        for command in command_list])

    for command in command_list:
        for i, option in enumerate(command[1:]):
            if option in multi_command_list:
                option = option + " " + command[i + 1]
            if option in option_dict:
                option_dict[option] = option_dict.get(option) + 1
            else:
                option_dict[option] = 1

    sorted_list = sorted([[option_dict.get(i), i]
                          for i in option_dict], reverse=True)

    for i in sorted_list:
        print i


if __name__ == '__main__':
    f = open('recon-jeff-isaak-07-10-2015')
    generate_bash_statistics(f, ["nmap"])
    f.close()
