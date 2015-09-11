#!/usr/bin/env python2.7

import sys, os, logging

def main():
	LOG_FILENAME = "/tmp/test.log"
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

	print "toto"
	logging.debug("Test de lecture du stdout en entree du cat")
	rd = sys.stdin.read(4)
#	sys.stdin.readline()
	logging.debug("rd : %s" % rd)

if __name__ == '__main__':
    main()
