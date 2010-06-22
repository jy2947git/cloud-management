'''
Created on May 24, 2010

@author: jy2947
'''
import sys
import os
import time
import shutil
import fnmatch
import string
from string import Template
import traceback
class FileUtils(object):
    '''
    classdocs
    '''

    def concat(self, input_file_dir,name_pattern):
        """search in the input file directory, and contact the found files to string"""
        str_list=[]
        filenames = os.listdir(input_file_dir)
        for filename in filenames:
            if fnmatch.fnmatch(filename,name_pattern):
                print filename
                str_list.append(open(input_file_dir+"/"+filename).read())
                str_list.append("\n")
        return string.join(str_list,'')
    
    def backup(self, output_file):
        """back up file if it exists."""
        backupname=output_file+"."+str(time.time())
        print "checking " + output_file +  "..."
        if(os.path.exists(output_file)):
            print "found "
            shutil.copyfile(output_file,backupname)
            print "file copied:" + backupname
        else:
            print "file not found, no need to backup"
        print "done"
 
    def remove(self, dir, pattern):
        for each in os.listdir(dir):
            if fnmatch.fnmatch(each,pattern):
                os.remove(dir+"/"+each)
                
    def template_substitute(self, template_file,**kws):
        #use input to substitute the teplate and return string
        tm=Template(open(template_file).read())
        return tm.substitute(kws)
    
    def write_with_template(self, targetFile, templateFile, **mapping):
        f=None
        try:
            f = open(targetFile, "w")
            f.write(self.template_substitute(templateFile,**mapping))
        except:
            print("error:",sys.exc_info()[0])
            traceback.print_exc();
            raise
        finally:
            if f!=None:
                f.close()
        
    def __init__(self):
        '''
        Constructor
        '''
        