#!/usr/bin/env python2.7
# version 0.4 - programmes d'optimisation
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
    LOG_FILENAME = "/var/log/clonage_a_chaud/clone_src_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour lecture par bit de sda1
    logging.debug("Ouverture pour lecture par bit de sda1")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    os.lseek(fh_src.fileno(), 0, os.SEEK_SET)    #sic = os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    aux = fh_src.read(2048*512)
    ## DEBUG
    logging.debug("que vaut aux ? : %s" % aux)
    
    ### Ouverture du fichier 'code_hash' en lecture seule
    hash_path = "/windows/prog_dev/prog_clone_optimisation/code_hash"
    hash = open(hash_path, "r")
    
    logging.debug("Ecriture sur disque destination")
    logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    while aux != '':
    #while aux != '' and sic < 1024*2048*512+1 :
        logging.info("Lecture des hash_blocks")
        #hash_src = hashlib.sha1(aux).digest()
        #hash_src = sys.stdin.read(20)
        hash_src = hash.read(20)
        sys.stdout.write(hash_src)
        sys.stdout.flush()
        logging.debug(binascii.hexlify(hash_src))
        
        msg = sys.stdin.read(4)
        if len(msg) != 4 :
            logging.error("Error clone_src_main 1")
            break
        if msg == 'next' :
            logging.info("Passage au bloc suivant")
        elif msg == 'sent':
            logging.info("Envoi du bloc")
            sys.stdout.write(aux)
            sys.stdout.flush()
            hash_src = hash.read(20)
            #hash_src = hash.read("\n")
        else:
            logging.debug("valeur de 'msg' : %s" % msg)
            logging.error("Error clone_src_main 2")
            break
        #sic = os.lseek(fh_src.fileno(), 1, os.SEEK_CUR)
        aux = fh_src.read(2048*512)
        #hash_src += hash.read(20)
    
    sys.stdin.close()
    sys.stdout.close()
    fh_src.close()
    logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")

if __name__ == '__main__':
    main()
