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
    LOG_FILENAME = "/var/log/clone_dst_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour ecriture par bit de sdb1
    logging.debug("Ouverture pour ecriture par bit de sdb1")
    dest_path = "/dev/sdb1"
    fh_dest_read = open(dest_path, "rb")
    fh_dest_write = open(dest_path, "wb")
    
    dest_size_disk = os.lseek(fh_dest_write.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque destination : %d" % dest_size_disk)
    os.lseek(fh_dest_write.fileno(), 0, os.SEEK_SET)
    aux_dest = fh_dest_read.read(2048*512)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    while aux_dest != '':
        hash_dest = hashlib.sha1(aux_dest).digest()
        logging.debug("Attente de lecture du hash_src")
        hash_src = sys.stdin.read(20)
        logging.debug(binascii.hexlify(hash_src))
        
        if len(hash_src) != 20:
            logging.error("Error dst 1")
            break
        if hash_src != hash_dest:
            logging.info("Ecriture sur bloc")
            sys.stdout.write('sent')
            sys.stdout.flush()
            aux_src = sys.stdin.read(2048*512)
            fh_dest_write.write(aux_src)
        else:
            logging.info("Passage au bloc suivant")
            sys.stdout.write('next')
            sys.stdout.flush()
            os.lseek(fh_dest_write.fileno(), 2048*512, os.SEEK_CUR)
        aux_dest = fh_dest_read.read(2048*512)
    sys.stdin.close()
    sys.stdout.close()
    fh_dest_read.close()
    fh_dest_write.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    

if __name__ == '__main__':
    main()
