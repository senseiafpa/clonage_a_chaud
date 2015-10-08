#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 
# version 1.0 - programmes d'optimisation avec arguments obligatoires
#
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
#       Tuteur de stage        : Sylvain Antoine <santoine@univ-jfc.fr>
#       Administrateur Système : Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
#
# Ce programme a été écrit par Jonathan Viandier pour une éventuelle 
# amélioration du système de clonage des machines clientes,
# au sein de l'Université Jean-Francois Champollion.


import os, sys, logging, hashlib, binascii
import argparse



def main():
    #############################################################################################################################################
    ### Creation des logs
    #############################################################################################################################################
    #os.mkdir("/var/log/clonage_a_chaud")
    log_path = "/var/log/clonage_a_chaud"
    try:
        os.stat(log_path)
    except:
        os.mkdir(log_path)
    LOG_FILENAME = "/var/log/clonage_a_chaud/dest_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #############################################################################################################################################

    
    #############################################################################################################################################
    ### Arguments obligatoires à récupérer par l'utilisateur pour procéder au clonage des machines destinataires définies par une IP Range
    #############################################################################################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--dest_part", dest="partdest", required="Partition Destinataire", help="la partition destinataire à cloner", action="store")
    parser.add_argument("-v", "--verbose", action="store_true", help="Augmente le mode verbeux")
    #parser.add_argument("-V", "--version", action="store_true", help="Affiche la version du programme")
    version=1.0
    args = parser.parse_args()
    
    dest_part = args.partdest
    
    logging.info("Partition destinataire : %s " % dest_part)
    #############################################################################################################################################
    
    
    #############################################################################################################################################
    ### Ouverture pour ecriture par bit de sdb1
    #############################################################################################################################################
    logging.debug("Ouverture pour ecriture par bit de sdb1")
    #dest_path = "/dev/sdb1"
    #dest_path = "/tmp/sdb1"
    dest_path = dest_part
    fh_dest = open(dest_path, "r+b")
    
    logging.debug("fd==%i"%fh_dest.fileno())
    dest_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque destination : %d" % dest_size_disk)
    os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    #sic = os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    #logging.warn("Ecriture sur disque destination")
    
#    sys.stdout.write("hello")
#    sys.stdout.flush()
    
    i=0
    aux_dest = fh_dest.read(2048*512)
    while aux_dest != '':
        hash_dest = hashlib.sha1(aux_dest).digest()
        logging.debug("Attente de lecture du hash_src")
        hash_src = sys.stdin.read(20)
        logging.debug("---------------------------------------")
        logging.debug("hash_src : %s " % binascii.hexlify(hash_src) )
        logging.debug("---------------------------------------")
#        logging.debug(binascii.hexlify(hash_src))
        
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
            fh_dest.flush()
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
    #logging.warn("Clonage disque fini. Merci d'avoir attendu patiemment")
    #############################################################################################################################################

if __name__ == '__main__':
    main()

