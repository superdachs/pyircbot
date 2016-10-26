#!/usr/bin/env python

import daemonize
import sys
import os
from time import sleep
import signal
import irc
from irc import client
import threading

class PyBot:

    class Connection:

        def __init__(self, server, port, nick, channels, private_message_handler, public_message_handler):
            self.reactor = irc.client.Reactor()
            self.c = self.reactor.server().connect(server, port, nick)
            self.channels = channels

            self.c.add_global_handler("welcome", self.on_connect)
            self.c.add_global_handler("privmsg", private_message_handler)
            self.c.add_global_handler("pubmsg", public_message_handler)
            
            self.thread = threading.Thread(target=self.reactor.process_forever)
            self.thread.start()


        def on_connect(self, connection, event):
            print("connected")
            for channel in self.channels:
                print("joining %s" % channel)
                connection.join(channel)

    def __init__(self):
        self.terminate = False

        self.connections = []

        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGQUIT, self.cleanup)

    def private_message_handler(self, connection, event):
        self.send_private_message(connection, event.source.split("!")[0], self.compute_answer(event.arguments[0]))

    def public_message_handler(self, connection, event):
        print(event)

    def send_private_message(self, connection, nick, text):
        connection.privmsg(nick, text)

    def compute_answer(self, text):
        answer = "Ich hab keine Ahnung was du von mir willst!öäü"
        #TODO: use google for answer
        return answer

    def terminate(self):
        self.terminate = True

    def cleanup(self, *args, **kwargs):
        print("cleaning up.")
        # do stuff
        os._exit(0)        

    def main(self):
        
        with open("/etc/pybot/pybot.conf", "r") as configfile:
            pass

        con = self.Connection("192.168.16.61", 6667, "PyBotDev", ["#Dachsbau", "#Holda"], self.private_message_handler, self.public_message_handler)


        self.loop()

    def loop(self):
        print("entering main loop")
        while not self.terminate:
            sleep(1)
        self.cleanup()

if __name__ == "__main__":
   
    def usage():
        print("usage: pybot.py [-h|--help] start|stop|restart|foreground")
        sys.exit(1)

    mode = ""

    def start():
        print("starting pybot")
        daemonize.Daemonize(app="pybot", pid="/tmp/pybot.pid", action=PyBot().main).start()

    def stop():
        print("stopping pybot")
        if not os.path.exists("/tmp/pybot.pid"):
            print("not running")
            return
        with open("/tmp/pybot.pid", "r") as pidfile:
            os.system('kill -15 %s' % pidfile.read())

    def restart():
        stop()
        start()

    def foreground():
        print("starting in foreground")
        PyBot().main()

    try:
        mode = sys.argv[1]
    except IndexError:
        usage()

    if mode == "-h" or mode == "--help":
        usage()
    elif mode == "foreground":
        foreground()
    elif mode == "start":
        start()
    elif mode == "stop":
        stop()
    elif mode == "restart":
        restart()
    else:
        usage()





