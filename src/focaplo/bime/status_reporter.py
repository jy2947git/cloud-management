#!/usr/bin/python
'''
Created on Jun 18, 2010

@author: jy2947
'''
import json
import focaplo.messaging.amqp_sender
import focaplo.os.util
import os
import logging
import time
import traceback
import sys
import getopt
import socket
class StatusReporter(object):
    '''
    classdocs
    '''
    curr_dir = os.getcwd()
    logfile = os.path.join(curr_dir, 'test_daemon.log')
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    
    def collect(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(socket.gethostname())
        msg = json.dumps({"name":hostname, "privateip":ip,"public_ip":ip},sort_keys=True)
        return msg
    
    def report(self,host, port, user, password):
        logging.debug('report status to ' + host + ' ' + port)
        try:

            sender = focaplo.messaging.amqp_sender.Sender()
            logging.info(self.collect())
            sender.send(host, port, user, password, "/", "bime", "server_status", msg)
        except:
            logging.error("error:",sys.exc_info()[0])
            traceback.print_exc()
        
    def start_report_daemon(self,host, port, user, password):
        print 'report daemon...'

        print 'logged to ' + self.logfile
        focaplo.os.util.daemonize()
        logging.info('starting')
        logging.debug('current directory is %s' % os.getcwd())
        
        while True:
            try:
                logging.debug("daemon reporting...")
                self.report(host, port, user, password)
                #logging.debug('report status to ' + host + ' ' + port)
                #try:
                #    hostname = socket.gethostname()
                #    ip = socket.gethostbyname(socket.gethostname())
                #    msg = json.dumps({"name":hostname, "privateip":ip,"public_ip":ip},sort_keys=True)
                #    sender = focaplo.messaging.amqp_sender.Sender()
                #    logging.info(msg)
                #    sender.send(host, port, user, password, "/", "bime", "server_status", msg)
                #except:
                #    logging.error("error:",sys.exc_info()[0])
                #    traceback.print_exc()
                time.sleep(60)
            except:
                logging.error("error:",sys.exc_info()[0])
                traceback.print_exc()
                time.sleep(60)
                continue
            


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
    
        
        reporter=StatusReporter()
        reporter.start_report_daemon(args[0],args[1],args[2],args[3])
            
if __name__ == '__main__':
        sys.exit(main())