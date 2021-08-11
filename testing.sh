#!/bin/bash

cd /home/jieun/data_generation_rocksdb
python main.py --wk $1
cd /home/jieun
tail -n 1 /home/jieun/data_generation_rocksdb/external_results_11.csv >> comp_results.csv
