import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SynthPresetsDataset(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        
        # TODO: Fix this
        # if len(self.data) != len(self.labels):
        #     raise Exception("The length of 'data' does not match the length of 'labels'")        

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        X = self.data[index]
        y = self.labels[index]
        
        return X, y
    
def loadADSRData(path):
    df = pd.read_csv(path)    
    data = df.loc[:, 'amp_attack':'amp_release']
     
    for colum in data.columns:
        data[colum] = data[colum] / data[colum].abs().max()
        data[colum] = data[colum].replace(np.nan, 0)
 
    
    X = torch.tensor(data.values)
    y = torch.zeros(len(X))
    
    return X,y
    
    
    
# def loadData(path, DEBUG=False):
#     df = pd.read_csv(path) # Read from the CSV file
#     df.fillna(0, inplace = True) # Replace empty values with 0 TODO: ensure this is the proper strategy (should be)
    
#     labels = df['preset_name'] # Split out the labels
#     # print(labels.shape)
#     data = df.iloc[:, 1:].astype(np.float32) # Split out the Data

#     # Normalize data between -1 and 1
#     for colum in data.columns:
#         data[colum] = data[colum] / data[colum].abs().max()
#         data[colum] = data[colum].replace(np.nan, 0)
 

#     X = torch.tensor(data.values) # Store as PyTorch tensor
#     y = labels.to_numpy() # Store as strings in Numpy Array
#     # print(X.min())
    
#     if DEBUG:
#         print(data) # Print Head
#         print(data['amp_attack'].max())
#         print(data['amp_attack'].idxmax())
#         print(df[df['amp_attack'] >= 0.6])
#         print("X Shape:", X.shape)
#         print("Y Shape:", y.shape)   
    
#     return X, y

def loadDataCategorical(path, DEBUG=False, DROP=False):
    added_cols = []
    df = pd.read_csv(path) # Read from the CSV file    
    print(df.isna().any())
    
    if DROP:
        del df['filter_kbd_track']
        del df['filter_vel_sens']
        del df['amp_vel_sens']
        del df['portamento_mode']
        del df['master_vol']
        del df['distortion_crunch']
        del df['osc2_detune']    
    categorical = df.select_dtypes(include=['int16', 'int32', 'int64']).columns.to_list()
    categorical.append("freq_mod_osc")
    
    
    # df = df.replace(np.nan, 0) # Replace all NAN with 0
    df['freq_mod_osc'] = df['freq_mod_osc'].replace(np.nan, 0)
    df['freq_mod_osc'] = df['freq_mod_osc'].astype(np.int32)
    
    
    # print(categorical)
    # print(df['freq_mod_osc'])

        
    for col in categorical:
        if col == 'portamento_time': continue # TODO: Fix this properly

        newOH = pd.get_dummies(pd.Categorical(df[col], categories=getCategories(col)), prefix=col, dtype=np.int32)
        del df[col]
        for i in newOH.columns:
            added_cols.append(i)
            # a[a==0]=-1
            np_arr = newOH[i].to_numpy() # Convert to numpy array for next step
            np_arr[np_arr==0] = -1 # Replace all 0s with -1s for TANH one hot encoding.
            df[i] = np_arr # Set dataframe column with updated numpy array.
                    
    df.fillna(0, inplace = True) # Replace empty values with 0 TODO: ensure this is the proper strategy (should be)
    
    labels = df['preset_name'] # Split out the labels

    data = df.iloc[:, 1:].astype(np.float32) # Split out the Data
    
    # Do some basic data filtering.
    data = data[data['amp_attack'] < 0.6]
    data = data[data['amp_release'] < 0.6]
    data = data[data['filter_attack'] < 0.6]
    
    # print(data.columns)
    
    
    skip = 0    
    # Normalize data between -1 and 1
    for colum in data.columns:
        if colum in added_cols: 
            skip += 1
            continue
        data[colum] = data[colum] / data[colum].abs().max()
        # data[colum] = 2*((data[colum]-data[colum].min()) / (data[colum].max()-data[colum].max()))-1
        # data[colum] = data[colum].replace(np.nan, -1)
    
    
    X = torch.tensor(data.values) # Store as PyTorch tensor
    y = labels.to_numpy() # Store as strings in Numpy Array

    
    
    return X, y


def loadDataCategorical01(path, DEBUG=False, DROP=False):
    added_cols = []
    df = pd.read_csv(path) # Read from the CSV file    
    print(df.isna().any())
    
    if DROP:
        del df['filter_kbd_track']
        del df['filter_vel_sens']
        del df['amp_vel_sens']
        del df['portamento_mode']
        del df['master_vol']
        del df['distortion_crunch']
        del df['osc2_detune']
        del df['lfo_waveform']
        
    categorical = df.select_dtypes(include=['int16', 'int32', 'int64']).columns.to_list()
    categorical.append("freq_mod_osc")
    
    
    # df = df.replace(np.nan, 0) # Replace all NAN with 0
    df['freq_mod_osc'] = df['freq_mod_osc'].replace(np.nan, 0)
    df['freq_mod_osc'] = df['freq_mod_osc'].astype(np.int32)
    
    
    # print(categorical)
    # print(df['freq_mod_osc'])

        
    for col in categorical:
        if col == 'portamento_time': continue # TODO: Fix this properly

        newOH = pd.get_dummies(pd.Categorical(df[col], categories=getCategories(col)), prefix=col, dtype=np.int32)
        del df[col]
        for i in newOH.columns:
            added_cols.append(i)
            # a[a==0]=-1
            np_arr = newOH[i].to_numpy() # Convert to numpy array for next step
            np_arr[np_arr==0] = -1 # Replace all 0s with -1s for TANH one hot encoding.
            df[i] = np_arr # Set dataframe column with updated numpy array.
                    
    df.fillna(0, inplace = True) # Replace empty values with 0 TODO: ensure this is the proper strategy (should be)
    
    labels = df['preset_name'] # Split out the labels

    data = df.iloc[:, 1:].astype(np.float32) # Split out the Data
    
    # Do some basic data filtering.
    data = data[data['amp_attack'] < 0.6]
    data = data[data['amp_release'] < 0.6]
    data = data[data['filter_attack'] < 0.6]
    
    print(data.columns)
    
    
    skip = 0    
    # Normalize data between -1 and 1
    for colum in data.columns:
        if colum in added_cols: 
            skip += 1
            continue
        
        data[colum] = (data[colum] - data[colum].min()) / (data[colum].max() - data[colum].min()) 
        # data[colum] = 2*((data[colum]-data[colum].min()) / (data[colum].max()-data[colum].max()))-1
        # data[colum] = data[colum].replace(np.nan, -1)
    
    
    X = torch.tensor(data.values) # Store as PyTorch tensor
    y = labels.to_numpy() # Store as strings in Numpy Array

    
    
    return X, y



def getCategories(parameter_name):
    if parameter_name == 'osc1_waveform':
        return [i for i in range(5)]
    if parameter_name == 'osc2_waveform':
        return [i for i in range(5)]
    if parameter_name == 'lfo_waveform':
        return [i for i in range(7)]
    if parameter_name == 'osc2_range':
        return [i for i in range(8)]
    if parameter_name == 'osc_mix_mode':
        return [i for i in range(3)]
    if parameter_name == 'osc2_sync':
        return [i for i in range(2)]
    if parameter_name == 'keyboard_mode':
        return [i for i in range(3)]
    if parameter_name == 'osc2_pitch':
        return [i for i in range(25)]
    if parameter_name == 'filter_type':
        return [i for i in range(5)]
    if parameter_name == 'filter_slope':
        return [i for i in range(2)]
    

# loadDataCategorical("./datasets/amsynth_presets.csv")
# print(pd.cut(np.array([1, 7, 5, 4, 6, 3]), 3))
# Mongo Password: M67JuiuNqr0LJAVa