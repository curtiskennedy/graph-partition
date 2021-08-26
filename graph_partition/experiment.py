from __future__ import print_function, unicode_literals

import os
import time
import csv

from collections import defaultdict
from PyInquirer import style_from_dict, Token, prompt
from pyfiglet import Figlet
from graph_partition import readInstance, checkAll, approx1, approx2, approx3, approx4, approx5, approx6, approx7, approx8


def experiment():
    exp1()



def exp1():
    f = Figlet(font='slant')
    print(f.renderText("graph-partition"))
    print("Running experiment...")
    # paths = {}
    # runPath = os.getcwd()
    # with open('ap6Testing.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for subdir, dirs, files in os.walk(runPath):
    #         for file in files:
    #             if file.endswith(".in"):
    #                 filePath = subdir[len(runPath):]
    #                 if filePath == '':
    #                     paths[file] = file
    #                 else:
    #                     paths[file] = filePath[1:]+'/'+file
    #                 grf = readInstance(paths[file])
    #                 # if len(grf.getBicomponents()) == 2:
    #                 if grf.is2Connected():
    #                     print(file)
    #                     # V1, V2, V3 = approx6(grf)
    #                     # writer.writerow([file, V1.weight(), V2.weight(), V3.weight()])