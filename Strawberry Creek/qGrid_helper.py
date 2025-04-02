import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_table(n, arr):
    '''
    Generates a table with n rows using columns passed in by arr.
    '''
    input_dict = {}
    for i in arr:
        input_dict[i] = ["Empty"] * n
    df = pd.DataFrame(input_dict)
    return df