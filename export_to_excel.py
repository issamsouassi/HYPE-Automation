import pandas as pd

df = pd.read_csv(r'..\Calibration\resultats.csv')
subid_dict = {k: v for k, v in df.groupby('SUBID')}
with pd.ExcelWriter(fr'C:\Users\SOUASSI\Documents\ENGEES\TFE\Wiam\Calibration\results\BV_id\BV.xlsx') as writer:
    for key, value in subid_dict.items():
        value.to_excel(writer, sheet_name=f'BV_{key}', index=False)