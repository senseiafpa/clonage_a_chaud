#!/usr/bin/env python2.7
# version 0.4 - programmes d'optimisation
#
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
#       Tuteur de stage : Sylvain Antoine <santoine@univ-jfc.fr>
#       SysAdmin        : Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
# 
# Ce programme a ete ecrit par Jonathan Viandier pour une amelioration du
# systeme de clonage des machines de chaque salle de TP, au sein de l'Uni
# versite Jean-Francois Champollion.

import os, sys, logging, hashlib, binascii

def main():
    ### Creation des logs
    LOG_FILENAME = "/var/log/clone_src_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour lecture par bit de sda1
    logging.debug("Ouverture pour lecture par bit de sda1")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    aux = fh_src.read(2048*512)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    while aux != '':
        hash_src = hashlib.sha1(aux).digest()
        sys.stdout.write(hash_src)
        sys.stdout.flush()
        logging.debug(binascii.hexlify(hash_src))
        
        msg = sys.stdin.read(4)
        if len(msg) != 4 :
            logging.error("Error src 1")
            break
        if msg == 'next' :
            logging.info("Passage au bloc suivant")
        elif msg == 'sent':
            logging.info("Envoi du bloc")
            sys.stdout.write(aux)
            sys.stdout.flush()
        else:
            logging.debug("valeur de 'msg' : %s" % msg)
            logging.error("Error src 2")
            break
        aux = fh_src.read(2048*512)
    
    sys.stdin.close()
    sys.stdout.close()
    fh_src.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    

if __name__ == '__main__':
    main()
