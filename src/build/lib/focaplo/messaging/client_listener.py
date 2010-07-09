#!/usr/bin/python
'''
Created on May 26, 2010

@author: jy2947
'''
import sys
import traceback
import getopt
import simplejson as json
from focaplo.messaging.amqp_listener import Listener
from focaplo.messaging.amqp_sender import Sender
from focaplo.bime.datasource import DataSourceUtils
class ClientListener(Listener):
    '''
    classdocs
    '''
            
    def __handle_client__(self, s):
        jobj = json.loads(s);
        print jobj
        res=None
        d = DataSourceUtils();
        if jobj["command"] == 'add':
            res=d.add_new_client(jobj['config_dir'], jobj['host'], jobj['databaseName'], jobj['password'],jobj['autoid'], jobj['adminemail'], jobj['adminfullname'], jobj['adminencryptedpassword'], jobj['template_dir'])
        elif jobj["command"] == 'remove':
            res=d.remove_datasource(jobj['config_dir'],jobj['databaseName'])
        else:
            res="unsupported command:" + jobj["command"]
        print 'message processed'
        #return json with incoming and output
        return json.dump({"incoming":s,"result":res})

            
    def __callback_update_client__(self,msg):
        print 'received:' + msg.body + ' from channel:' + str(msg.channel.channel_id)
        res=None
        try:
            jobj = json.loads(msg.body);
            res=self.__handle_client__(msg.body)
                        
        except:
            res="failed"
            traceback.print_exc();
        finally:
            #send result back to queue
            if "replyTo" in jobj:
                s=Sender()
                s.send(jobj["replyToHost"], jobj["replyToPort"], jobj["replyToUser"], jobj["replyToPassword"], jobj["replyToVirtualHost"], jobj["replyToExchange"], jobj["replyToRoutingKey"], res)

    
    def startBimeClientListener(self,host, port, user, password):
        print 'starting bime client listener on ' + host +':' + port+'...'
        self.listen(host, port, user, password, "/", "client", "incoming", "datasource", self.__callback_update_client__)


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
        print 'usage: ClientListener host port user password'
        sys.exit(2)
    if len(args) != 4:
        print 'usage: ClientListener host port user password'
        sys.exit(2)

    c=ClientListener()
    c.startBimeClientListener(args[0],args[1],args[2],args[3])
        
if __name__ == '__main__':
    sys.exit(main())
        