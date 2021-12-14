import modules.controller as controller
import argparse
import signal
import threading
import sys


def main():
    args = argumentParser()
    controller.Control().main(args.TESTCYCLES, args.FILENAME)

def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--testcycles',dest = "TESTCYCLES", help = "Test cycles", default = 5)
    parser.add_argument('-f', '--filename', dest = "FILENAME", help = "File name",default = "OpenVPN_report")
    args = parser.parse_args()
    return args

def ctrlc_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, ctrlc_handler)
forever = threading.Event()

if __name__ == "__main__":
    main()