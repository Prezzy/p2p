#!/usr/bin/bash


dt=`date '+%Y-%m-%d--%H-%M-%S'`

mv total_run_time measurments/run_time_LAN33_zip_$dt
mv client_time measurments/client_time_LAN33_zip_$dt
mv verifier_1_time measurments/verifier1_time_LAN33_zip_$dt
mv verifier_2_time measurments/verifier2_time_LAN33_zip_$dt
