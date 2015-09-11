#!/usr/bin/env python2.7
# v 0.1 prod

import os, sys, logging

def main():
    ### Creation des logs
    LOG_FILENAME = "/var/log/clone_part.log"
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
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de cloner le disque")
    while aux != '':
        fh_dest.write(aux)
        aux = fh_src.read(2048*512)

if __name__ == '__main__':
    main()
