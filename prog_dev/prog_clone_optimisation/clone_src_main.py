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
    #os.mkdir("/var/log/clonage_a_chaud")
    log_path = "/var/log/clonage_a_chaud"
    try:
        os.stat(log_path)
    except:
        os.mkdir(log_path)
    LOG_FILENAME = "/var/log/clonage_a_chaud/clone_src_main.log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    
    ### Ouverture pour lecture par bit de sda1
    logging.debug("Ouverture pour lecture par bit de sda1")
    src_path = "/dev/sda1"
    fh_src = open(src_path, "rb")
    src_size_disk = os.lseek(fh_src.fileno(), 0, os.SEEK_END)
    logging.debug("Taille disque source : %d" % src_size_disk)
    #os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    sic = os.lseek(fh_src.fileno(), 0, os.SEEK_SET)
    aux = fh_src.read(2048*512)
    
    #logging.debug("Ecriture sur disque destination")
    #logging.info("Merci de bien vouloir patienter le temps de clonage du disque")
    logging.warn("Ecriture sur disque destination")
    
    #while aux != '':
    i = 0
    with open('code_hash', 'r') as fichier_hash:
        hash_src = fichier_hash.read(20)
        while aux != '' and hash_src != '':
            logging.info("Lecture des hash_blocks")
            sys.stdout.write(hash_src)
            sys.stdout.flush()
            logging.debug(binascii.hexlify(hash_src))
        
            msg = sys.stdin.read(5)
            logging.debug("msg=='%s'"%msg)
            if len(msg) != 5 :
                logging.error("Error clone_src_main 1")
                break
            if msg == 'next\n' :
                logging.info("Passage au bloc suivant")
            elif msg == 'sent\n':
                logging.info("Envoi du bloc")
                sic = os.lseek(fh_src.fileno(), i*2048*512, os.SEEK_SET)
                if sic != i*2048*512:
                    logging.error("os.lseek(fh_src...) error")
                    break
                aux = fh_src.read(2048*512)
                if aux == '':
                    logging.error("fh_src.read() error")
                    break
                sys.stdout.write(aux)
                sys.stdout.flush()
            else:
                logging.debug("valeur de 'msg' : %s" % msg)
                logging.error("Error clone_src_main 2")
                break

            hash_src = fichier_hash.read(20)
            i += 1
    
    sys.stdin.close()
    sys.stdout.close()
    fh_src.close()
    #logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    logging.warn("Clonage disque fini. Merci d'avoir attendu patiemment")

if __name__ == '__main__':
    main()
