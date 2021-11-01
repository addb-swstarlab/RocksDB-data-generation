import os
import sys
import argparse

from option import *
from parsing import *
from instance_index import *
from benchmark_params import BenchmarkParams

# Use argparser to get command options
argparser = argparse.ArgumentParser(description="rocksdb dbbench test program")
argparser.add_argument('--wk', required=True, default=0, type=int, help="which workload a user wants to test")
argparser.add_argument('--mode', required=False, default=0, type=int, help="by config file option : 0|  by random option : 1| by gen config option : 2")
argparser.add_argument('--num', required=False, default=20, type=int, help="how many random option create and test")
argparser.add_argument('--config_path', required=False, default="./conf_tmp/", type=str, help="config file path")

args = argparser.parse_args()
IS_RANDOM = args.mode
NUM = args.num
CONFIG_FILE_PATH = args.config_path
BENCH_PATH = "/home/jieun/rocksdb"
BP = BenchmarkParams(args.wk)

###################################### Need to fix #############################################

# Set value size for specific workload
def set_value_size():
    key_size = 16
    value_size = int(BP.get_value_size())
    entry_num = int(BP.get_entry_num()) # 1GB 10GB  사이즈별 소요시간 측정
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
    # print(benchmark_option)
    # assert False
    return benchmark_option

#################################################################################################

# Execute db_bench by existed config files
def execute_by_config(config_file : str, tmp_dir : str):
    
    command = BENCH_PATH + "/db_bench "

    # Set key value size 
    data_option, tmp_dict = set_value_size()
    tmp_dict.update({"index" : config_file})
    command += data_option

    # Create random option
    option_list, option_dict = read_config_option(config_file)
    command += option_list
    option_dict.update(tmp_dict)

    # Benchmarks option
    benchmark_option = set_benchmark()
    command += benchmark_option

    # Bench result redirection
    directory, file = os.path.split(config_file)
    bench_result = f"{file.rstrip('.cnf')}.txt"
    bench_result = os.path.join(tmp_dir, bench_result)
    redirection_command = f"> {bench_result}"
    command += redirection_command
    
    # Execute benchmark test
    os.system(command)

    # Parsing
    ex_results = parsing_external(bench_result)
    ex_results.update({"index" : config_file})
    in_results = parsing_internal(bench_result)
    in_results.update({"index" : config_file})

    return ex_results, in_results, option_dict

# Execute db_bench by random config files
def execute_by_random(index : int, tmp_dir : str):

    command = BENCH_PATH + "/db_bench "

    # Set key value size 
    data_option, tmp_dict = set_value_size()
    tmp_dict.update({"index" : index})
    command += data_option

    # create random option
    option_list, option_dict = make_random_option()
    command += option_list
    option_dict.update(tmp_dict)

    # benchmarks option
    benchmark_option = set_benchmark()
    command += benchmark_option

    # save config
    random_config_filename = f"config{i}.cnf"
    random_config_filename = os.path.join(CONFIG_FILE_PATH, random_config_filename)
    save_option_as_cnf(option_dict, random_config_filename)

    # bench result redirection
    bench_result = f"{str(index).zfill(6)}.txt"
    bench_result = os.path.join(tmp_dir, bench_result)
    redirection_command = f"> {bench_result}"
    command += redirection_command
    
    # execute benchmark test
    os.system(command)

    # parsing
    ex_results = parsing_external(bench_result)
    ex_results.update({"index" : index})
    in_results = parsing_internal(bench_result)
    in_results.update({"index" : index})

    return ex_results, in_results, option_dict

# Generate random RocksDB configurations
def gen_config(number : int):
    for i in range(1,number+1):
        data_option, tmp_dict = set_value_size()
        #tmp_dict.update({"index" : i})

        # create random option
        option_list, option_dict = make_random_option()
        option_dict.update(tmp_dict)

        # benchmarks option
        benchmark_option = set_benchmark()

        # save config
        random_config_filename = f"config{i}.cnf"
        random_config_filename = os.path.join(CONFIG_FILE_PATH, random_config_filename)
        save_option_as_cnf(option_dict, random_config_filename)

if __name__ == "__main__":

    # arguments parsing

    # create directory for benchmark result data
    try:
        os.mkdir(os.path.join(os.getcwd(), "tmp_data"))
    except:
        pass
    finally:
        tmp_dir = os.path.join(os.getcwd(), "tmp_data")

    range_start, range_end, idx = get_instance_index(NUM)

    external_file_path = "external_results_"+str(idx)+".csv"
    internal_file_path = "internal_results_"+str(idx)+".csv"

    external_file = os.path.join(os.getcwd(), external_file_path)
    internal_file = os.path.join(os.getcwd(), internal_file_path)
    
    #record_column = [key for key in external_params] + [key for key in outputs]
    record_column = [key for key in outputs]

    ex_result_file = open(external_file, "w")
    ex_result_file.write(",".join(record_column) + "\n")
    ex_result_file.close()

    in_result_file = open(internal_file, "w")
    in_result_file.write(",".join(internal_params) + "\n")
    in_result_file.close()

    
    if IS_RANDOM == 1:
        # random option으로 실행
        for i in range(range_start, range_end):
            # execute bench
            ex_results, in_results, option_dict = execute_by_random(i, tmp_dir)

            # save record to csv
            # ex_record = [ex_results[key] for key in outputs] + [option_dict[key] for key in external_params]
            ex_record = [ex_results[key] for key in outputs]
            ex_result_file = open(external_file, "a")
            ex_result_file.write(",".join(map(str, ex_record)) + "\n")
            ex_result_file.close()

            in_record = [in_results[key] for key in internal_params]
            in_result_file = open(internal_file, "a")
            in_result_file.write(",".join(map(str, in_record)) + "\n")
            in_result_file.close()

    elif IS_RANDOM == 0:
        # config file을 읽어서 실행
        #for index in range(3, 23):
        for index in range(1):

            config_file = os.path.abspath(os.path.join(CONFIG_FILE_PATH, "config{}.cnf".format(index)))

            # execute bench
            ex_results, in_results, option_dict = execute_by_config(config_file, tmp_dir)

            # save record to csv
            #ex_record = [ex_results[key] for key in outputs] + [option_dict[key] for key in external_params]
            ex_record = [ex_results[key] for key in outputs]
            ex_result_file = open(external_file, "a")
            ex_result_file.write(",".join(map(str, ex_record)) + "\n")
            ex_result_file.close()

            in_record = [in_results[key] for key in internal_params]
            in_result_file = open(internal_file, "a")
            in_result_file.write(",".join(map(str, in_record)) + "\n")
            in_result_file.close()
    elif IS_RANDOM == 2:
        gen_config(20000)
