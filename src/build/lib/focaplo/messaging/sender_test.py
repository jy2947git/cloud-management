'''
Created on May 24, 2010

@author: jy2947
'''
import unittest
import json
import focaplo.messaging.amqp_sender
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testAddHaproxyRouting(self):
        msg = json.dumps({"command":"add", "subdomain":"rrrrr","host":"192.292.2.4","port":"8080", "configdir":"/etc/haproxy", "configfile":"/etc/haproxy/haproxy.cfg"},sort_keys=True)
        sender = focaplo.messaging.amqp_sender.Sender()
        sender.send(msg, "192.168.8.130", "5672", "guest", "guest", "/", "haproxy", "incoming", "configuration")
        pass

    def testAddNewBimeClient(self):
        #d.add_new_client(jobj['config_dir'], jobj['host'], jobj['databaseName'], jobj['password'],jobj['autoid'], jobj['adminemail'], jobj['adminfullname'], jobj['adminencryptedpassword'], jobj['template'])
        msg=json.dumps({"command":"add","config_dir":"/tmp","host":"192.168.8.128","databaseName":"my1","password":"11111","autoid":"300000","adminemail":"me@yahoo.com","adminfullname":"Joe Stmith","adminencryptedpassword":"0390303","template_dir":"/tmp"})
        sender = focaplo.messaging.amqp_sender.Sender()
        sender.send(msg, "192.168.8.128", "5672", "guest", "guest", "/", "client", "datasource")

    def testSendError(self):
        msg="this is an error message!"
        sender = focaplo.messaging.amqp_sender.Sender()
        sender.send(msg, "192.168.8.128", "5672", "guest", "guest", "/", "monitor", "error")
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testAddHaproxyRouting']
    unittest.main()