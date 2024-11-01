# RocksDB sample generation
This repository is aiming at a generation of RocksDB samples to tuning its configuration knobs.

## RocksDB
RocksDB is a disk based database that can achieve fast data writing performance. 
Generation valuable RocksDB data is important for RocksDB optimization and analyzation studies. 
However, generating the useful data is a complex, difficult and time consuming task. 
This project is aiming at generating valuable RocksDB data with specific workload using db_bench and do some test for data analysis.
Users can also change RocksDB parameters while generating data.

If you want to apply this project to your own database, please remember to change parameter options as well as related files. 

## Requirements
- python3
### How to Install RocksDB and db_bench
You can install RocksDB and db_bench on here.
- https://github.com/facebook/rocksdb
- https://github.com/facebook/rocksdb/wiki/Benchmarking-tools

## Run
#### How to Run
<pre>
python main.py --wk 29 --key 16 --value 128 --num 5000000 --sample_size 100 --workload_option updaterandom --generate
</pre>

#### Provided Option
<pre>
--wk          : workload index 
                type=str
                default=0
--key         : Set a key size of workload
                type=int
--value       : Set a value size of workload
                type=int
--num         : Set number of key-value pairs
                type=int
--sample_size : number of generated samples
                default=20

--workload_options : Define workload options of db_bench
                     type=str
                     example) readrandom
--readwritepercent : Define read write ratios, if benchmark option includes readrandomwriterandom
                     type=int
                     example) 70 (It should be in [0,100]
--generate         : generate samples (trigger)
</pre>
