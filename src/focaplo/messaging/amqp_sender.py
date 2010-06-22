#!/usr/bin/python
'''
Created on May 24, 2010

@author: jy2947
'''
from amqplib import client_0_8 as amqp
import sys
import traceback
import getopt

class Sender(object):
    '''
    classdocs
    '''
    def send(self, message, host, port="5672", user="guest", password="guest", virtualhost="/", exchange="temp", queue="test_queue", routingkey="test"):
        conn = None
        chan = None
        try:
            conn=amqp.Connection(host=host+":"+port,userid=user,password=password, virtual_host=virtualhost, insist=False)
            chan=conn.channel()
            msg=amqp.Message(message)
            msg.properties["delivery_mode"]=2
            chan.basic_publish(msg,exchange=exchange,routing_key=routingkey)
        except:
            print("error:",sys.exc_info()[0])
            traceback.print_exc()
            raise
        finally:
            if chan is not None:
                chan.close()
            if conn is not None:
                conn.close()

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
        print 'usage: Sender host port user password virtualhost exchange queue routingkey message'
        sys.exit(2)
    if len(args) < 2:
        print 'usage: Sender message host [port user password virtualhost exchange queue routingkey message]'
        sys.exit(2)

    c=Sender()
    #c.send(args[0],args[1],args[2],args[3], args[4], args[5],args[6], args[7], args[8])
    c.send(args[0], args[1])   
if __name__ == '__main__':
    sys.exit(main()) 