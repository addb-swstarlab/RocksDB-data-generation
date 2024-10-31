import os
import sys
import argparse
import pandas as pd

from option import *
from parsing import *
from benchmark_params import BenchmarkParams
from params import (ROCKSDB_PATH, RESULT_PATH)

# Use argparser to get command options
argparser = argparse.ArgumentParser(description="rocksdb dbbench test program")
argparser.add_argument('--wk', required=True, default=0, type=int, help="which workload a user wants to test")
argparser.add_argument('--key', default=16, type=int, help="Define key size on workloads")
argparser.add_argument('--value', default=1024, type=int, help="Define value size on workloads")
argparser.add_argument('--num', default=100000, type=int, help="Define number of key/value pairs on workloads")
argparser.add_argument('--sample_size', required=False, default=10, type=int, help="Define a sample size")
argparser.add_argument('--workload_options', type=str, help="Define workload options")
argparser.add_argument('--readwritepercent', default=0, type=int, help="Define workload options of read write percent, if necessary")
argparser.add_argument('--generate', action='store_true')

args = argparser.parse_args()

CONFIG_FILE_PATH = os.path.join(RESULT_PATH, str(args.wk), 'configs')
EXTERNAL_FILE_PATH = os.path.join(RESULT_PATH, str(args.wk), f"external_results_{args.wk}.csv")
INTERNAL_FILE_PATH = os.path.join(RESULT_PATH, str(args.wk), f"internal_results_{args.wk}.csv")
RESULT_FILE_PATH = os.path.join(RESULT_PATH, str(args.wk), 'result_txt')

benchmark_option = f'--benchmarks={args.workload_options},compact,stats --statistics'
if args.readwritepercent > 0:
    benchmark_option += r'--readwritepercent{args.readwritepercent}'

# -------------------
# Set value size for specific workload
def set_value_size():
    key_size = 16
    value_size = int(BP.get_value_size())
    entry_num = int(BP.get_entry_num())
    data_option = f"-key_size={key_size} -value_size={value_size} -num={entry_num} "
    tmp_dict = {"key_size" : key_size, "value_size" : value_size, "num" : entry_num}
    # print(data_option)
    return data_option, tmp_dict

# Set benchmark type and options for specific workload
def set_benchmark():
    benchmark = BP.get_benchmark() # "readrandomwriterandom"
    if benchmark == "readrandomwriterandom":
        benchmark_option = f'--benchmarks="{benchmark},compact,stats" --statistics --readwritepercent={int(BP.get_benchmark_option())}'
    elif benchmark == "updaterandom":
        benchmark_option = f'--benchmarks="{benchmark},compact,stats" --statistics'
    elif benchmark == "fillrandom":
        benchmark_option = f'--benchmarks="{benchmark},compact,stats" --statistics'
    # print(benchmark_option)
    # assert False
    return benchmark_option

# Generate random RocksDB configurations
def gen_config(number : int, path):
    db_bench_cmds = []
    pd_configs = pd.DataFrame()
    for i in range(number):
        db_bench_datas, _ = set_value_size()
        # create random option
        db_bench_configs, dict_config = make_random_option()
        # benchmarks option
        db_bench_benchmarks = set_benchmark()

        db_bench_cmd = ROCKSDB_PATH + "/db_bench " + db_bench_datas + db_bench_configs + db_bench_benchmarks
        db_bench_cmds.append(db_bench_cmd)
        
        pd_configs = pd.concat([pd_configs, pd.DataFrame.from_dict([dict_config])])
    pd_configs = pd_configs.reset_index(drop=True)
    pd_configs.to_csv(os.path.join(path, "knobs.csv"))
    return db_bench_cmds, pd_configs


def gen_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    gen_dir(RESULT_PATH)
    gen_dir(CONFIG_FILE_PATH)
    gen_dir(RESULT_FILE_PATH)
        
    if GEN_CONFIGS: # generate rocksdb configurations randomly
        db_bench_cmds, pd_configs = gen_config(NUM, CONFIG_FILE_PATH)
    else:
        assert False, "to do: convert exist configs to db_bench commands"
    
    result_paths = []
    pd_externals = pd.DataFrame()
    pd_internals = pd.DataFrame()
    for i, dbc in enumerate(db_bench_cmds):
        result_path = os.path.join(RESULT_FILE_PATH, f'results_{i}.txt')
        result_paths.append(result_path)
        os.system(f"{dbc} > {result_path}")
        
        res_external = parsing_external(result_path)
        res_internal = parsing_internal(result_path)
        
        pd_externals = pd.concat([pd_externals, pd.DataFrame.from_dict([res_external])])
        pd_internals = pd.concat([pd_internals, pd.DataFrame.from_dict([res_internal])])
    
    pd_externals = pd_externals.reset_index(drop=True)
    pd_internals = pd_internals.reset_index(drop=True)
    
    pd_externals.to_csv(EXTERNAL_FILE_PATH)
    pd_internals.to_csv(INTERNAL_FILE_PATH)
