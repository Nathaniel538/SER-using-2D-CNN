import pandas as pd
import numpy as np
import librosa
import time
import os
import sys
if os.path.abspath('../lib') not in sys.path:
    sys.path.insert(0, os.path.abspath('../lib'))
import util_for_2d_features as util
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

def extract_and_get_features(data_path):
    start_epoch_time = time.time()
    print('starting feature extraction...\nstarted at', time.ctime(start_epoch_time))
    X, Y = np.array([np.zeros((106, 160))]), np.array([])
    i = 0
    for path, emotion in zip(data_path.Path, data_path.Emotions):
        y, sr = librosa.load(path)
        X = util.get_all_features_with_variations(y, sr, X)
        Y = np.append(Y, [emotion, emotion, emotion])
        i += 1
        print(round(i * 100 / len(data_path), 3), '\t%', end='\r')
    end_epoch_time = time.time()
    print('ended at', time.ctime(end_epoch_time))
    print('time taken ==>', round((end_epoch_time - start_epoch_time) / 60, 2), 'minutes')
    X = np.delete(X, 0, axis = 0)
    print('X.shape, Y.shape ==>', X.shape, Y.shape)
    return X, Y

def store_X(X):
    data_X = np.asarray(X)
    to_store_at = os.path.join(os.path.abspath('..'), 'data', 'data_x.npz')
    np.savez_compressed(to_store_at, data_X)
    print('successfully saved data_x.npz to', to_store_at)

def store_Y(Y):
    data_y = np.asarray(Y)
    to_store_at = os.path.join(os.path.abspath('..'), 'data', 'data_y.npz')
    np.savez_compressed(to_store_at, data_y)
    print('successfully saved data_y.npz to', to_store_at)

def main():
    data_path = pd.read_csv(os.path.join(os.path.abspath('..'), 'data', 'data_path.csv'))
    print('successfully loaded data_path.csv')
    X, Y = extract_and_get_features(data_path)
    store_X(X)
    store_Y(Y)

if __name__ == '__main__':
    main()
