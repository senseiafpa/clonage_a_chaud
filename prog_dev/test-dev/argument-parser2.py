#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# version 0.1 - programmes de gestion d'adresses IPs
#               utilisation du parser d'arguments
#                   pour gérer les options obligatoires
# 
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
# 	Tuteur de stage : Sylvain Antoine <santoine@univ-jfc.fr>
#	SysAdmin	: Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
#
# Ce programme a été écrit par Jonathan Viandier pour une éventuelle 
# amélioration du système de clonage des machines clientes,
# au sein de l'Université Jean-Francois Champollion.

import sys, os, logging, hashlib, binascii
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ipb", "--ipbegin", dest="ipbegin", required="Adresse IP début de plage", help="Adresse IP du début de la plage", action="store")
    parser.add_argument("-ipe", "--ipend", dest="ipend", required="Adresse IP fin de plage", help="Adresse IP de fin de la plage", action="store")
    parser.add_argument("-v", "--verbose", action="store_true", help="Augmente la verbosité")
    args = parser.parse_args()
    
    ipbegin = args.ipbegin
    ipend = args.ipend
    
    print("Plage IP : %s - %s" % (ipbegin, ipend))

if __name__ == '__main__':
    main()
