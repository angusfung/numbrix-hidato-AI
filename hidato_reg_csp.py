from cspbase import *
import itertools

def get_satisfying_tuples(vars, reduced_domain, max):
    var_doms = []
    new_tuples = []
    for var in vars:
        if type(var) is int:
            continue
        if len(var.cur_domain()) == 1:
            var_doms.append(var.cur_domain())
        else:
            var_doms.append(reduced_domain)
        
    sat_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup) and (tup[0]+1 in tup and tup[0] -1 in tup)] 
    
    
    if 1 in reduced_domain or max in reduced_domain:
        if 1 in reduced_domain and max in reduced_domain:
            new_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup) and ((tup[0] ==1 and 2 in tup) or tup[0] == max and max-1 in tup)] 
        
        elif 1 in reduced_domain:
            new_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup) and tup[0] ==1 and 2 in tup] 
        elif max in reduced_domain:
            new_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup) and tup[0] == max and max-1 in tup] 
            
    return list(set(sat_tuples + new_tuples))
def make_var_doms(vars):
    var_doms = []
    for var in vars:
        if type(var) is int:
            continue
        if len(var.cur_domain()) == 1:
            var_doms.append(var.cur_domain())
        else:
            var_doms.append(reduced_domain)
    return var_doms

def first_last_sat_tuples(vars, reduced_domain):
    var_doms = []
    for var in vars:
        if type(var) is int:
            continue
        if len(var.cur_domain()) == 1:
            var_doms.append(var.cur_domain())
        else:
            var_doms.append(reduced_domain)
        
    sat_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup) and (tup[0]+1 in tup or tup[0] -1 in tup)] 
    return sat_tuples


def single_row(initial_grid):
    max_num = 0
    initial_nums = []
    for i in range(len(initial_grid)):
        if initial_grid[i] != -2:
            max_num += 1
            if initial_grid[i] != -1:
                initial_nums.append(initial_grid[i])
    initial_nums.sort()
    whole_dom = [k for k in range(1, max_num+1)]
    reduced_domain = list(set(whole_dom) - set(initial_nums))
    reduced_domain.sort()
    
    # Assign domain to each variable
    variable_array = []
    for i in range(len(initial_grid)):
        if initial_grid[i] == -1:
            variable_array.append(Variable('{}'.format(i), whole_dom))
        elif initial_grid[i] == -2:
            variable_array.append(0) 
        else:
            variable_array.append(Variable('{}'.format(i),[initial_grid[i]]))
            
    # Constraints
    cons = []
    if len(variable_array) == 1:
        numbrix_csp = CSP('Numbrix', variable_array)
        return numbrix_csp, variable_array
    
    
    for i in range (len(variable_array)):
        vars = []
        if variable_array[i] == 0:
            continue
        
        # if left edge
        if i == 0:
            vars.append(variable_array[i])
            if variable_array[i+1] != 0:
                vars.append(variable_array[i+1])
        
        # if right edge
        elif i == len(variable_array) - 1:
            vars.append(variable_array[i])
            if variable_array[i-1] != 0:
                vars.append(variable_array[i-1])
        
        # anywhere else
        else:
            vars.append(variable_array[i])
            if variable_array[i-1] != 0:
                vars.append(variable_array[i-1])
            if variable_array[i+1] != 0:
                vars.append(variable_array[i+1])            
                
        con = Constraint('R{}'.format(i), vars)
        
        sat_tuples = get_satisfying_tuples(vars, reduced_domain, max_num)
        if len(sat_tuples) == 0:
            if (vars[0].cur_domain()[0] == 1 and len(vars[0].cur_domain()) == 1)  or (vars[0].cur_domain()[0] == max_num and len(vars[0].cur_domain()) == 1):
                sat_tuples = first_last_sat_tuples(vars, reduced_domain)
        
        if len(sat_tuples) == 0:
            sat_tuples.append([1])
        
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        

    flattened_var = [val for val in variable_array if val != 0]
    
    # binary not equal constraints for all pairs
    for i in range(len(flattened_var)):
        for j in range(i+1, len(flattened_var)):
            vars = []
            var_doms = []
            flag = False
            vars.append(flattened_var[i])
            vars.append(flattened_var[j])
            con = Constraint('R{}'.format(i), vars)
            
            for var in vars:
                if type(var) is int:
                    flag = True
                    continue
                if len(var.cur_domain()) == 1:
                    var_doms.append(var.cur_domain())
                else:
                    var_doms.append(reduced_domain)
            if not flag:
                sat_tuples = [tup for tup in itertools.product(*var_doms) if tup[0] != tup[1]]
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
    
    
    numbrix_csp = CSP('Numbrix', flattened_var)
    for c in cons:
        numbrix_csp.add_constraint(c)
        
    return numbrix_csp, variable_array
        
def single_column(initial_grid):
    max_num = 0
    initial_nums = []
    for i in range(len(initial_grid)):
        if initial_grid[i][0] != -2:
            max_num += 1
            if initial_grid[i][0] != -1:
                initial_nums.append(initial_grid[i][0])
    initial_nums.sort()
    whole_dom = [k for k in range(1, max_num+1)]
    reduced_domain = list(set(whole_dom) - set(initial_nums))
    reduced_domain.sort()
    
    # Assign domain to each variable
    variable_array = []
    for i in range(len(initial_grid)):
        if initial_grid[i][0] == -1:
            variable_array.append(Variable('{}'.format(i), whole_dom))
        elif initial_grid[i][0] == -2:
            variable_array.append(0) 
        else:
            variable_array.append(Variable('{}'.format(i),[initial_grid[i][0]]))
            
    # Constraints
    cons = []
    if len(variable_array) == 1:
        numbrix_csp = CSP('Numbrix', variable_array)
        return numbrix_csp, variable_array
    
    
    for i in range (len(variable_array)):
        vars = []
        if variable_array[i] == 0:
            continue
        
        # if left edge
        if i == 0:
            vars.append(variable_array[i])
            if variable_array[i+1] != 0:
                vars.append(variable_array[i+1])
        
        # if right edge
        elif i == len(variable_array) - 1:
            vars.append(variable_array[i])
            if variable_array[i-1] != 0:
                vars.append(variable_array[i-1])
        
        # anywhere else
        else:
            vars.append(variable_array[i])
            if variable_array[i-1] != 0:
                vars.append(variable_array[i-1])
            if variable_array[i+1] != 0:
                vars.append(variable_array[i+1])            
                
        con = Constraint('R{}'.format(i), vars)
        
        sat_tuples = get_satisfying_tuples(vars, reduced_domain, max_num)
        if len(sat_tuples) == 0:
            if (vars[0].cur_domain()[0] == 1 and len(vars[0].cur_domain()) == 1)  or (vars[0].cur_domain()[0] == max_num and len(vars[0].cur_domain()) == 1):
                sat_tuples = first_last_sat_tuples(vars, reduced_domain)
        
        if len(sat_tuples) == 0:
            sat_tuples.append([1])
        
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
        

    flattened_var = [val for val in variable_array if val != 0]
    
    # binary not equal constraints for all pairs
    for i in range(len(flattened_var)):
        for j in range(i+1, len(flattened_var)):
            vars = []
            var_doms = []
            flag = False
            vars.append(flattened_var[i])
            vars.append(flattened_var[j])
            con = Constraint('R{}'.format(i), vars)
            
            for var in vars:
                if type(var) is int:
                    flag = True
                    continue
                if len(var.cur_domain()) == 1:
                    var_doms.append(var.cur_domain())
                else:
                    var_doms.append(reduced_domain)
            if not flag:
                sat_tuples = [tup for tup in itertools.product(*var_doms) if tup[0] != tup[1]]
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
    
    
    numbrix_csp = CSP('Numbrix', flattened_var)
    for c in cons:
        numbrix_csp.add_constraint(c)
        
    return numbrix_csp, variable_array

def numbrix_model_1(initial_grid):
    
    # single row case
    if type(initial_grid[0]) is int:
        numbrix_csp, variable_array = single_row(initial_grid)
        return numbrix_csp, variable_array
        
    if len(initial_grid[0]) == 1:
        numbrix_csp, variable_array = single_column(initial_grid)
        return numbrix_csp, variable_array
    
    
    max_num = 0
    
    # store initially given numbers from grid in this array
    initial_numbers = [] 
    
    # Calculate the maximum number that that will be on the grid
    for i in range(len(initial_grid)):
        for j in range(len(initial_grid[i])):
            if initial_grid[i][j] != -2:
                max_num += 1
                if initial_grid[i][j] != -1:
                    initial_numbers.append(initial_grid[i][j])
    initial_numbers.sort()
    
    whole_domain = [k for k in range (1, max_num+1)]
    reduced_domain = list(set(whole_domain) - set(initial_numbers))
    reduced_domain.sort()
    
    # Assign a domain to each variable
    variable_array = []
    for i in range(len(initial_grid)):
        vars = []
        for j in range (len(initial_grid[i])):
            if initial_grid[i][j] == -1:
                vars.append(Variable('{}, {}'.format(i, j), [k for k in range(1, max_num + 1)]))
            elif initial_grid[i][j] == -2:
                vars.append(0)
            else:
                vars.append(Variable('{}, {}'.format(i, j), [initial_grid[i][j]]))
        variable_array.append(vars)
    
    
    # Adjacent constraints       
    cons = []
    for i in range(len(initial_grid)):
        for j in range(len(initial_grid[0])):
            vars = []
            
            if variable_array[i][j] == 0:
                continue
            
            # if number on top edge
            if i == 0:  
            
                # if number in top left corner
                if j == 0:  
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i+1][j] !=0:
                        vars.append(variable_array[i+1][j])
                    if variable_array[i][j+1] !=0:
                        vars.append(variable_array[i][j+1])
                    if variable_array[i+1][j+1] !=0:
                        vars.append(variable_array[i+1][j+1])
                    con = Constraint('R{}'.format(i), vars)
                
                # if number in top right corner
                elif j == len(initial_grid[i]) - 1: 
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i+1][j] !=0:   
                        vars.append(variable_array[i+1][j])
                    if variable_array[i][j-1] !=0:
                        vars.append(variable_array[i][j-1])
                    if variable_array[i+1][j-1] !=0:
                        vars.append(variable_array[i+1][j-1])
                    con = Constraint('R{}'.format(i), vars)
                    
                # otherwise just on top edge    
                else:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i+1][j] !=0:
                        vars.append(variable_array[i+1][j])
                    if variable_array[i][j-1] !=0:
                        vars.append(variable_array[i][j-1])
                    if variable_array[i][j+1] !=0:
                        vars.append(variable_array[i][j+1])
                    if variable_array[i+1][j+1] !=0:
                        vars.append(variable_array[i+1][j+1])
                    if variable_array[i+1][j-1] !=0:
                        vars.append(variable_array[i+1][j-1])
                    con = Constraint('R{}'.format(i), vars)    
                    

  #   #           # if number on bottom edge of grid
            elif i == len(initial_grid) - 1:
                
                # if number in bottom left corner
                if j == 0:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i-1][j] !=0:
                        vars.append(variable_array[i-1][j])
                    if variable_array[i][j+1] !=0:
                        vars.append(variable_array[i][j+1])
                    if variable_array[i-1][j+1] !=0:
                        vars.append(variable_array[i-1][j+1])
                    con = Constraint('R{}'.format(i), vars)
                    
                # if number in bottom right corner
                elif j == len(initial_grid[i]) -1:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i-1][j] !=0:
                        vars.append(variable_array[i-1][j])
                    if variable_array[i][j-1] !=0:
                        vars.append(variable_array[i][j-1])
                    if variable_array[i-1][j-1] !=0:
                        vars.append(variable_array[i-1][j-1])
                    con = Constraint('R{}'.format(i), vars)
                    
                # otherwise just on bottom edge
                else:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i-1][j] !=0:
                        vars.append(variable_array[i-1][j])
                    if variable_array[i][j-1] !=0:
                        vars.append(variable_array[i][j-1])
                    if variable_array[i][j+1] !=0:
                        vars.append(variable_array[i][j+1])
                    if variable_array[i-1][j+1] !=0:
                        vars.append(variable_array[i-1][j+1])
                    if variable_array[i-1][j-1] !=0:
                        vars.append(variable_array[i-1][j-1])
                    con = Constraint('R{}'.format(i), vars)
                    
            # if the number is on the left or right edge (corners already taken care of)
            elif j == 0 or j == len(initial_grid[i]) - 1:
                
                # number is on left edge
                if j == 0:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i-1][j] !=0:
                        vars.append(variable_array[i-1][j])
                    if variable_array[i+1][j] !=0:
                        vars.append(variable_array[i+1][j])
                    if variable_array[i][j+1] !=0:
                        vars.append(variable_array[i][j+1])
                    if variable_array[i-1][j+1] !=0:
                        vars.append(variable_array[i-1][j+1])
                    if variable_array[i+1][j+1] !=0:
                        vars.append(variable_array[i+1][j+1])
                    con = Constraint('R{}'.format(i), vars)
                    
                # number is on right edge    
                elif j == len(initial_grid[i]) - 1:
                    if variable_array[i][j] !=0:
                        vars.append(variable_array[i][j])
                    if variable_array[i-1][j] !=0:
                        vars.append(variable_array[i-1][j])
                    if variable_array[i+1][j] !=0:
                        vars.append(variable_array[i+1][j])
                    if variable_array[i][j-1] !=0:
                        vars.append(variable_array[i][j-1])
                    if variable_array[i-1][j-1] !=0:
                        vars.append(variable_array[i-1][j-1])
                    if variable_array[i+1][j-1] !=0:
                        vars.append(variable_array[i+1][j-1])
                    con = Constraint('R{}'.format(i), vars)
                
            # anywhere else on the grid (won't be on an edge)
            else:
                if variable_array[i][j] !=0:
                    vars.append(variable_array[i][j])
                if variable_array[i-1][j] !=0:
                    vars.append(variable_array[i-1][j])
                if variable_array[i+1][j] !=0:
                    vars.append(variable_array[i+1][j])
                if variable_array[i][j-1] !=0:
                    vars.append(variable_array[i][j-1])
                if variable_array[i][j+1] !=0:
                    vars.append(variable_array[i][j+1])
                if variable_array[i-1][j-1] !=0:
                    vars.append(variable_array[i-1][j-1])
                if variable_array[i-1][j+1] !=0:
                    vars.append(variable_array[i-1][j+1])
                if variable_array[i+1][j-1] !=0:
                    vars.append(variable_array[i+1][j-1])
                if variable_array[i+1][j+1] !=0:
                    vars.append(variable_array[i+1][j+1])
                con = Constraint('R{}'.format(i), vars)
                
            sat_tuples = get_satisfying_tuples(vars, reduced_domain, max_num)
            if len(sat_tuples) == 0:
                if (vars[0].cur_domain()[0] == 1 and len(vars[0].cur_domain()) == 1)  or (vars[0].cur_domain()[0] == max_num and len(vars[0].cur_domain()) == 1):
                    sat_tuples = first_last_sat_tuples(vars, reduced_domain)
            
            if len(sat_tuples) == 0:
                sat_tuples.append([1])
            
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # ******All diff constraints take too long******
    # var = []
    # var_doms = []
    # for i in range(len(variable_array)):
    #     for j in range(len(variable_array[i])):
    #         vars.append(variable_array[i][j])
    #         
    # con = Constraint('R{}'.format(i), vars)
    # 
    # for var in vars:
    #     if len(var.cur_domain()) == 1:
    #         var_doms.append(var.cur_domain())
    #     else:
    #         var_doms.append(reduced_domain)
    # 
    # sat_tuples = [tup for tup in itertools.product(*var_doms) if len(set(tup)) == len(tup)]
    # con.add_satisfying_tuples(sat_tuples)
    # cons.append(con)


    flattened_var = [val for sublist in variable_array for val in sublist if val != 0]
    
    # binary not equal constraints for all pairs
    for i in range(len(flattened_var)):
        for j in range(i+1, len(flattened_var)):
            vars = []
            var_doms = []
            flag = False
            vars.append(flattened_var[i])
            vars.append(flattened_var[j])
            con = Constraint('R{}'.format(i), vars)
            
            for var in vars:
                if type(var) is int:
                    flag = True
                    continue
                if len(var.cur_domain()) == 1:
                    var_doms.append(var.cur_domain())
                else:
                    var_doms.append(reduced_domain)
            if not flag:
                sat_tuples = [tup for tup in itertools.product(*var_doms) if tup[0] != tup[1]]
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
    
    
    numbrix_csp = CSP('Numbrix', flattened_var)
    for c in cons:
        numbrix_csp.add_constraint(c)
        
    return numbrix_csp, variable_array
    
            
            
            
            
            
            
            
            
            
            
            
                