import numpy as np
import h5py

root_path = 'datasets'

def load_data():
    train_dataset = h5py.File(root_path + '/training_dataset.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])

    test_dataset = h5py.File(root_path + '/test_dataset.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig

train_x_orig, train_y_orig, test_x_orig, test_y_orig = load_data()