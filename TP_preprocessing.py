import pandas as pd
import numpy as np
import datetime

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def generate_csv_file(to_be_preprocessed):
    toConcat = []
    columns = ['Timestamp', 'Code', 'Message']

    df = pd.read_csv('clean_' + to_be_preprocessed , sep='(?:\]\s+\[)', engine = 'python', encoding= 'latin1', names=columns, usecols= [columns[0],columns[2]])
    #df = pd.read_csv('clean_jozagv_4' + '.log', sep='(?:\]\s+\[)', engine = 'python', names=columns, usecols= [columns[0],columns[2]])
    df['Timestamp'] = df['Timestamp'].apply(lambda x: x[1:15])
    df = df[df['Timestamp'].apply(lambda x: is_float(x))]
    df['Timestamp'] = df['Timestamp'].astype(float)
    df['Timestamp'] = df['Timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df['Message'] = df['Message'].astype("str")
    df['Message'] = df['Message'].replace('^.*\]\s*','', regex=True)
    df.rename(columns={'Timestamp':'Datetime'}, inplace = True)
    df.set_index('Datetime', inplace = True)
    df = df.sort_index()
    df[['transponder_code','global_tp_x','global_tp_y','local_tp_y']] = df['Message'].apply(lambda x: pd.Series([x.split(', ')[0][9:]] + x.split(', ')[4:6] + [x.split(', ')[1]]) if 'AGVTRS' in x else pd.Series([np.NaN,np.NaN,np.NaN,np.NaN]))
    df = df.drop('Message', 1)
    df.dropna(subset=['transponder_code','global_tp_x','global_tp_y'], how='all', inplace=True)

    df.to_csv('agv_df_' + datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S.%f") + '.csv')

def clean_log_files(file_path, file_name):
    columns = ['Timestamp', 'Code', 'Message']
    # New files saved as (clean_ + file name.log)
    words_to_check = ['[INFO    BatteryMonitor.cpp:262] System Power',
                '[INFO    BatteryMonitor.cpp:573] System Power @Disconnect',
                '[INFO    BatteryMonitor.cpp:573] System Power @Charger',
                'Continued in next file',
                'Continuation of previous file',
                'Version',
                'Revision',
                'Build date',
                'JOZ AGV',
                'SQLite Error']
    #Log files have different encoding, some of them can't be processed, so they all have be encoded in latin-1 beforehand.
    with open(file_path, encoding='latin-1') as toBeCleaned, open('clean_' + file_name, 'w', encoding='latin-1') as cleanFile:
        for line in toBeCleaned:
            clean = True
            for word in words_to_check:
                if word in line:
                    clean = False
            if clean == True:
                cleanFile.write(line)
    generate_csv_file(file_name)

'''
if __name__ == "__main__":
    clean_log_files()
'''

#clean_log_files()
