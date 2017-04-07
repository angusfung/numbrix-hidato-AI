from numbrix_reg_csp import * 
from test_case_hidato import *
from test_case_numbrix import *
from propagators2 import *
import ast, sys
import os


def print_numbrix_soln(var_array):

    if isinstance(var_array[0],list) == True:
        for i in range(len((var_array))):
            for j in range(len(var_array[0])):
                if var_array[i][j] != 0:
                    print("{:>3}".format(str(var_array[i][j].get_assigned_value())), end = '')
                else:
                    print("{:>3}".format(str('X')), end = '')
            print('')
    else:
        for i in range(len(var_array)):
            if var_array[i] != 0:
                print("{:>3}".format(str(var_array[i].get_assigned_value())), end = '')
            else:
                print("{:>3}".format(str('X')), end = '')
        print('')
        

if __name__ == "__main__":

    for b in [a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11]: #Numbrix Test Cases from 3x3 to 10x10
    #for b in [c0,c1,c2,c3,c4,c5,c6,c7]: #Testing the Ability to Handle 3x3 to 6x6 Hidato
    #for b in [hidsq1,hidsq2,hidsq3,hidsq4,hidsq5,hidsq6]: #Official Hidato Puzzles
    #for b in [hid1,hid2,hid3,hid4,hid5,hid6,hid7,hid8,hid9,hid10,hid11]: #Hidato with Obstacles
        print("Solving Numbrix/Hidato Puzzle:")


        print("Using Model to solve Numbrix/Hidato: ")
        start_time = os.times()[0]
        csp, var_array = numbrix_model_1(b)
        solver = BT(csp)
        print("===============================================================")
        start_solver = os.times()[0]
        print("The total set up time taken is: ",start_solver - start_time," seconds")
        print("---------------------------------------------------------------")
        print("FC")
        solver.bt_search(prop_FC)
        end_time = os.times()[0]
        print("The FC time taken is: ",end_time - start_solver," seconds")
        print("---------------------------------------------------------------")
        print("GAC")
        start_solver = os.times()[0]
        solver.bt_search(prop_GAC)
        end_time = os.times()[0]
        print("The GAC time taken is: ",end_time - start_solver," seconds")
        print("---------------------------------------------------------------")
        print("Solution: ")
        print_numbrix_soln(var_array)
        print("===============================================================")
        print('')
        print('')