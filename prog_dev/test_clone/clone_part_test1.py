#!/usr/bin/env python2.7
# v 0.1

import os, sys, logging

def main():
    LOG_FILENAME = "/tmp/clone_part_test.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')

    logging.debug("Starting clonage")
    ## commande systeme clonage part sda1 dans fic_test1.txt
    val1 = os.system("dd if=/dev/sda of=/windows/clonages_test/fic_test1.txt count=102400")
    print val1
    logging.info("Info test clonage")
    
    logging.debug("Ordonnancement dans fic_test1.txt")
    ## commande systeme ordonnancement du fichier de sortie
    ordo_val1 = os.system("hd /windows/clonages_test/fic_test1.txt > /windows/clonages_test/ordo_fic_test1.txt")
    logging.info("Info test ordo")
    
    logging.debug("Test de copie dans le 2eme disque")
    ## commande systeme creation de disque par copie
    #cp_val1 = os.system("dd if=/windows/clonages_test/ordo_fic_test1.txt of=/dev/sdb1")
    cp_val1 = os.system("dd if=/windows/clonages_test/fic_test1.txt of=/dev/sdb")
    logging.info("Info copy fic --> /dev/sdb")
    
    

if __name__ == '__main__':
    main()
