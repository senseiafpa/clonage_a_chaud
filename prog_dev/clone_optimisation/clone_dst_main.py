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
    #os.mkdir("/var/log/clonage_a_chaud")
    log_path = "/var/log/clonage_a_chaud"
    try:
        os.stat(log_path)
    except:
        os.mkdir(log_path)
    LOG_FILENAME = "/var/log/clonage_a_chaud/clone_dst_main.log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour ecriture par bit de sdb1
    logging.debug("Ouverture pour ecriture par bit de sdb1")
    #dest_path = "/dev/sdb1"
    dest_path = "/tmp/sdb1"
    fh_dest = open(dest_path, "r+b")
    
    logging.debug("fd==%i"%fh_dest.fileno())
    dest_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque destination : %d" % dest_size_disk)
    os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    #sic = os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    logging.warn("Ecriture sur disque destination")
    
    i=0
    aux_dest = fh_dest.read(2048*512)
    while aux_dest != '':
    #while aux_dest != '' and sic < 1024*2048*512+1 :
        hash_dest = hashlib.sha1(aux_dest).digest()
        logging.debug("Attente de lecture du hash_src")
        hash_src = sys.stdin.read(20)
        logging.debug("---------------------------------------")
        logging.debug("hash_src : %s " % binascii.hexlify(hash_src) )
        logging.debug("---------------------------------------")
        logging.debug(binascii.hexlify(hash_src))
        
        if len(hash_src) != 20:
            logging.error("Error dst 1")
            break
        if hash_src != hash_dest:
            logging.info("Ecriture sur bloc")
            sys.stdout.write('sent\n')
            sys.stdout.flush()
            aux_src = sys.stdin.read(2048*512)
            if len(aux_src) != 2048*512:
                logging.error("Error dst 2")
                break
            os.lseek(fh_dest.fileno(), i*2048*512, os.SEEK_SET)
            fh_dest.write(aux_src)
        else:
            logging.info("Passage au bloc suivant")
            sys.stdout.write('next\n')
            sys.stdout.flush()
        aux_dest = fh_dest.read(2048*512)
        logging.debug("len(aux_dest)==%i"%len(aux_dest))
        i += 1

    sys.stdin.close()
    sys.stdout.close()
    fh_dest.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    logging.warn("Clonage disque fini. Merci d'avoir attendu patiemment")

if __name__ == '__main__':
    main()
