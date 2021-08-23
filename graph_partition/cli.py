from __future__ import print_function, unicode_literals

import os
import time
import csv

from collections import defaultdict
from PyInquirer import style_from_dict, Token, prompt
from prompt_toolkit.terminal.vt100_output import Vt100_Output
from pyfiglet import Figlet
from graph_partition import readInstance, checkAll, approx1, approx2, approx3, approx4, approx5, approx6, approx7, approx8


def experiment():
    print("Loading CLI...")
    f = Figlet(font='slant')
    print(f.renderText("graph-partition"))


def guided():
    print("Loading CLI...")
    instances = set()
    levels = defaultdict(set)
    runPath = os.getcwd()
    for subdir, dirs, files in os.walk(runPath):
        for file in files:
            if file.endswith(".in"):
                instances.add(file)
                filePath = subdir[len(runPath):]
                if not filePath.startswith("/"):
                    filePath = filePath
                levels[filePath].add(file)
                l = filePath.split("/")
                if len(l) > 1:
                    for i in range(len(l)-1, 0, -1):
                        if l[i] != '':
                            addTo = "/".join(l[:i])
                            # print("adding", "/"+l[i], "to", addTo)
                            levels[addTo].add("/"+l[i])

                        
    f = Figlet(font='slant')
    print(f.renderText("graph-partition"))

    style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
    })

    done = False
    choice = ""
    stack = []
    while not done:
        while not done:
            sortedList = sorted(levels[choice])
            sortedList.append("-BACK-")
            sortedList.append("-EXIT-")
            questions = [
            {
                'type': 'list',
                'name': 'result',
                'message': 'Please select an instance file',
                'choices': sortedList
            }]

            try:
                answers = prompt(questions, style=style)
            except:
                print("\nCould not find any .in files in this directory or sub-directories\n")
                raise SystemExit
            result = answers['result']
            if result == "-BACK-":
                if stack == []:
                    stack = [""]
                choice = stack.pop()
            elif result == "-EXIT-":
                print("Goodbye")
                raise SystemExit
            elif result.endswith(".in") and result in instances:
                name = choice + "/" + result
                name = name[1:]
                done = True
            else:
                stack.append(choice)
                choice += result
            


        print("Opening {} located at {}".format(result, "/"+name[:len(name)-len(result)]))
        graph = readInstance(name)
        goalWeight = graph.weight()
        print("="*len("Graph statistics for {}:".format(result)))
        print("Graph statistics for {}:".format(result))
        print("        # of nodes = {}".format(len(graph.nodes)))
        print("      Total weight = {}".format(goalWeight))
        print("      Is connected = {}".format(graph.isConnected()))
        print("    Is 2-conencted = {}".format(graph.is2Connected()))
        print(" # of bicomponents = {}".format(len(graph.getBicomponents())))
        print("="*len("Graph statistics for {}:".format(result)))
        

        options = sorted(checkAll(graph))
        options.append("-BACK-")
        options.append("-EXIT-")

        questions = [
        {
        'type': 'list',
        'name': 'algo',
        'message': 'Select an algorithm to run',
        'choices': options
        }]
        answers = prompt(questions, style=style)
        if answers['algo'] == "-EXIT-":
            print("Goodbye")
            raise SystemExit
        elif answers['algo'] == "-BACK-":
            # Go back to file explorer
            done = False

    if answers['algo'] == "Approx-1 for MAX-MIN k=2 (recommended)":
        print("Running Approx-1 ...")
        algo = approx1
        k=2
    elif answers['algo'] == "Approx-2 for MAX-MIN k=2":
        print("Running Approx-2 ...")
        algo = approx2
        k=2
    elif answers['algo'] == "Approx-3 for MIN-MAX k=3 (recommended)":
        print("Running Approx-3 ...")
        algo = approx3
        k=3
    elif answers['algo'] == "Approx-4 for MIN-MAX k=3":
        print("Running Approx-4 ...")
        algo = approx4
        k=3
    elif answers['algo'] == "Approx-5 for MIN-MAX k=3":
        print("Running Approx-5 ...")
        algo = approx5
        k=3
    elif answers['algo'] == "Approx-6 for MAX-MIN k=3 (recommended)":
        print("Running Approx-6 ...")
        algo = approx6
        k=3
    elif answers['algo'] == "Approx-7 for MAX-MIN k=3":
        print("Running Approx-7 ...")
        algo = approx7
        k=3
    elif answers['algo'] == "Approx-8 for MAX-MIN k=3":
        print("Running Approx-8 ...")
        algo = approx8
        k=3

    if k==2:
        start = time.time()
        V1, V2 = algo(graph)
        end = time.time()
        V1_weight = V1.weight()
        V2_weight = V2.weight()
        if V1_weight > V2_weight:
            V1, V2 = V2, V1
            V1_weight, V2_weight = V2_weight, V1_weight

    elif k==3:
        start = time.time()
        V1, V2, V3 = algo(graph)
        end = time.time()

        V1_weight = V1.weight()
        V2_weight = V2.weight()
        V3_weight = V3.weight()
        min_weight = min(V1_weight,V2_weight,V3_weight)
        max_weight = max(V1_weight,V2_weight,V3_weight)
        if min_weight == V2_weight:
            V1, V2 = V2, V1
            V1_weight, V2_weight = V2_weight, V1_weight

        if max_weight == V2_weight:
            V2, V3 = V3, V2
            V2_weight, V3_weight = V3_weight, V2_weight

        if min_weight == V3_weight or max_weight == V1_weight:
            V1, V3 = V3, V1
            V1_weight, V3_weight = V3_weight, V1_weight




    string = "Instance name = {}".format(result)
    print("\n"+ "="*len(string))
    print(string)
    print("   Time taken =", end-start, "seconds")
    print("    V1 weight =", V1_weight)
    print("    V2 weight =", V2_weight)
    if k == 3:
        print("    V3 weight =", V3_weight)
    print("="*len(string))

    if k==3:
        if V1_weight + V2_weight + V3_weight != goalWeight:
            print("ERROR - weights of partitions don't add up!")
        elif not (V1.isConnected() and V2.isConnected() and V3.isConnected()):
            print("ERROR - partition is not connected")
        else:
            print("Partition checked!")
    if k==2:
        if V1_weight + V2_weight != goalWeight:
            print("ERROR - weights of partitions don't add up!")
        elif not (V1.isConnected() and V2.isConnected()):
            print("ERROR - partition is not connected")
        else:
            print("Partition checked!")
        
