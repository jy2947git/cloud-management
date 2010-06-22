'''
Created on May 24, 2010

@author: jy2947
'''
import unittest
import simplejson as json
import os
import shutil
import focaplo.messaging.amqp_listener
import focaplo.files.file
from functools import partial
class Test(unittest.TestCase):


    def setUp(self):
        print 'copy template files to /tmp directory'
        mc = focaplo.files.file.FileUtils();
        cwd=os.getcwd()
        parentpath="/users/jy2947/Documents/eclipse-workspace/bime/scripts"
        
        
        shutil.copyfile(parentpath+"/haproxy/"+"haproxy.cfg.template","/tmp/haproxy.cfg.template")
        shutil.copyfile(parentpath+"/haproxy/"+"acl.template","/tmp/acl.template")
        shutil.copyfile(parentpath+"/haproxy/"+"acl-backend.template","/tmp/acl-backend.template")
        shutil.copyfile(parentpath+"/haproxy/"+"backend.template","/tmp/backend.template")
        mc.remove('/tmp','*.acl')
        mc.remove('/tmp','*.backend')
        mc.remove('/tmp','*.aclbackend')
        shutil.copyfile(parentpath+"/mysql/"+"auto_increment.template","/tmp/auto_increment.template")
        shutil.copyfile(parentpath+"/mysql/"+"createDatabase.template","/tmp/createDatabase.template")
        shutil.copyfile(parentpath+"/mysql/"+"dropDatabase.template","/tmp/dropDatabase.template")
        shutil.copyfile(parentpath+"/mysql/"+"initialize_lab.template","/tmp/initialize_lab.template")
        shutil.copyfile(parentpath+"/mysql/"+"jdbc.properties.template","/tmp/jdbc.properties.template")
        
        mc.remove('/tmp','*.sql')
        mc.remove('/tmp','*.properties')

    def tearDown(self):
       
        print 'deleting templates...'
        os.remove("/tmp/haproxy.cfg.template")
        os.remove("/tmp/acl.template")
        os.remove("/tmp/acl-backend.template")
        os.remove("/tmp/backend.template")

    def testHandlerOfHaproxy(self):
        listener = focaplo.messaging.haproxy_listener.HaproxyListener()
        listener.__handle_haproxy__('{"command":"add", "subdomain":"lab234","host":"192.292.2.4","port":"8080"}')
        
    def testJson(self):
        #jstring = simplejson.dump({"command":"add", "subdomain":"lab234","host":"192.292.2.4","port":"8080"})
        jobj = json.loads('{"command":"add", "subdomain":"lab234","host":"192.292.2.4","port":"8080"}')
        print jobj["command"]
        print jobj["subdomain"]
        print jobj["host"]
        print jobj["port"]
        
    
    def testListenerOfHaproxy(self):
        listener = focaplo.messaging.haproxy_listener.HaproxyListener()
        listener.listen("192.168.8.128", "5672", "guest", "guest", "/", "haproxy","incoming", "configuration", listener.callback_reconfigure_haproxy)
        print "listener is done"
        
    def testListenerOfClient(self):
        listener = focaplo.messaging.client_listener.ClientListener()
        listener.listen("192.168.8.128", "5672", "guest", "guest", "/", "client","incoming", "datasource", listener.callback_update_client)
        print "listener is done"

    def testStartHaproxyListener(self):
        listener = focaplo.messaging.client_listener.ClientListener()
        listener.startHaproxyListener("192.168.8.128", "5672", "guest", "guest")
        
    def testStartBimeClientListener(self):
        listener = focaplo.messaging.client_listener.ClientListener()
        listener.startBimeClientListener("192.168.8.128", "5672", "guest", "guest")
        
    def printMessage(self, message):
        print message.body
        
        
        
    def testStartAmqpListener(self):
        listener = focaplo.messaging.amqp_listener.Listener();
        print 'starting listener...'
        listener.listen("192.168.8.128", "5672", "guest", "guest", "/", "bime", "server_status_queue", "server_status", self.printMessage);
        
if __name__ == "__main__":
    print 'test main'
    import sys;sys.argv = ['', 'Test.testStartAmqpListener']
    unittest.main()