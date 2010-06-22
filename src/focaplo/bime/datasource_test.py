'''
Created on May 25, 2010

@author: jy2947
'''
import unittest
import os
import shutil
from focaplo.bime.datasource import DataSourceUtils
from focaplo.files.file import FileUtils
class Test(unittest.TestCase):


    def setUp(self):
        print 'copy template files to /tmp directory'
        mc = FileUtils();
        templatedir="/home/jy2947/Documents/eclipse-workspace/bime/scripts/mysql"
        shutil.copyfile(templatedir+"/"+"auto_increment.template","/tmp/auto_increment.template")
        shutil.copyfile(templatedir+"/"+"createDatabase.template","/tmp/createDatabase.template")
        shutil.copyfile(templatedir+"/"+"dropDatabase.template","/tmp/dropDatabase.template")
        shutil.copyfile(templatedir+"/"+"initialize_lab.template","/tmp/initialize_lab.template")
        shutil.copyfile(templatedir+"/"+"jdbc.properties.template","/tmp/jdbc.properties.template")
        
        mc.remove('/tmp','*.sql')
        mc.remove('/tmp','*.properties')
        


    def tearDown(self):
        print 'deleting templates...'
        os.remove("/tmp/auto_increment.template")
        os.remove("/tmp/createDatabase.template")
        os.remove("/tmp/dropDatabase.template")
        os.remove("/tmp/initialize_lab.template")
        os.remove("/tmp/jdbc.properties.template")


    def testCreateJdbcProperties(self):
        d = DataSourceUtils()
        d.create_jdbc_properties("/tmp", "123.4.5.7", "lab303", "pppppp", "/tmp/jdbc.properties.template")

    def testDropDatabase(self):
        d = DataSourceUtils()
        d.create_drop_database_sql("/tmp", "123.4.5.7", "lab303", "pppppp", "/tmp/dropDatabase.template")

    def testAutoIncrement(self):
        d = DataSourceUtils()
        d.create_auto_increment_sql("/tmp", "lab303", "120000", "/tmp/auto_increment.template")


    def testCreateDatabase(self):
        d = DataSourceUtils()
        d.create_create_database_sql("/tmp", "123.4.5.7", "lab123", "kdofodjsafo","/tmp/createDatabase.template")
        
    def testInitializeLab(self):
        d = DataSourceUtils()
        d.create_initialize_lab_sql("/tmp",  "lab303", "1200000", "admin@yahoo.com","Joe Smith","93nf93nedoe","/tmp/initialize_lab.template")

    def testAddNewClient(self):
        d = DataSourceUtils()
        d.add_new_client("/tmp", "localhost", "lab034", "passpass", "340000", "meyahoo.com", "joe smith", "33333", "/tmp")

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testAddNewClient']
    unittest.main()