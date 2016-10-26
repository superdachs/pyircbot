#!/usr/bin/env python

import daemonize
import sys
import os
from time import sleep
import signal
import irc
from irc import client

class PyBot:

    def __init__(self):
        self.terminate = False
        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGQUIT, self.cleanup)

    def terminate(self):
        self.terminate = True

    def cleanup(self, *args, **kwargs):
        print("cleaning up.")
        # do stuff
        os._exit(0)        

    def main(self):
        
        with open("/etc/pybot/pybot.conf", "r") as configfile:
            pass


        # testcode
        # TODO: build up structure holding connection to multiple servers
        #       and add handlers

        server = "192.168.16.61"
        port = 6667
        nick = "PyBotDev"

        reactor = irc.client.Reactor()

        c = reactor.server().connect(server, port, nick)
        def on_connect(connection, event):
            connection.join("#Dachsbau")

        def on_message(connection, event):
            print(event)

        c.add_global_handler("welcome", on_connect)
        c.add_global_handler("message", on_message)

        reactor.process_forever()

        # end of testcode

        self.loop()

    def loop(self):
        print("entering main loop")
        while not self.terminate:
            print("beep")
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





