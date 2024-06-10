import pandas as pd
import os
import glob
import time
import subprocess
import itertools

# List of parameters to modify
params_to_modify = ['mperc1', 'mperc2', 'wcfc1', 'wcfc2', 'wcfc3', 'wcep1', 'wcep2', 'wcep3', 'rrcs1']

# List of values to test for each parameter
values_to_test = {
    'mperc1': [5, 100],
    'mperc2': [5, 100],
    'wcfc1': [0.05, 0.5],
    'wcfc2': [0.05, 0.5],
    'wcfc3': [0.05, 0.5],
    'wcep1': [0.05, 0.5],
    'wcep2': [0.05, 0.5],
    'wcep3': [0.05, 0.5],
    'rrcs1': [0.05, 0.5]
}

# Generate all combinations of parameter values
all_combinations = itertools.product(*values_to_test.values())

# Read the config file
with open(r'C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration\par.txt', 'r') as f:
    original_config_lines = f.readlines()
resultats = pd.DataFrame()
count = 0
# Iterate over all combinations and export par.txt 
for i, combination in enumerate(all_combinations):
    config_lines = original_config_lines.copy()
    combin = ''
    for param, value in zip(params_to_modify, combination):
        combin_count = f'{param}={value}' # get each param and its value
        combin = ",".join([combin, combin_count]) # group all params and their values
        for j, line in enumerate(config_lines):
            if line.lstrip().startswith(param):
                parts_1 = line.split('\t') # split the param's name and all the values
                parts = parts_1[1].strip().split(' ') # get a list of all values
                parts[3] = str(value) # change the fourth value
                config_lines[j] = parts_1[0] +'\t'+ ' '.join(parts) + '\n' # rebuild all the line 
                break
    combin = combin[1:]
    count += 1
    # Write the modified config file
    with open(r"C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration\par.txt", 'w') as f:
        f.writelines(config_lines)
    process = subprocess.Popen([r'C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration\HYPE.exe'])
    time.sleep(1)
    log_file_prefix = 'hyss_000_'
    log_dir = r"C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration"
    latest_log_file = max(glob.glob(os.path.join(log_dir, f'{log_file_prefix}*')), key=os.path.getctime)
    while True:
        time.sleep(1)
        with open(latest_log_file, 'r') as f:
            log_contents = f.read()
        if 'Job finished date:' in log_contents:
            process.terminate()
            break
        time.sleep(1)    
    with open(r"C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration\results\subass1.txt", 'r') as file:
        next(file)
        lines = file.readlines()
    data = [line.strip().split() for line in lines[1:]]
    df = pd.DataFrame(data, columns=['SUBID', 'NSE', 'CC', 'RE(%)', 'RSDE(%)', 'Sim', 'Rec', 'SDSim', 'SDRec', 'MAE', 'RMSE', 'Bias', 'SDE', 'KGE', 'KGESD', 'KGEM', 'NRMSE', 'NSEW', 'Nrec'])
    result = df[['SUBID', 'NSE', 'KGE']]
    result['parameters'] = combin
    for i in combin.split(","):
        list = str(i).split("=")
        result[list[0]] = float(list[1])
    resultats = pd.concat([resultats, result])
    resultats.sort_index()
    print(f"Iteration N°{count+1} is done.")
    result.to_csv('result.csv', index=False)
    resultats.to_csv('resultats.csv', index=False)
