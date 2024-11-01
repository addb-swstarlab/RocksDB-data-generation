import os
import sys
import argparse
import pandas as pd
import configparser

from option import *
from parsing import *
from benchmark_params import BenchmarkParams
from params import (ROCKSDB_DIR_PATH, RESULT_DIR_PATH)

# Use argparser to get command options
argparser = argparse.ArgumentParser(description="rocksdb dbbench test program")
argparser.add_argument('--wk', required=True, default=0, type=str, help="which workload a user wants to test")
argparser.add_argument('--key', default=16, type=int, help="Define key size on workloads")
argparser.add_argument('--value', default=1024, type=int, help="Define value size on workloads")
argparser.add_argument('--num', default=100000, type=int, help="Define number of key/value pairs on workloads")
argparser.add_argument('--sample_size', required=False, default=10, type=int, help="Define a sample size")
argparser.add_argument('--workload_options', type=str, help="Define workload options")
argparser.add_argument('--readwritepercent', default=0, type=int, help="Define workload options of read write percent, if necessary")
argparser.add_argument('--generate', action='store_true')

args = argparser.parse_args()

CONFIG_DIR_PATH = os.path.join(RESULT_DIR_PATH, str(args.wk), 'configs')
EXTERNAL_FILE_PATH = os.path.join(RESULT_DIR_PATH, str(args.wk), f"external_results_{args.wk}.csv")
INTERNAL_FILE_PATH = os.path.join(RESULT_DIR_PATH, str(args.wk), f"internal_results_{args.wk}.csv")
RESULT_FILE_PATH = os.path.join(RESULT_DIR_PATH, str(args.wk), 'result.txt')

def get_benchmark_option():
    benchmark_option = f'--benchmarks="{args.workload_options},compact,stats" --statistics'
    if args.readwritepercent > 0:
        benchmark_option += r'--readwritepercent{args.readwritepercent}'
    
    benchmark_option += f" > {RESULT_FILE_PATH}"
    return benchmark_option

def get_front_cmd():
    front_cmd = " ".join([ROCKSDB_DIR_PATH+"/db_bench", f"-key_size={args.key}", f"-value_size={args.value}", f"-num={args.num}"])
    return front_cmd

# Generate random RocksDB configurations
def gen_config(sample_size: int, path: str):
    db_bench_cmds = []
    pd_configs = pd.DataFrame()
    for i in range(sample_size):
        db_bench_datas, _ = args.value
        # create random option
        db_bench_configs, dict_config = make_random_option()
        # benchmarks option
        db_bench_benchmarks = get_benchmark_option()

        db_bench_cmd = ROCKSDB_DIR_PATH + "/db_bench " + db_bench_datas + db_bench_configs + db_bench_benchmarks
        db_bench_cmds.append(db_bench_cmd)
        
        pd_configs = pd.concat([pd_configs, pd.DataFrame.from_dict([dict_config])])
    pd_configs = pd_configs.reset_index(drop=True)
    pd_configs.to_csv(os.path.join(path, "knobs.csv"))
    return db_bench_cmds, pd_configs

def convert_conf_to_cmd(sample_size: int, path: str):
    db_bench_cmds = []
    c = configparser.ConfigParser()
    
    for i in range(sample_size):
        c.read(os.path.join(CONFIG_DIR_PATH, f'config{i+1}.cnf'))
        data = dict(c["rocksdb"])
        cmd = get_front_cmd()
        for k, v in data.items():
            cmd = " ".join([cmd, f'-{k}={v}'])
        
        cmd = " ".join([cmd, get_benchmark_option()])
        db_bench_cmds.append(cmd)
    
    return db_bench_cmds
    

def gen_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    gen_dir(RESULT_DIR_PATH)
    gen_dir(CONFIG_DIR_PATH)
        
    if args.generate: # generate rocksdb configurations randomly
        db_bench_cmds, pd_configs = gen_config(args.sample_size, CONFIG_DIR_PATH)
    else:
        # assert False, "to do: convert exist configs to db_bench commands"
        db_bench_cmds = convert_conf_to_cmd(args.sample_size, CONFIG_DIR_PATH)
    
    pd_externals = pd.DataFrame()
    pd_internals = pd.DataFrame()
    for i, bench_cmd in enumerate(db_bench_cmds):
        os.system(bench_cmd)
        
        res_external = parsing_external(RESULT_FILE_PATH)
        res_internal = parsing_internal(RESULT_FILE_PATH)
        
        pd_externals = pd.concat([pd_externals, pd.DataFrame.from_dict([res_external])])
        pd_internals = pd.concat([pd_internals, pd.DataFrame.from_dict([res_internal])])
    
        pd_externals.to_csv(EXTERNAL_FILE_PATH)
        pd_internals.to_csv(INTERNAL_FILE_PATH)
        
    pd_externals = pd_externals.reset_index(drop=True)
    pd_internals = pd_internals.reset_index(drop=True)
    
    pd_externals.to_csv(EXTERNAL_FILE_PATH)
    pd_internals.to_csv(INTERNAL_FILE_PATH)
