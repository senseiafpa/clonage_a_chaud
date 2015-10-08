#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import sys
import select
import subprocess
import logging



def main():
    ip_list = ("127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4")
    client_infos = {}
    e = select.epoll()
    # Fork all ssh for clients and register all sockets
    for ip in ip_list:
        p = subprocess.Popen(['./yes.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (fh_in, fh_out) = (p.stdout, p.stdin)
        client_infos[fh_in.fileno()] = (fh_in, fh_out, ip, 0)
        e.register(fh_in)
    # Main read loop
    try:
        while True:
            events = e.poll(1)
            logging.debug("events : %s"%events)
            for fileno, event_type in events:
                (fh_in, fh_out, ip, current_block_number) = client_infos[fileno]

                if event_type & select.EPOLLIN:
                    msg = fh_in.read(1)
                    process_msg(msg, fh_out, ip, current_block_number)
                    current_block_number += 1
                    client_infos[fileno] = (fh_in, fh_out, ip, current_block_number)
                else:
                    logging.debug("Evt d'un type non gere : %i"%event_type)

    finally:
        logging.debug("Fermeture de tous les sockets")
        for fileno in client_infos:
            fh_in = client_infos[fileno][0]
            e.unregister(fh_in)
            fh_in.close()
        e.close()




def process_msg(msg, fh_out, ip, current_block_number):
    logging.debug("Recu de %s(%i) : %s"%(ip,current_block_number,msg))
    fh_out.write("OK pour %s\n"%msg)







if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='/tmp/epoll.log')
    main()
