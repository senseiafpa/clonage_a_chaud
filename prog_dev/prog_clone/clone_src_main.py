#!/usr/bin/env python2.7
# v 0.3

import os, sys, logging

def main():
    ### Creation des logs
    LOG_FILENAME = "/var/log/clone_src_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour lecture par bit de sda1
    logging.debug("Ouverture pour lecture par bit de sda1")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    aux = fh_src.read(2048*512)
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    while aux != '':
        sys.stdout.write(aux)
        aux = fh_src.read(2048*512)
    sys.stdout.close()
    fh_src.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")

if __name__ == '__main__':
    main()
