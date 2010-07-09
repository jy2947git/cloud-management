'''
Created on May 25, 2010

@author: jy2947
'''
import traceback
import os
import sys
import time
import focaplo.files.file
import subprocess
class DataSourceUtils(object):
    '''
    classdocs
    '''
    def removeClient(self, config_dir, databaseName):
        res=None
        try:
            res=subprocess.call(["/usr/local/bime-home/bime/scripts/client-management/dropLab.sh "+config_dir+"/"+databaseName],shell=True)
            print 'return ' + str(res)
            print "done"
        except:
            res = "failed"
            traceback.print_exc();
        finally:
            return res
                
    def add_new_client(self,config_dir, host, databaseName, databasepassword, autoid, adminemail, adminfullname, adminencryptedpassword, templateDir="/usr/local/bime-home/bime/scripts/mysql"):
        res=None
        try:        
            print 'creating new client ' + databaseName
            #first create the home directory
            if os.path.exists(config_dir+"/"+databaseName):
                archiveName=config_dir+"/"+databaseName+"."+str(time.time())+".cancelled"
                os.rename(config_dir+"/"+databaseName, archiveName)
                print 'found directory already exists:' + databaseName + " renamed existing one to" + archiveName
            else:
                os.mkdir(config_dir+"/"+databaseName)
            #create the sql files for this specific client
            self.create_create_database_sql(config_dir, host, databaseName, databasepassword, templateDir+"/"+"createDatabase.template");
            self.create_drop_database_sql(config_dir, host, databaseName, databasepassword, templateDir+"/"+"dropDatabase.template");
            self.create_auto_increment_sql(config_dir, databaseName, autoid, templateDir+"/"+"auto_increment.template");
            self.create_initialize_lab_sql(config_dir, databaseName, autoid, adminemail, adminfullname, adminencryptedpassword, templateDir+"/"+"initialize_lab.template");
            
            #run the sql files agaist the database server
            #the account to run this py must have permission to the /usr/local/bime-home directory and the config-dir
            res=subprocess.call(["/usr/local/bime-home/bime/scripts/client-management/addLab.sh "+config_dir+"/"+databaseName],shell=True)
            print 'return ' + str(res)
            if res==1:
                print 'creating jdbc properties'
                res=self.create_jdbc_properties(config_dir, host, databaseName, databasepassword, templateDir+"/"+"jdbc.properties.template")
            print "done"
        except:
            res = "failed"
            traceback.print_exc();
        finally:
            return res      
          
    def create_jdbc_properties(self,config_dir,host,databaseName,password,template):
        #create jdbc.properties in configuration directory
        print 'creating jdbc.properties'
        mc = focaplo.files.file.FileUtils()
        mc.write_with_template(config_dir+"/jdbc.properties", template,databasename=databaseName,host=host,databasepassword=password)
        print 'done'
        
    def create_drop_database_sql(self,config_dir, host,databaseName,databasepassword,template):
        print 'creating dropDatabase.sql'
        mc = focaplo.files.file.FileUtils()
        mc.write_with_template(config_dir+"/dropDatabase.sql", template,databasename=databaseName,host=host,databasepassword=databasepassword)

        print 'done'
        
    def create_create_database_sql(self,config_dir,host,databaseName,databasepassword,template):
        print 'creating createDatabase.sql'
        mc = focaplo.files.file.FileUtils()
        mc.write_with_template(config_dir+"/createDatabase.sql", template,databasename=databaseName,databasepassword=databasepassword,host=host)
        print 'done'
        
    def create_auto_increment_sql(self,config_dir, databaseName, autoid, template):
        print 'creating auto_increment.sql'
        mc = focaplo.files.file.FileUtils()
        mc.write_with_template(config_dir+"/auto_increment.sql", template,databasename=databaseName,autoid=autoid)

        print 'done'
    
    def create_initialize_lab_sql(self,config_dir, databaseName, autoid, adminemail, adminfullname, adminencryptedpassword,template):
        print 'creating initialize_lab.sql'
        mc = focaplo.files.file.FileUtils()
        mc.write_with_template(config_dir+"/initialize_lab.sql", template,databasename=databaseName,autoid=autoid,adminemail=adminemail,adminfullname=adminfullname,adminencryptedpassword=adminencryptedpassword)

        print 'done'
        
    def __init__(self):
        '''
        Constructor
        '''
        