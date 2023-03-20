import argparse, os
import pandas as pd
from parsing import parsing_external, parsing_internal

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str)
opt = parser.parse_args()

DIR_PATH = f'results/{opt.dir}'
RESULT_PATH = 'csv'

if os.path.exists(RESULT_PATH) is False:
    os.mkdir(RESULT_PATH)

file_names = os.listdir(DIR_PATH)

externals = pd.DataFrame()
internals = pd.DataFrame()

for f_name in file_names:
    f_ex = parsing_external(os.path.join(DIR_PATH, f_name))
    f_in = parsing_internal(os.path.join(DIR_PATH, f_name))
    
    pd_ex = pd.DataFrame.from_dict(f_ex, orient='index', columns=[f_name[:-4]])
    pd_in = pd.DataFrame.from_dict(f_in, orient='index', columns=[f_name[:-4]])
    
    externals = pd.concat([externals, pd_ex], axis=1)
    internals = pd.concat([internals, pd_in], axis=1)
    
externals.T.to_csv(os.path.join(RESULT_PATH, opt.dir+'_external_results.csv'))
internals.T.to_csv(os.path.join(RESULT_PATH, opt.dir+'_internal_results.csv'))
