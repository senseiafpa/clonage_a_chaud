#!/usr/bin/env python2.7

import sys, os, logging, hashlib, binascii

def main():
    LOG_FILENAME = "/tmp/test_read-code_hash.log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
    logging.debug("Test lecture du hash par ligne dans 'code_hash' ")
    
    lig = 1
    lig_tot = os.system("wc -l code_hash")
    logging.info("-------------------------------------------")
    logging.info("Ouverture du fichier 'code_hash' ")
    logging.info("-------------------------------------------")
    with open('code_hash', 'r') as fichier_hash:
        #for lig in (1, os.system("wc -l code_hash")+1):
        while lig <= lig_tot :
            hash_src = fichier_hash.read()
            sys.stdout.write(hash_src)
            sys.stdout.flush()
            logging.debug(binascii.hexlify(hash_src))
    logging.info("-------------------------------------------")
    logging.info("Fermeture du fichier 'code_hash' ")
    logging.info("-------------------------------------------")

if __name__ == '__main__':
    main()
