Authors: Angus Fung, Alvin Lee, Ryan You

Please run on Python3.

1. Please put all of the below files into the same directory.
numbrix_sample_run.py
test_case_numbrix.py
test_case_hidato.py
propagators2.py    (FC, GAC)
numbrix_reg_csp.py (implementation of numbrix)
hidato_reg_csp.py  (implementation of hidato)
cspbase.py

2. Please open numbrix_sample_run.py

3. There are 4 classes that can be tested. These are the a-class (test_case_numbrix.py), c-class, hidsq-class, and hid-class (test_case_hidato.py).
   The a-class is for the Numbrix test cases. The latter 3 are for the Hidato test cases.

4. To run the a-class, line 1 must be as below.
from numbrix_reg_csp import * 

Line 30 must be the only uncommented for-loop condition.

5. To run the c-class, line 1 must be as below.
from hidato_reg_csp import * 

Line 31 must be the only uncommented for-loop condition (re-comment Line 30).

6. To run the hidsq-class and hid-class, please keep line 1 as
from hidato_reg_csp import * and simple uncomment Lines 32, 33 respectively (only keep one line uncommented from 30-33 at a time)

Note: Running hidato_reg_csp on a-class (Numbrix test case) will result in non-unique solutions due to the nature of the constraints.

The output for each run is in a format where the first block shows information about set up time, the second block shows information
about FC, the third block shows information about GAC, and the last block outputs the solution.



Please check the test_case_numbrix.py and test_case_hidato.py for the solutions to the test cases (in block comments directly above each test case).