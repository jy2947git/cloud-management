'''
Created on May 24, 2010

@author: jy2947
'''
import unittest
import focaplo.haproxy.tools
import os
import shutil
import focaplo.files.file
class Test(unittest.TestCase):


    def setUp(self):
        print 'copy template files to /tmp directory'
        mc = focaplo.files.file.FileUtils();
        templatedir="/home/jy2947/Documents/eclipse-workspace/bime/scripts/haproxy"
        shutil.copyfile(templatedir+"/"+"haproxy.cfg.template","/tmp/haproxy.cfg.template")
        shutil.copyfile(templatedir+"/"+"acl.template","/tmp/acl.template")
        shutil.copyfile(templatedir+"/"+"acl-backend.template","/tmp/acl-backend.template")
        shutil.copyfile(templatedir+"/"+"backend.template","/tmp/backend.template")
        mc.remove('/tmp','*.acl')
        mc.remove('/tmp','*.backend')
        mc.remove('/tmp','*.aclbackend')

    def tearDown(self):
       
        print 'deleting templates...'
        os.remove("/tmp/haproxy.cfg.template")
        os.remove("/tmp/acl.template")
        os.remove("/tmp/acl-backend.template")
        os.remove("/tmp/backend.template")
        


    def testRecreateConfiguration(self):
        hu = focaplo.haproxy.tools.HaproxyUtils()
        hu.recreate_configuration("/tmp/haproxy.cfg","/tmp/haproxy.cfg.template","/tmp")
    
    def testAddRouting(self):
        hu = focaplo.haproxy.tools.HaproxyUtils()
        hu.addRouting('lab1', '192.393.3.4', '6080','/tmp')
        hu.addRouting('lab2', '192.393.3.5', '6080','/tmp')
        hu.reconfig('/tmp/haproxy.cfg','/tmp')

    def testRemoveRouting(self):
        hu = focaplo.haproxy.tools.HaproxyUtils()
        hu.removeRouting('lab2', '/tmp')
        hu.reconfig('/tmp/haproxy.cfg','/tmp')
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testAddRouting']
    unittest.main()