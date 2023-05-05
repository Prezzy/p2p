#!/usr/bin/bash

WAN23bz2='WAN23_bz2_2023-04-03--16-08-52'

awk '{x += $0} END {print "run time WAN22 bz2: " x/100}' run_time_$WAN23bz2
awk '{x += $0} END {print "client time WAN22 bz2: " x/100}' client_time_$WAN23bz2
awk '{x += $0} END {print "ver1 time WAN22 bz2: " x/100}' verifier1_time_$WAN23bz2
awk '{x += $0} END {print "ver2 time WAN22 bz2: " x/100}' verifier3_time_$WAN23bz2
