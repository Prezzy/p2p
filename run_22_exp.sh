#!/usr/bin/bash


for i in {1..100}
do 
	taskset -c 0 python3 ver1_node.py &
	sleep 2
	taskset -c 1 python3 ver2_node.py &
	sleep 2
	taskset -c 2 python3 client_node.py

	wait
	echo "done experiment $i"
done
