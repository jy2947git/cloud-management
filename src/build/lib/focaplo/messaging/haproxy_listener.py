#!/usr/bin/python
'''
Created on May 26, 2010

@author: jy2947
'''
import sys
import traceback
import getopt
import focaplo.haproxy.tools
import simplejson as json
from focaplo.messaging.amqp_listener import Listener
from focaplo.messaging.amqp_sender import Sender
class HaproxyListener(Listener):
    '''
    classdocs
    '''

    def __handle_haproxy__(self, s):
        jobj = json.loads(s);
        print jobj
        hu = focaplo.haproxy.tools.HaproxyUtils()
        res='failed'
        if jobj["command"] == 'add':
            if jobj['configdir']:
                res=hu.addRouting(jobj["subdomain"], jobj["host"], jobj["port"], jobj['configdir'])
            else:
                res=hu.addRouting(jobj["subdomain"], jobj["host"], jobj["port"])
        elif jobj["command"] == 'remove':
            if jobj['configdir']:
                res=hu.removeRouting(jobj["subdomain"], jobj['configdir'])
            else:
                res=hu.removeRouting(jobj["subdomain"])
        elif jobj["command"] == 'regenerate':
            #regenerate the haproxy configuration file
            if jobj['configdir'] and jobj['configfile']:
                res=hu.reconfig(jobj['configfile'],jobj['configdir'])
            else:
                res=hu.reconfig()
        elif jobj["command"] == 'display':
            #display haproxy.cfg
            res= hu.getCurrentConfiguration()
        elif jobj["command"] == 'reload':
            res=hu.hotReconfiguration()
        else:
            res="unsupported command:" + jobj["command"]
        #return json with incoming and output
        print res
        return json.dumps({"incoming":s,"result":res},sort_keys=True)
        
    def __callback_reconfigure_haproxy__(self,msg):
        print 'received:' + msg.body + ' from channel:' + str(msg.channel.channel_id)
        res='failed'
        try:
            jobj = json.loads(msg.body);
            res = self.__handle_haproxy__(msg.body)
        except:
            print("error:",sys.exc_info()[0])
            traceback.print_exc();
        finally:
            #send result back to queue
            if "replyTo" in jobj:
                s=Sender()
                s.send(jobj["replyToHost"], jobj["replyToPort"], jobj["replyToUser"], jobj["replyToPassword"], jobj["replyToVirtualHost"], jobj["replyToExchange"], jobj["replyToRoutingKey"], res)

    def startHaproxyListener(self,host, port, user, password):
        print 'starting haproxy reconfiguration listener...' + host +' ' + port + "haproxy - incoming - configuration"
        self.listen(host, port, user, password, "/", "haproxy", "incoming", "configuration", self.__callback_reconfigure_haproxy__)

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
        print 'usage: HaproxyListener host port user password'
        sys.exit(2)
    if len(args) != 4:
        print 'usage: HaproxyListener host port user password'
        sys.exit(2)

    c=HaproxyListener()
    c.startHaproxyListener(args[0],args[1],args[2],args[3])
        
if __name__ == '__main__':
    sys.exit(main()) 