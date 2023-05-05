#!/usr/bin/bash

LAN23='LAN23_bz2_2023-04-04--11-51-06'

awk '{x += $0} END {print "run time LAN22: " x/100}' run_time_$LAN23
awk '{x += $0} END {print "client time LAN22: " x/100}' client_time_$LAN23
awk '{x += $0} END {print "ver1 time LAN22: " x/100}' verifier1_time_$LAN23
awk '{x += $0} END {print "ver3 time LAN22: " x/100}' verifier3_time_$LAN23
