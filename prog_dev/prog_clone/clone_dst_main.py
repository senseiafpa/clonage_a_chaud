#!/usr/bin/env python2.7
# v 0.3

import os, sys, logging

def main():
    ### Creation des logs
    LOG_FILENAME = "/var/log/clone_dst_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour ecriture par bit de sdb1
    logging.debug("Ouverture pour ecriture par bit de sdb1")
    dest_path = "/dev/sdb1"
    fh_dest = open(dest_path, "wb")
    dest_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque destination : %d" % dest_size_disk)
    dst_size_disk = os.lseek(fh_dest.fileno(), 0, os.SEEK_SET)
    aux = sys.stdin.read(2048*512)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    while aux != '':
        fh_dest.write(aux)
        aux = sys.stdin.read(2048*512)
    fh_dest.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")

if __name__ == '__main__':
    main()
