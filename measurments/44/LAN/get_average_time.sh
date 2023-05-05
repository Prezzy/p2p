#!/usr/bin/bash

LAN44='LAN44_bz2_2023-04-04--13-49-20'

awk '{x += $0} END {print "run time LAN44: " x/100}' run_time_$LAN44
awk '{x += $0} END {print "client time LAN44: " x/100}' client_time_$LAN44
awk '{x += $0} END {print "ver1 time LAN44: " x/100}' verifier1_time_$LAN44
awk '{x += $0} END {print "ver2 time LAN44: " x/100}' verifier2_time_$LAN44
