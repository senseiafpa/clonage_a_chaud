#!/usr/bin/env python2.7
# version 0.1 - programmes d'optimisation
# 
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
# 	Tuteur de stage : Sylvain Antoine <santoine@univ-jfc.fr>
#	SysAdmin	: Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
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
    LOG_FILENAME = "/var/log/clonage_a_chaud/hash_block.log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s %(levelname)s %(funcName)s %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s %(levelname)s %(funcName)s %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s %(levelname)s %(funcName)s %(message)s')
    
    ### Ouverture pour lecture par bit de la partition sda1
    logging.debug("Ouverture de la partition sda1")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    #os.system('rm code_hash')
    #os.remove('code_hash')
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    #os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    sic = os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    aux = fh_src.read(2048*512)
    
    i=1
    #logging.debug("Commencement du hashage des blocks du disque sda1")
    logging.warn("Commencement du hashage des blocks du disque sda1")
    with open('code_hash', 'w') as fic:
        while aux != '':
        #while aux != '' and i<1024:
            hash_src = hashlib.sha1(aux).digest()
            logging.info("Ecriture des hash-blocks")
            fic.write(hash_src)
            #fic.write("\n")
            logging.debug("block %i : %s"%( i,binascii.hexlify(hash_src) ) )
            #logging.debug("Test de lecture des hash-blocks du fichier")
            #with open('code_hash', 'r') as fic_read:
            #    txt = fic_read.read(20)
            #    logging.info("Hash : %s" % binascii.hexlify(txt))
            logging.info("Passage au bloc suivant")
            aux = fh_src.read(2048*512)
            i += 1
        
    sys.stdout.close()
    fh_src.close()
    #logging.info("Fin du hashage des blocks du disque sda1")
    logging.warn("Fin du hashage des blocks du disque sda1")
    

if __name__ == '__main__':
    main()
