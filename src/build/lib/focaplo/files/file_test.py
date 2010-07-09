'''
Created on May 24, 2010

@author: jy2947
'''
import unittest
from focaplo.files.file import FileUtils

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testBackup(self):
        print "testing..."
        mc = FileUtils();
        mc.backup("/Users/jy2947/Documents/eclipse-workspace/bime/Documents/python/amqp_consumer.py")
        pass

    def testConcat(self):
        print "testing!"
        mc = FileUtils()
        allString = mc.concat("/Users/jy2947/Documents/eclipse-workspace/bime/Documents/python", "*.py")
        print allString
        pass
    
    def testTemplate(self):
        mc = FileUtils()
        s = mc.template_substitute("./my.template",this='summer', that='winter')
        print s;
    
    def testWriteWithTemplate(self):
        mc = FileUtils()
        mc.write_with_template("/tmp/t.me", "./my.template",this='summer', that='winter')

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testWriteWithTemplate']
    unittest.main()