import pandas as pd

class BenchmarkParams():
    def __init__(self, wk_num):
        super(BenchmarkParams, self).__init__()
        self.wk_num = wk_num
        self.wk_info = pd.read_csv('workload_info.csv')
        self.entry_num = self.wk_info['entry_num'][self.wk_num] # [1032444, 261124, 65472, 16380]
        self.value_size = self.wk_info['value_size'][self.wk_num] # [1024, 4096, 16384, 65536]
        self.benchmark = self.wk_info['benchmark'][self.wk_num] # ['readrandomwriterandom', 'updaterandom']
        self.benchmark_option = self.wk_info['benchmark_option'][self.wk_num] # [90, 50, 10]

    def get_entry_num(self):
        # ''' n = ?
        #     0~3 => 0
        #     4~7 => 1
        #     8~11 => 2
        #     12~15 => 3
        # '''
        # n = int(self.wk_num/4)
        # return self.entry_num[n]
        return self.entry_num

    def get_value_size(self):
        # n = int(self.wk_num/4)
        # return self.value_size[n]
        return self.value_size

    def get_benchmark(self):
        # n = self.wk_num%4
        # if n == 3:
        #     return self.benchmark[1]
        # return self.benchmark[0]
        return self.benchmark

    def get_benchmark_option(self):
        # n = self.wk_num%4
        # if n != 3:
        #     return self.benchmark_option[n]
        return self.benchmark_option
