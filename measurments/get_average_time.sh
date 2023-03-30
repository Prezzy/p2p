#!/usr/bin/bash

LAN22='LAN22_2023-03-28--21-13-16'
WAN22='WAN22_2023-03-28--21-55-43'
WAN22bz2='WAN22_bz2_2023-03-29--11-18-22'
WAN22lz='WAN22_lz_2023-03-29--10-34-00'
WAN22zip='WAN22_zip_2023-03-29--12-37-15'

awk '{x += $0} END {print "run time LAN22: " x/100}' run_time_$LAN22
awk '{x += $0} END {print "client time LAN22: " x/100}' client_time_$LAN22
awk '{x += $0} END {print "ver1 time LAN22: " x/100}' verifier1_time_$LAN22
awk '{x += $0} END {print "ver2 time LAN22: " x/100}' verifier2_time_$LAN22

awk '{x += $0} END {print "run time WAN22: " x/100}' run_time_$WAN22
awk '{x += $0} END {print "client time WAN22: " x/100}' client_time_$WAN22
awk '{x += $0} END {print "ver1 time WAN22: " x/100}' verifier1_time_$WAN22
awk '{x += $0} END {print "ver2 time WAN22: " x/100}' verifier2_time_$WAN22

awk '{x += $0} END {print "run time WAN22 bz2: " x/100}' run_time_$WAN22bz2
awk '{x += $0} END {print "client time WAN22 bz2: " x/100}' client_time_$WAN22bz2
awk '{x += $0} END {print "ver1 time WAN22 bz2: " x/100}' verifier1_time_$WAN22bz2
awk '{x += $0} END {print "ver2 time WAN22 bz2: " x/100}' verifier2_time_$WAN22bz2

awk '{x += $0} END {print "run time WAN22 lz: " x/100}' run_time_$WAN22lz
awk '{x += $0} END {print "client time WAN22 lz: " x/100}' client_time_$WAN22lz
awk '{x += $0} END {print "ver1 time WAN22 lz: " x/100}' verifier1_time_$WAN22lz
awk '{x += $0} END {print "ver2 time WAN22 lz: " x/100}' verifier2_time_$WAN22lz

awk '{x += $0} END {print "run time WAN22 zip: " x/100}' run_time_$WAN22zip
awk '{x += $0} END {print "client time WAN22 zip: " x/100}' client_time_$WAN22zip
awk '{x += $0} END {print "ver1 time WAN22 zip: " x/100}' verifier1_time_$WAN22zip
awk '{x += $0} END {print "ver2 time WAN22 zip: " x/100}' verifier2_time_$WAN22zip
