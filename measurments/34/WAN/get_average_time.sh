#!/usr/bin/bash

WAN22bz2='WAN34_bz2_2023-04-05--12-27-35'

awk '{x += $0} END {print "run time WAN22 bz2: " x/100}' run_time_$WAN22bz2
awk '{x += $0} END {print "client time WAN22 bz2: " x/100}' client_time_$WAN22bz2
awk '{x += $0} END {print "ver1 time WAN22 bz2: " x/100}' verifier1_time_$WAN22bz2
awk '{x += $0} END {print "ver2 time WAN22 bz2: " x/100}' verifier2_time_$WAN22bz2
