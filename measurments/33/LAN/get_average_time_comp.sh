#!/usr/bin/bash

LAN33='LAN33_bz2_2023-05-05--01-58-06'

awk '{x += $0} END {print "run time LAN33: " x/100}' run_time_$LAN33
awk '{x += $0} END {print "client time LAN33: " x/100}' client_time_$LAN33
awk '{x += $0} END {print "ver1 time LAN33: " x/100}' verifier1_time_$LAN33
awk '{x += $0} END {print "ver2 time LAN33: " x/100}' verifier2_time_$LAN33
