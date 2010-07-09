'''
Created on Jun 18, 2010

@author: jy2947
'''
import unittest
import json
from focaplo.bime.status_reporter import StatusReporter
from threading import Timer
import random

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def testReportStatus(self):
        reporter = StatusReporter()
        reporter.report(reporter.collect(), "192.168.8.128", "5672", "guest", "guest")

    def colectStatus(self, host="server0"):
        msg = json.dumps({"name":host, "private_ip":host,"public_ip":host},sort_keys=True)
        return msg

    def testDaemon(self):
        
        '''test daemon'''

        reporter = StatusReporter()
        reporter.start_report_daemon("192.168.8.128", "5672", "guest", "guest", self.colectStatus, "server2")

    def f1(self, func, *args):
        print args
        print 'i am f1, here is return from running func' + func(*args)
        print 'done'
        
    def f(self, p1, p2, p3):
        print p1
        print p2
        print p3
        return p1 + ' ' + p2 + ' ' +  p3
    
    def testF1(self):
        self.f1(self.f, "a","b","c")
        
    def testMultipleServers(self):
#        t = Timer(30.0, self.testDaemon, args=[], kwargs={})
#        t.start()
#        t.join()
        hosts = ['server1', 'server2', 'server3']
        for host in hosts:
            reporter = StatusReporter()
            reporter.start_report_daemon("192.168.8.128", "5672", "guest", "guest", self.colectStatus, host)
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testDaemon']
    unittest.main()