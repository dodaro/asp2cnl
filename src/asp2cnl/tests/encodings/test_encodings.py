import unittest

from chemiotherapy_scheduling.test import TestRules as Test1
from graph_coloring.test import TestRules as Test2
#from hamiltonian_path.test import TestRules as Test3
from hanoi_tower.test import TestRules as Test4
#from integer_sets.test import TestRules as Test5
from mao.test import TestRules as TestMao
from maxclique.test import TestRules as Test6
from nurse_scheduling.test import TestRules as Test7
from robot_arm.test import TestRules as Test8
#from undirected_graph.test import TestRules as Test9

class TestEncodings(unittest.TestCase):
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test1))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test2))
    #test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test3))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test4))
    #test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test5))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMao))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test6))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test7))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test8))
    #test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test9))


    runner=unittest.TextTestRunner()
    runner.run(test_suite)

