#!/usr/bin/python
'''
Created on May 24, 2010

@author: jy2947
'''
import sys
import traceback
from amqplib import client_0_8 as amqp
import getopt
class Listener(object):
    '''
    classdocs
    '''
    def printMessage(self, message):
        print message.body
        
        
        
    def startSimpleListener(self, host, port="5672", user="guest", password="guest", virtualhost="/", exchange="temp", queue="test_queue", routingkey="test"):
        print 'starting listener...at ' + host + ' ' + port + ' ' + queue
        self.listen(host, port, user, user, virtualhost, exchange,queue, routingkey, self.printMessage);

        
    def listen(self, host, port, user, password, virtualhost, exchange, queue, routingkey, callback):
        conn = None
        chan = None
        try:
            conn = amqp.Connection(host=host+":"+port,userid=user,password=password,virtual__host=virtualhost, insist=False)
            chan=conn.channel()
            
            chan.queue_declare(queue=queue, durable=True, exclusive=False,auto_delete=False)
            chan.exchange_declare(exchange=exchange, type="direct", durable=True,auto_delete=False)
            chan.queue_bind(queue=queue, exchange=exchange,routing_key=routingkey)
            #recv_callback=self.recv_callback
            
            chan.basic_consume(queue=queue, no_ack=True, callback=callback, consumer_tag=queue+"consumer")
            while True:
                chan.wait()
            chan.basic_cancel(queue+"consumer")
        except:
            print("error:",sys.exc_info()[0])
            traceback.print_exc();
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
        print 'usage: Listener host port user password'
        sys.exit(2)
    if len(args) < 2:
        print 'usage: Listener host port [user password virtualhost exchange queue routingkey] '
        sys.exit(2)

    c=Listener()
    #c.startSimpleListener(args[0],args[1],args[2],args[3], args[4], args[5],args[6], args[7])
    c.startSimpleListener(args[0],args[1])
if __name__ == '__main__':
    sys.exit(main()) 