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
python main.py --wk 0
</pre>

#### Provided Option
<pre>
wk          : workload index 
              type=int
              default=0
mode        : configuration option {0: by config file option
                                    1: by random option
                                    3: by generated config option}
              type=int
              default=0
num         : number of generated samples
              default=20
config_path : config file path
              "./conf_tmp/"
</pre>
