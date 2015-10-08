#!/bin/sh
dpipe ssh 172.16.20.38 python /windows/prog_dev/prog_clone_optimisation/clone_dst_main.py ={ pv -s $(blockdev --getsize64 /dev/sda1) {= python /windows/prog_dev/prog_clone_optimisation/clone_src_main.py
