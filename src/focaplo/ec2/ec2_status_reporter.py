#!/usr/bin/python
'''
Created on Jun 18, 2010

@author: jy2947
'''

import sys
import getopt
import json
from focaplo.bime.status_reporter import StatusReporter
from focaplo.ec2.EC2Metadata import EC2Metadata

class Ec2StatusReporter(StatusReporter):
    '''
    classdocs
    '''
    def collect(self):
        print "this is ec2"
        instanceId = EC2Metadata.get(self, "instance-id")
        localName = EC2Metadata.get(self, "local-hostname")
        privateIp = EC2Metadata.get(self, "local-ipv4")
        publicName = EC2Metadata.get(self, "public-hostname")
        publicIp = EC2Metadata.get(self, "public-ipv4")
        userData = EC2Metadata.get(self, "user-data")
        
        msg = json.dumps({"instance_id":instanceId, "local_name":localName,"public_name":publicName, "private_ip":privateIp,"public_ip":publicIp, "user_data":userData},sort_keys=True)
        return msg

    def __init__(self):
        '''
        Constructor
        '''
def main(argv=None):
        print 'in main function'
        if argv is None:
            argv=sys.argv
        try:
            opt,args=getopt.getopt(argv[1:],"h",["help"])
        except getopt.GetoptError:
            print 'usage: StatusReporter host port user password'
            sys.exit(2)
        if len(args) != 4:
            print 'usage: StatusReporter host port user password'
            sys.exit(2)
    
        
        reporter=Ec2StatusReporter()
        reporter.start_report_daemon(args[0],args[1],args[2],args[3])
            
if __name__ == '__main__':
        sys.exit(main())