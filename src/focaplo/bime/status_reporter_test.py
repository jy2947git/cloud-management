'''
Created on Jun 18, 2010

@author: jy2947
'''
import unittest
import json
from focaplo.bime.status_reporter import StatusReporter

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def testReportStatus(self):
        reporter = StatusReporter()
        reporter.report("192.168.8.128", "5672", "guest", "guest")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()