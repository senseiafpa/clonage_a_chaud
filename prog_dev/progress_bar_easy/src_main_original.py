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

import select, subprocess, time
import errno, fcntl, socket
import os, sys, signal
import logging, hashlib, binascii
import iprange2, argparse


def main():
    #############################################################################################################################################
    ### Creation des logs
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
    #version = 1.0
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--ipmotif", dest="ipmotif", required="Motif d'adresse IP", help="Motif d'adresse IP", action="store")
    #parser.add_argument("-ipe", "--ipend", dest="ipend", required="Adresse IP fin de plage", help="Adresse IP de fin de la plage", action="store")
    parser.add_argument("-p", "--destpart", dest="partdest", required="Partition Destinataire", help="la partition destinataire à cloner", action="store")
    parser.add_argument("-v", "--verbose", action="store_true", help="mode verbeux")
    #parser.add_argument("-V", "--version", action="store_true", help="affiche la version du programme")
    args = parser.parse_args()
    
    ip_motif = args.ipmotif
    dest_part = args.partdest
    
#    print("Plage IP : %s - %s" % (ip_begin, ip_end))
    print("Partition destinataire : %s " % dest_part)
    
    iprange = iprange2.IPRange()
    listIP = iprange.run(ip_motif)
    p_stdin = []
    p_stdout = []
    for ip in listIP:
#        print ip
#	p = subprocess.Popen(['ssh', ip, 'python /usr/local/bin/dest_main.py -p %s' % dest_part], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
#	p = subprocess.Popen(['ssh', ip, 'python /media/OS/Users/Jonathan/Desktop/Partages-NFS_Dev-Python/prog_dev/progress_bar_easy/dest_main.py -p %s' % dest_part], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
	p = subprocess.Popen(['yes'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
	p_stdin.append(p.stdin)
	p_stdout.append(p.stdout)
	
    
    #############################################################################################################################################
    
    
    #############################################################################################################################################
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
    
    ### Parametrage de 'epoll()'
    poller_stdin = select.epoll()
    poller_stdout = select.epoll()
    
    for ipd_fh in p_stdout:
        poller_stdout.register(ipd_fh.fileno())#, select.EPOLLIN)
        logging.debug("ipd_fh : %i" % ipd_fh.fileno())
    
    n=0
    while True:
        events = poller_stdout.poll(1)
        logging.debug("events : %s"%events)
        for fileno, event in events:
            try:
                if event & select.EPOLLIN:
                    msgr = os.read(fileno, 5)
                    logging.debug("message fileno : %s %i"%(msgr,fileno))

#                    poller_stdin.poll(p_stdin)
#                elif event & select.EPOLLOUT:
#                    msgw = os.write(fileno, ' ')
#                    logging.debug("message fileno : %s %i"%(msgw,fileno))
#                    poller_stdin.epoll_out(p_stdin)
            except socket.error, err:
                debug('epoll event exception : %s', err)
                if err.errno == 11: # Catch the Errno
                    pass
                else:
                    raise
    
        #while aux != '':
#        i = 0
#        with open('code_hash', 'r') as fichier_hash:
#            fd = poller_stdin.fileno()
#            print "number of file descriptor : %d" % fd
#            Nfd = 0
#            for Nfd in range(fd):
#                print poller_stdin(n_fd)
#                print poller_stdin.fromfd(Nfd)
#                Nfd += 1
#            hash_src = fichier_hash.read(20)
#            while aux != '': # and hash_src != '':
#                logging.info("Lecture des hash_blocks")
                #poller_stdout.write(hash_src)
                #poller_stdout.flush()
#                p_stdout[fd].write(hash_src)
#                p_stdout[fd].flush()
#                logging.debug(binascii.hexlify(hash_src))
                
#                msg = poller_stdin.poll(maxevents = 5)
#                logging.debug("msg=='%s'"%msg)
#                if len(msg) != 5 :
#                    logging.error("Error clone_src_main 1")
#                    break
#                    if msg == 'next\n' :
#                        logging.info("Passage au bloc suivant")
#                    elif msg == 'sent\n':
#                        logging.info("Envoi du bloc")
#                        sic = os.lseek(fh_src.fileno(), i*2048*512, os.SEEK_SET)
#                    if sic != i*2048*512:
#                        logging.error("os.lseek(fh_src...) error")
#                        break
#                    aux = fh_src.read(2048*512)
#                    if aux == '':
#                        logging.error("fh_src.read() error")
#                        break
#                    poller_stdout(aux)
#                    poller_stdout()
#                    #poller_stdout.flush()
#                else:
#                    logging.debug("valeur de 'msg' : %s" % msg)
#                    logging.error("Error clone_src_main 2")
#                    break
#                
#                hash_src = fichier_hash.read(20)
                i += 1
        n += 1
    
    poller_stdin.unregister(ips_fh)
    poller_stdin.close()
    poller_stdout.unregister(ipd_fh)
    poller_stdout.close()
    fh_src.close()
    #logging.info("Clonage disque fini. Merci d'avoir attendu patiemment")
    logging.warn("Clonage disque fini. Merci d'avoir attendu patiemment")
    #############################################################################################################################################

if __name__ == '__main__':
    main()
