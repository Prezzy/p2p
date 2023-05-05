#!/usr/bin/bash

WAN23bz2='WAN23_bz2_2023-05-05--02-41-52'

awk '{x += $0} END {print "run time WAN23 bz2: " x/100}' run_time_$WAN23bz2
awk '{x += $0} END {print "client time WAN23 bz2: " x/100}' client_time_$WAN23bz2
awk '{x += $0} END {print "ver1 time WAN23 bz2: " x/100}' verifier1_time_$WAN23bz2
awk '{x += $0} END {print "ver2 time WAN23 bz2: " x/100}' verifier3_time_$WAN23bz2
