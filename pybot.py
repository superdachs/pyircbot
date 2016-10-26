#!/usr/bin/env python

import daemonize
import sys
import os
from time import sleep

class PyBot:

    def __init__(self):
        self.terminate = False
        pass

    def main(self):
        
        with open("/etc/pybot/pybot.conf", "r") as configfile:
            pass

        self.loop()

    def loop(self):
        print("entering main loop")
        while not self.terminate:
            print("beep")
            sleep(1)

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




