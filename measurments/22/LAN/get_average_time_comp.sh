#!/usr/bin/bash

LAN22='LAN22_bz2_2023-05-04--23-24-49'

awk '{x += $0} END {print "run time LAN22: " x/100}' run_time_$LAN22
awk '{x += $0} END {print "client time LAN22: " x/100}' client_time_$LAN22
awk '{x += $0} END {print "ver1 time LAN22: " x/100}' verifier1_time_$LAN22
awk '{x += $0} END {print "ver2 time LAN22: " x/100}' verifier2_time_$LAN22
