'''
Created on May 24, 2010
it assumes the directory of Haproxy is /etc/haproxy, where all the templates exist
@author: jy2947
'''

import os
import traceback
import sys
import focaplo.files.file
from string import Template
import subprocess
class HaproxyUtils(object):
    '''
    classdocs
    '''
    def getCurrentConfiguration(self):
        """get the current haproxy.cfg """
        res=None
        try:
            res=open("/etc/haproxy/haproxy.cfg","r").read()
        except:
            res=sys.exc_info()[0]
            print("error:",res)
            traceback.print_exc();
        finally:
            return res
        
    def hotReconfiguration(self):
        """run the shellscript ot hot reconfigure haproxy """
        res=None
        try:
            res=subprocess.call(["/usr/local/bime-home/bime/scripts/haproxy/reconfigure.sh"],shell=True)
            print 'return ' + str(res)
        except:
            res=sys.exc_info()[0]
            print("error:",res)
            traceback.print_exc();
        finally:
            return res
        
    def addRouting(self, subdomain, host, port, configdir='/etc/haproxy'):
        """add acl, backend, aclbackend files for the new routing"""
        res=None
        try:
            print "add " + subdomain+"->" + host+":"+port
            #get templates
            acltemplate=Template(open(configdir+'/acl.template','r').read())
            backendtemplate=Template(open(configdir+'/backend.template','r').read())
            aclbackendtemplate=Template(open(configdir+'/acl-backend.template','r').read())
            #write files subdomain.acl and subdomain.backend
            aclfile=subdomain+".acl"
            backendfile=subdomain+".backend"
            aclbackendfile=subdomain+".aclbackend"
            acl = open(configdir+"/"+aclfile, "w")
            acl.write(acltemplate.substitute(subdomain=subdomain))
            acl.close()
            backend = open(configdir+'/'+backendfile, 'w')
            backend.write(backendtemplate.substitute(subdomain=subdomain,host=host,port=port))
            backend.close()
            aclbackend = open(configdir+"/"+aclbackendfile, "w")
            aclbackend.write(aclbackendtemplate.substitute(subdomain=subdomain))
            aclbackend.close()
            res="success"
        except:
            res=sys.exc_info()[0]
            print("error:",res)
            traceback.print_exc();
        finally:
            return res
        
    def removeRouting(self, subdomain, configdir='/etc/haproxy'):
        """remove the acl, backend, aclbackend file for the routing"""
        res=None
        try:
            print 'remove ' + subdomain
            aclfile=subdomain+".acl"
            backendfile=subdomain+".backend"
            aclbackendfile=subdomain+".aclbackend"
            os.remove(configdir+"/"+aclfile)
            os.remove(configdir+"/"+backendfile)
            os.remove(configdir+"/"+aclbackendfile)
            res="success"
        except:
            res=sys.exc_info()[0]
            print("error:",res)
            traceback.print_exc();
        finally:
            return res    
    def reconfig(self,config_file='/etc/haproxy/haproxy.cfg',config_dir='/etc/haproxy'):
        """recreate the haproxy configuration from template."""
        res=None
        try:
            templatename=config_dir+'/'+ 'haproxy.cfg.template'
            print 'checking ' + templatename +  '...'
            if(os.path.exists(templatename)):
                print 'found '
                self.__recreate_configuration__(config_file,templatename,config_dir)
                print 'file generated:' + config_file
            else:
                print 'template file not found'
            print 'done'
            res="success"
        except:
            res=sys.exc_info()[0]
            print("error:",res)
            traceback.print_exc();
        finally:
            return res  

    def __recreate_configuration__(self,config_file='/etc/haproxy/haproxy.cfg', template_name='/etc/haproxy/haproxy.cfg.template',config_dir='/etc/haproxy'):
        """recreate the haproxy configuration file based on template and files in config directory"""
        print 'recreating ' + config_file+' from ' + template_name + ' in ' + config_dir
        #first back up the file
        fu = focaplo.files.file.FileUtils()
        fu.backup(config_file)
       
        #search the ACL files in the configuration directory
        acl=fu.concat(config_dir, '*.acl')
        print acl
        aclbackend=fu.concat(config_dir, '*.aclbackend')
        print acl
        backend=fu.concat(config_dir, '*.backend')
        print backend
        #read template
        configtemplate=Template(open(template_name).read())
        
        #write new to file
        conf = open(config_file, 'w')
        conf.write(configtemplate.substitute(aclplaceholder=acl,aclbackendplaceholder=aclbackend,backendplaceholder=backend))
        conf.close()
        print 'done'
    def __init__(self):
        '''
        Constructor
        '''
        