#!/usr/bin/bash

WAN33bz2='WAN33_bz2_2023-05-05--01-13-32'

awk '{x += $0} END {print "run time WAN33 bz2: " x/100}' run_time_$WAN33bz2
awk '{x += $0} END {print "client time WAN33 bz2: " x/100}' client_time_$WAN33bz2
awk '{x += $0} END {print "ver1 time WAN33 bz2: " x/100}' verifier1_time_$WAN33bz2
awk '{x += $0} END {print "ver2 time WAN33 bz2: " x/100}' verifier2_time_$WAN33bz2
