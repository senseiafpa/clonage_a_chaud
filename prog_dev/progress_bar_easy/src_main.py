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


import select, subprocess, sys
import logging, hashlib, binascii
import iprange2, argparse, os


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
    LOG_FILENAME = "/var/log/clonage_a_chaud/src_main.log"
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.WARN,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s  %(levelname)s  %(funcName)s  %(message)s')
    #############################################################################################################################################
    
    
    #############################################################################################################################################
    ### Arguments obligatoires à récupérer par l'utilisateur pour procéder au clonage des machines destinataires définies par une IP Range
    #############################################################################################################################################
#    version=1.0
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--ipmotif", dest="ipmotif", required="Motif d'adresse IP", help="Motif d'adresse IP", action="store")
    #parser.add_argument("-ipe", "--ipend", dest="ipend", required="Adresse IP fin de plage", help="Adresse IP de fin de la plage", action="store")
    parser.add_argument("-p", "--destpart", dest="partdest", required="Partition Destinataire", help="la partition destinataire à cloner", action="store")
    parser.add_argument("-v", "--verbose", action="store_true", help="mode verbeux")
#    parser.add_argument("-V", "--version", dest="version", action="store_true", help="affiche la version du programme")
    args = parser.parse_args()
    ip_motif = args.ipmotif
    dest_part = args.partdest
    logging.info("Partition destinataire : %s " % dest_part)
    iprange = iprange2.IPRange()
    listIP = iprange.run(ip_motif)
    clients = {}
    poller = select.epoll()
    for ip in listIP:
#	p = subprocess.Popen(['ssh', ip, 'python /usr/local/bin/dest_main.py -p %s' % dest_part], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True) # Version finale de clonage multiposte
	p = subprocess.Popen(['ssh', ip, 'python /media/OS/Users/Jonathan/Desktop/Partages-NFS_Dev-Python/prog_dev/progress_bar_easy/dest_main.py -p %s' % dest_part], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
#      p = subprocess.Popen(['yes'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True) # Test Sample for implementation function epoll with socket  # Test fonctionne avec 'yes' mais pas avec 'ssh' ...
        (fh_in, fh_out) = (p.stdout, p.stdin)
    	clients[fh_in.fileno()] = (fh_in, fh_out, ip, 0)
        logging.info("fh_in : %s"%fh_in)
        poller.register(fh_in)
    #############################################################################################################################################
    
    
    #############################################################################################################################################
    ### Ouverture pour lecture par bit de sda1
    #############################################################################################################################################
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
    #############################################################################################################################################


    #############################################################################################################################################
    ### Implementation de 'epoll()' - utilisation multicast par tuple '(src_in,src_out)=(dst_out,dst_in)'
    #############################################################################################################################################
    try:
        while True:
            events = poller.poll(1)
            
            i = 0
            with open('code_hash', 'r') as fichier_hash:
                hash_src = fichier_hash.read(20)
                while aux != '':
                    logging.info("Lecture des hash_blocks")
                    fh_out.write(hash_src)
                    fh_out.flush()
                    logging.debug(binascii.hexlify(hash_src))
                    msg = fh_in.read(5)
                    logging.debug("msg = %s"%msg)
                    if len(msg) != 5 :
                        logging.error("Error src_main 1")
                        break
                    if [ events == [] ]:
                        logging.warn("ERROR !!")
                        break
                    
                    ### Problème avec events -> fileno, event - aucun évènement
                    ### 'events' is null ...
                    logging.debug("events : %s"%events)
                    ##### TEST DEBUG 1 
                    logging.info("TEST DEBUG 1 : %s"%poller)  ## Test passé
                    ##### FIN TEST DEBUG 1 
                    for fileno, event in events:
                        ##### TEST DEBUG 2 
                        logging.info("TEST DEBUG 2 : %s"%poller)  ## Echec du test
                        ##### FIN TEST DEBUG 2 
                        (fichier_hash, fh_out, ip, current_block) = clients[fileno]
                        if event & select.EPOLLIN:
                            msg = fichier_hash.read(5)
                            res = process_msg(msg, fh_out, ip, current_block, fh_src)
                            if res != 0:
                                break
                            current_block += 1
                            clients[fileno] = (fichier_hash, fh_out, ip, current_block)
                        else:
                            logging.debug("Evènement %i non géré"%event)
                    hash_src = fh_in.read(20)
            i += 1

    finally:
        logging.debug("Close all sockets")
        for fileno in clients:
            fh_in = clients[fileno][0]
            poller.unregister(fh_in)
            fh_in.close()
        poller.close()
    
    fh_in.close() # fd -> read data clients
    fh_out.close() # fd -> write data clients per processes
    fh_src.close() # fd -> read data master source
    #logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    logging.warn("Clonage disque fini. Merci d'avoir attendu patiemment")
    #############################################################################################################################################


def process_msg(msg, fh_out, ip, current_block, fh_src):
    logging.warn("Reçu de %s(%i) : %s"%(ip,current_block,msg))  ## Message test - affichage dans les logs si bien reçu
    if msg == 'next\n' :
        logging.info("Passage au bloc suivant")
    elif msg == 'sent\n':
        logging.info("Envoi du bloc")
        sic = os.lseek(fh_src.fileno(), i*2048*512, os.SEEK_SET)
        if sic != i*2048*512:
            logging.error("os.lseek(fh_src...) error")
            res=1
        aux = fh_src.read(2048*512)
        if aux == '':
            logging.error("fh_src.read() error")
            res=1
        res = fh_out.write(aux)
        fh_out.flush()
        logging.debug("fh_out.write(aux)=> %i"%res)
        res=0
    else:
        logging.debug("valeur de 'msg' : %s" % msg)
        logging.error("Error src_main 2")
        res=1
    res=0
    return res


if __name__ == '__main__':
    main()

