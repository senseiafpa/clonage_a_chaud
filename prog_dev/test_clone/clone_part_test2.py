#!/usr/bin/env python2.7
# version 0.2 - programmes d'optimisation
# 
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
#       Tuteur de stage : Sylvain Antoine <santoine@univ-jfc.fr>
#       SysAdmin        : Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
# 
# Ce programme a ete ecrit par Jonathan Viandier pour une amelioration du
# systeme de clonage des machines de chaque salle de TP, au sein de l'Uni
# versite Jean-Francois Champollion.

import os, sys, logging

def main():
    ### Creation des logs
    LOG_FILENAME = "/tmp/clone_part_test2.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Test de clonage de sda1
    logging.debug("Starting clonage")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    
    dest_path = "/dev/sdb1"
    fh_dest = open(dest_path, "wb")
    dest_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque destination : %d" % dest_size_disk)
    
    if dest_size_disk < src_size_disk:
        logging.debug("Erreur !! La taille de la partition de destination est plus petite que celle de la source !!")
        logging.debug("Merci de resoudre le probleme avant de relancer le clonage a chaud !")
        os._exit(1)
    os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    dst_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    
    aux = fh_src.read(2048*512)
    logging.debug("Contenu de aux : %s" % aux)

    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de cloner le disque")
    while aux != '':
        fh_dest.write(aux)
        aux = fh_src.read(2048*512)

if __name__ == '__main__':
    main()
