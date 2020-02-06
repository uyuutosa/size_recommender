import pandas as pd
from numpy import *

import pytest

class SizeRecommender:
    def  __init__(self, path):
        self.f = pd.ExcelFile(path)
    def _recommend(self, df, param_dic, required_param_lst):
        c_max = where(["max" in x for x in df.columns ])[0][-1]
        idx_lst = []
        for i in range(0, c_max+1, 2):
            n_min, n_max = df.columns[i:i+2]
            result = df[(df[n_min] <= param_dic[n_min.strip("_min")]) == (df[n_max] > param_dic[n_min.strip("_min")])]
            if result.shape[0]:
                idx_lst += [result.index[0]]
    
        # extract most frequent value
        a,b = unique(idx_lst, return_counts=True)
        ret_dic = {}
        for p in required_param_lst:
            ret_dic[p] = df.loc[a[b.argmax()]][p]
        return ret_dic
            
    def _get_df(self, sheet_name):
        df = self.f.parse(sheet_name)
        return df
        
    def recommend(self, param_dic, sheet_name, required_param_lst):
        df = self._get_df(sheet_name)
        return self._recommend(df, param_dic, required_param_lst)
    
        
@pytest.fixture()
def data_male():
    param_dic = {"Height": 170, "Neck":39, "Chest": 90, "Waist":80, "Hip": 90}
    ret = {"param_dic": param_dic}
    return ret

def test_male(data_male):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    assert sr.recommend(data_male["param_dic"], "male", ["size"]) == {"size": "M"}

@pytest.fixture()
def data_female():
    param_dic = {"Height": 163, "Chest": 88, "Waist":72, "Hip": 99}
    ret = {"param_dic": param_dic}
    return ret

def test_female(data_female):
    sr = SizeRecommender(path="assets/size_chart.xlsx")
    assert sr.recommend(data_female["param_dic"], "female", ["size"]) == {"size": "L"}
